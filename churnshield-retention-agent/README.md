# 📉 ChurnShield — Agente de Retención de Clientes

Agente enterprise que **detecta clientes en riesgo de fuga, calcula su LTV y
negocia ofertas de retención que siempre son rentables** para la empresa.
Cada oferta se verifica contra el margen antes de lanzarse; si el cliente es
demasiado valioso o la oferta no cierra, escala al equipo comercial.

> Proyecto para el **Desarrollo Spring Camp — Taligent 2026**.

## 🎯 Problema de negocio

En telecom/fintech/SaaS, retener un cliente cuesta **5-7x menos** que
conseguir uno nuevo, pero las campañas de retención suelen ser manuales,
genéricas o peor: **regalan descuentos a clientes que se quedaban solos**.
Eso es margen quemado.

**ChurnShield** solo ofrece descuento cuando el valor esperado de retener
supera su costo.

## 🧠 Ciclo Planner → Execute → Verify

```
Cliente ─▶ 1. PLANNER: churn_score (señales de uso, tickets, oferta competencia)
        ─▶ 2. EXECUTE: LTV + selección de oferta dentro de catálogo
        ─▶ 3. VERIFY: EV(retener) > costo de la oferta ? ¿churn muy alto?
              ├─ PASS  → LANZAR oferta personalizada
              ├─ NO RENTABLE → oferta menor o campaña pasiva
              └─ VIP EN RIESGO → ESCALAR a account manager
```

## 🚀 Quickstart

```bash
git clone https://github.com/<tu-usuario>/churnshield-retention-agent.git
cd churnshield-retention-agent
python scripts/generate_customers.py
python examples/demo.py
python -m unittest discover tests -v
```

## ⚖️ Autonomía acotada

- Descuento máximo: el menor entre `MAX_DISCOUNT` y `margen × probabilidad de permanencia`.
- Clientes enterprise con churn_score > 0.7 nunca se tratan por agente: escalan.
- Ninguna oferta sale sin pasar el verificador de rentabilidad.

## 📁 Estructura

```
src/signals.py       # Señales → churn_score 0-1
src/ltv.py           # LTV y catálogo de ofertas
src/retention.py     # Motor de retención (cycle completo)
src/campaign.py      # Campaña + analytics
scripts/generate_customers.py
examples/demo.py
tests/test_churnshield.py
```

## 🔌 Roadmap

- [ ] LLM para redactar mensajes de retención personalizados
- [ ] Modelo de churn entrenado (survival analysis)
- [ ] Integración CRM (Salesforce/HubSpot)
- [ ] Test A/B automático de ofertas por segmento

## 📄 Licencia

MIT — ver [LICENSE](LICENSE).
