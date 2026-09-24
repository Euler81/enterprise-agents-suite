"""Inventario de procesos internos de la empresa."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Process:
    name: str
    area: str
    owner: str
    sensitivity: int      # 1-5: qué tan expuesto está a regulación


PROCESSES = [
    Process("Onboarding digital de clientes", "data_privacy", "Producto", 5),
    Process("Motor de recomendación", "data_privacy", "Data", 4),
    Process("Liquidación de impuestos", "tax", "Finanzas", 4),
    Process("Monitoreo AML", "aml", "Compliance", 5),
    Process("Gestión de recibos", "tax", "Finanzas", 3),
    Process("Políticas de teletrabajo", "labor", "People", 2),
    Process("Términos y condiciones web", "consumer", "Legal", 3),
]
