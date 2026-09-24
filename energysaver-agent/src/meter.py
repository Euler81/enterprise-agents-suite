"""Serie de consumo mensual (kWh)."""
from __future__ import annotations

from dataclasses import dataclass

TARIFF_KWH_PRICE = 12.5    # $/kWh promedio (valor referencial)


@dataclass
class ConsumptionSeries:
    site: str
    monthly_kwh: list      # 24 meses
    contracted_kw: float

    @property
    def avg(self) -> float:
        return sum(self.monthly_kwh) / len(self.monthly_kwh)

    @property
    def std(self) -> float:
        m = self.avg
        return (sum((x - m) ** 2 for x in self.monthly_kwh) / len(self.monthly_kwh)) ** 0.5
