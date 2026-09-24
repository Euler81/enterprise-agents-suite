# 🏦 UnderwriteAI — Agente de Crédito para PyMEs

Agente enterprise de **evaluación crediticia para pymes usando datos
alternativos** (facturación, flujo de comprobantes, antigüedad, comportamiento
de pagos), con scoring explicable, límites de exposición por política y
decisiones auditables: aprobar / derivar / declinar.

> Proyecto para el **Desarrollo Spring Camp — Taligent 2026**.

## 🎯 Problema de negocio

Las PyMEs representan ~99% de las empresas en Argentina pero el crédito
bancario llega a pocas: no tienen historial crediticio tradicional. Las
fintech que sí las evalúan hoy usan procesos manuales o scores de caja negra.

**UnderwriteAI** evalúa con datos alternativos **explicables**: cada decisión
incluye los motivos exactos que la produjeron (reason codes), listos para
regulatoria y para el cliente.

## 🧠 Ciclo

```
Solicitud ─▶ PLANNER: extraer features de la solicitud
          ─▶ EXECUTE: score explicable 0-1000 con reason codes
          ─▶ VERIFY: score ≥ umbral del producto Y exposición ≤ límite
                ├─ PASS  → APROBAR con monto y tasa sugerida
                ├─ ZONA GRIS → DERIVAR a analista
                └─ FAIL  → DECLINAR con motivos
```

## 🚀 Quickstart

```bash
git clone https://github.com/<tu-usuario>/underwriteai-credit-agent.git
cd underwriteai-credit-agent
python scripts/generate_applicants.py
python examples/demo.py
python -m unittest discover tests -v
```

## ⚖️ Autonomía acotada

- Exposición máxima = 20% de la facturación anual del solicitante.
- Scores 400-600 nunca se aprueban solos: derivan a analista humano.
- Cada decisión incluye reason codes auditables.

## 📁 Estructura

```
src/applicant.py    # Solicitud PyME
src/score.py        # Scoring explicable 0-1000
src/policy.py       # Límites de producto y exposición
src/decision.py     # Orquestador + reason codes
scripts/generate_applicants.py
examples/demo.py
tests/test_underwrite.py
```

## 🔌 Roadmap

- [ ] Open Banking / data de AFIP (facturación real)
- [ ] Modelo entrenado con historial de default
- [ ] Pricing de tasa por riesgo (risk-based pricing)
- [ ] Monitoreo post-origination (early warning)

## 📄 Licencia

MIT — ver [LICENSE](LICENSE).
