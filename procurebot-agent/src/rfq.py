"""Solicitud de cotización (RFQ)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RFQ:
    item: str
    quantity: int
    budget: float          # presupuesto aprobado
    max_lead_days: int     # plazo máximo de entrega aceptable
