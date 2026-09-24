"""Loop de negociación: el agente ofrece, el deudor responde con una
utilidad simulada, y el agente concede dentro de política hasta cerrar
o agotar rondas (y entonces escalar o dejar campaña pasiva)."""
from __future__ import annotations

from .policies import PolicyEngine
from .scoring import Debtor, risk_score


class DebtorSimulator:
    """Simula la respuesta de un deudor real a una oferta.

    Utilidad = capacidad de pago percibida - esfuerzo de la oferta.
    Se calibra con el score: mejor perfil → acepta más fácil.
    """

    def __init__(self, debtor: Debtor):
        self.debtor = debtor
        self.utility = 0.45 + risk_score(debtor) / 200 - debtor.hostility_signals * 0.2
        self.rounds = 0
        self.hostility = debtor.hostility_signals

    def respond(self, offer: dict) -> tuple[bool, str, float]:
        """Devuelve (acepta, razón, sentimiento)."""
        self.rounds += 1
        n = offer.get("installments", 1)
        discount = offer.get("discount", 0)
        effort = 0.48 + 0.14 * n - 1.0 * discount - 0.12 * (self.rounds - 1)

        sentiment = 0.25 - 0.18 * self.rounds - self.hostility * 0.45 + discount

        if sentiment < -0.5:
            return False, "hostilidad creciente", sentiment
        if effort <= self.utility:
            return True, "acepta el plan", sentiment
        return False, "oferta insuficiente", sentiment


class Negotiator:
    """Estrategia de concesiones del agente: arranca estricto y cede
    sistemáticamente, SIEMPRE dentro de los límites del PolicyEngine."""

    def __init__(self, policy: PolicyEngine, debtor: Debtor, max_rounds: int = 4):
        self.policy = policy
        self.debtor = debtor
        self.max_rounds = max_rounds
        self.trace: list[dict] = []

    def _initial_offer(self) -> dict:
        return {"debt": self.debtor.debt, "discount": 0.0,
                "installments": 2, "first_payment_pct": 0.50}

    def _concede(self, offer: dict, round_n: int) -> dict:
        cfg = self.policy.cfg
        o = dict(offer)
        # Secuencia de concesiones: más cuotas → primera cuota menor → algo de descuento
        o["installments"] = min(o["installments"] + 1, cfg.max_installments)
        if round_n >= 2:
            o["first_payment_pct"] = max(o["first_payment_pct"] - 0.10,
                                         cfg.min_first_payment)
        if round_n >= 3:
            o["discount"] = min(o["discount"] + 0.10, cfg.max_discount)
        return o

    def negotiate(self) -> dict:
        sim = DebtorSimulator(self.debtor)
        offer = self._initial_offer()
        for round_n in range(1, self.max_rounds + 1):
            ok, reason, sentiment = sim.respond(offer)
            self.trace.append({"round": round_n, "offer": dict(offer),
                               "accepted": ok, "reason": reason,
                               "sentiment": round(sentiment, 2)})
            if sentiment < self.policy.cfg.escalation_sentiment:
                return {"outcome": "ESCALATE", "reason": "hostilidad",
                        "trace": self.trace}
            if ok:
                valid, _ = self.policy.check_offer(offer)
                if valid:
                    return {"outcome": "AGREED", "offer": offer,
                            "trace": self.trace}
            if round_n < self.max_rounds:
                offer = self._concede(offer, round_n)
        return {"outcome": "PASSIVE", "reason": "no hubo acuerdo en rondas",
                "trace": self.trace}
