# 🛒 ProcureBot — Agente Autónomo de Compras y Negociación

Agente enterprise que **arma solicitudes de cotización, compara proveedores
con scoring multi-criterio, negocia contraofertas dentro de mandato y
adjudica compras con trazabilidad completa**.

> Proyecto para el **Desarrollo Spring Camp — Taligent 2026**.

## 🎯 Problema de negocio

El 30-50% del costo de una empresa es compras, pero la mayoría de las áreas
compran por costumbre: mismo proveedor, sin comparar, sin negociar.
ProcureBot estandariza: RFQ automática, comparación ponderada
(precio 50%, plazo 25%, calidad 25%) y **negociación automática** con el
finalista para capturar ahorro adicional.

## 🧠 Ciclo

```
Necesidad ─▶ PLANNER: generar RFQ con especificaciones
          ─▶ EXECUTE: recolectar cotizaciones → scoring multi-criterio
          ─▶ NEGOTIATE: contraoferta al finalista (piso de proveedor)
          ─▶ VERIFY: ¿ahorro ≥ umbral y scoring sin empate? → ADJUDICAR
                      si no → ESCALAR a compras
```

## 🚀 Quickstart

```bash
git clone https://github.com/<tu-usuario>/procurebot-agent.git
cd procurebot-agent
python examples/demo.py
python -m unittest discover tests -v
```

## ⚖️ Autonomía acotada

- Solo adjudica si el ahorro vs. presupuesto ≥ 3% y el score supera al
  segundo por más de 0.05 (sin empates).
- Nunca acepta una contraoferta sobre el precio original.
- Todo queda auditado en `trace`.

## 📁 Estructura

```
src/rfq.py        # Solicitud de cotización
src/quotes.py     # Proveedores y cotizaciones sintéticas
src/evaluate.py   # Scoring multi-criterio normalizado
src/negotiate.py  # Contraoferta y simulador de proveedor
src/agent.py      # Orquestador + verificador
examples/demo.py
tests/test_procurebot.py
```

## 🔌 Roadmap

- [ ] Scrapers/APIs reales de marketplaces (Mercado Libre, Amazon Business)
- [ ] LLM para redactar RFQs técnicas
- [ ] Estrategia de negociación aprendida (históricos de proveedores)
- [ ] Integración ERP (SAP/Oracle)

## 📄 Licencia

MIT — ver [LICENSE](LICENSE).
