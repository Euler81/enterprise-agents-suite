"""Proveedores y generación determinística de cotizaciones."""
from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass
class Quote:
    supplier: str
    price: float           # total por el volumen
    lead_days: int
    quality: float         # 0-5 rating histórico
    floor_pct: float       # piso de negociación: mín. descuento que acepta


def collect_quotes(rfq: RFQ, seed: int = 5) -> list[Quote]:
    random.seed(hash(rfq.item) % 10**6 + seed)
    suppliers = ["Proveedor Alfa", "Beta Industrial", "Gamma SRL", "Delta Corp", "Epsilon SA"]
    quotes = []
    for s in suppliers:
        price = rfq.budget * random.uniform(0.82, 1.15)
        quotes.append(Quote(s, round(price, 0),
                            random.randint(3, rfq.max_lead_days + 15),
                            round(random.uniform(2.5, 5.0), 1),
                            round(random.uniform(0.90, 0.97), 2)))
    return quotes
