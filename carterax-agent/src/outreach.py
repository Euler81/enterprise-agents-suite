"""Generador de comunicaciones multi-canal personalizadas por perfil."""
from __future__ import annotations

from .scoring import Debtor, priority_tier


class OutreachGenerator:
    CHANNEL_BY_TIER = {"P1": "llamada+whatsapp", "P2": "whatsapp", "P3": "email+SMS"}

    def message(self, debtor: Debtor, offer: dict | None) -> dict:
        tier = priority_tier_from(debtor)
        channel = self.CHANNEL_BY_TIER[tier]
        nombre = debtor.name.split()[0]

        if offer:
            body = (f"Hola {nombre}, armamos un plan para regularizar tu cuenta: "
                    f"{offer['installments']} cuota(s) con "
                    f"{offer['discount']:.0%} de descuento y primera cuota de "
                    f"{offer['first_payment_pct']:.0%}. ¿Lo confirmamos?")
        else:
            body = (f"Hola {nombre}, tu cuenta tiene un saldo pendiente de "
                    f"${debtor.debt:,.0f}. Contactanos y lo resolvemos juntos.")

        return {"channel": channel, "tier": tier, "body": body}


def priority_tier_from(debtor: Debtor) -> str:
    from .scoring import risk_score
    return priority_tier(risk_score(debtor))
