"""Normas regulatorias (fuente simulada: boletines oficiales)."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Norm:
    norm_id: str
    issuer: str              # BCRA, AAIP, AFIP, CNV...
    title: str
    area: str                # data_privacy | labor | tax | aml | consumer
    severity: str            # baja | media | alta | critica
    deadline_days: int       # plazo para adaptarse
    summary: str


NORM_DB = [
    Norm("N-2026-014", "AAIP", "Actualización reglamento datos personales",
         "data_privacy", "alta", 45,
         "Consentimiento expreso reforzado y derecho de portabilidad ampliado."),
    Norm("N-2026-021", "BCRA", "Nuevas exigencias de encaje digital",
         "tax", "media", 90, "Ajustes en liquidación de impuestos digitales."),
    Norm("N-2026-033", "CNV", "Recompra de acciones: nuevos límites de disclosure",
         "aml", "critica", 10, "Reporte inmediato de operaciones sospechosas."),
    Norm("N-2026-040", "AFIP", "Facturación electrónica: nuevo esquema de validación",
         "tax", "alta", 30, "Validación en tiempo real de comprobantes."),
    Norm("N-2026-052", "MTSS", "Teletrabajo: actualización de convenios",
         "labor", "baja", 120, "Registro de jornada en modalidad remota."),
]
