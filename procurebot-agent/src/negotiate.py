"""Contraoferta al finalista y simulador de respuesta del proveedor."""
from __future__ import annotations

from .quotes import Quote

COUNTER_ASK = 0.95   # el agente pide 5% de descuento


def counter_offer(quote: Quote) -> tuple[float, bool]:
    """Pide 5% menos. El proveedor acepta si su piso lo permite.
    Devuelve (precio final, aceptó_negociación)."""
    asked = quote.price * COUNTER_ASK
    floor = quote.price * quote.floor_pct
    if asked >= floor:
        return round(asked, 0), True
    return quote.price, False
