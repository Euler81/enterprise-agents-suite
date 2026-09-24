"""Motor de políticas: define los límites dentro de los cuales
el agente puede negociar. Ninguna concesión puede exceder estos límites."""
from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class PolicyConfig:
    max_discount: float = float(os.getenv("MAX_DISCOUNT", 0.30))
    max_installments: int = int(os.getenv("MAX_INSTALLMENTS", 6))
    min_first_payment: float = float(os.getenv("MIN_FIRST_PAYMENT", 0.20))
    min_recovery_pv: float = float(os.getenv("MIN_RECOVERY_PV", 0.65))
    escalation_sentiment: float = float(os.getenv("ESCALATION_SENTIMENT", -0.5))
    monthly_rate: float = float(os.getenv("MONTHLY_RATE", 0.04))


class PolicyEngine:
    """Evalúa cada oferta del agente contra las políticas. Devuelve (ok, motivo)."""

    def __init__(self, cfg: PolicyConfig | None = None):
        self.cfg = cfg or PolicyConfig()

    def check_offer(self, offer: dict) -> tuple[bool, str]:
        if offer.get("discount", 0) > self.cfg.max_discount:
            return False, f"descuento {offer['discount']:.0%} > máx {self.cfg.max_discount:.0%}"
        if offer.get("installments", 1) > self.cfg.max_installments:
            return False, f"cuotas {offer['installments']} > máx {self.cfg.max_installments}"
        if offer.get("first_payment_pct", 1.0) < self.cfg.min_first_payment:
            return False, (f"primera cuota {offer['first_payment_pct']:.0%} "
                           f"< mín {self.cfg.min_first_payment:.0%}")
        if self.recovery_pv(offer) < self.cfg.min_recovery_pv:
            return False, f"PV recuperado {self.recovery_pv(offer):.2f} < mín"
        return True, "ok"

    def recovery_pv(self, offer: dict) -> float:
        """Valor presente de lo que realmente ingresa (post-descuento),
        descontando cuotas futuras por costo de capital."""
        debt = offer["debt"]
        net = debt * (1 - offer.get("discount", 0))
        n = offer.get("installments", 1)
        first = offer.get("first_payment_pct", 1.0)
        r = self.cfg.monthly_rate

        pv = net * first  # primera cuota: hoy
        rest = net * (1 - first)
        if n > 1 and rest > 0:
            cuota = rest / (n - 1)
            pv += sum(cuota / (1 + r) ** t for t in range(1, n))
        return round(pv / debt, 3)  # normalizado a la deuda original
