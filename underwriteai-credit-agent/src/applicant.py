"""Solicitud de crédito PyME."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Applicant:
    applicant_id: str
    company: str
    annual_revenue: float        # facturación anual
    years_in_business: int
    monthly_invoices: int        # volumen de comprobantes/mes (dato alternativo)
    bank_debt_ratio: float       # 0-1, endeudamiento bancario actual
    bounced_payments_12m: int    # cheques/rechazos en 12 meses
    requested_amount: float
