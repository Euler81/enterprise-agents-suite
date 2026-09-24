# 💼 CarteraX — Agente Autónomo de Recupero de Cartera

Agente de IA enterprise que **negocia planes de pago con deudores de manera
autónoma, segura y medible**. Combina scoring de riesgo, un motor de políticas
de negocio, estrategia de negociación con **autonomía acotada**, generación de
comunicaciones multi-canal y escalado inteligente a humanos.

> Proyecto demo para el **Desarrollo Spring Camp — Taligent 2026**.

## 🎯 El problema de negocio (real)

En LatAm, las carteras vencidas representan el **3–8% de la facturación** de
empresas de servicios, fintechs y bancos. Los procesos de cobranza actuales:

- Son **genéricos**: mismos mensajes para todos los deudores.
- **Escalan tarde** a humanos, quemando casos recuperables.
- **No negocian**: ofrecen un plan fijo; si no entra, llaman.
- No miden el **costo de recuperación vs. valor recuperado**.

**CarteraX** ataca los 4 puntos: prioriza por scoring, negocia dentro de
políticas, escala a tiempo y reporta ROI de la campaña.

## 🧠 Cómo funciona (ciclo Planner → Execute → Verify)

```
                    ┌──────────────────────────────┐
  Cartera vencida → │ 1. SCORING (priorización)    │
                    └──────────────┬───────────────┘
                                   ▼
                    ┌──────────────────────────────┐
                    │ 2. POLICY ENGINE (límites)   │ ← descuento máx.,
                    └──────────────┬───────────────┘    cuotas máx., antigüedad
                                   ▼
                    ┌──────────────────────────────┐
                    │ 3. PLANNER (estrategia)      │
                    └──────────────┬───────────────┘
                                   ▼
              ┌─────────── 4. NEGOTIATION LOOP ──────────┐
              │  Agente ofrece → Deudor responde         │
              │  Ajustar oferta (dentro de política)     │
              │  Sentimiento negativo → ESCALAR a humano │
              └──────────────┬───────────────────────────┘
                             ▼
                    ┌──────────────────────────────┐
                    │ 5. VERIFIER (¿cierra? ¿ROI?) │
                    └──────────────┬───────────────┘
                                   ▼
                    ┌──────────────────────────────┐
                    │ 6. OUTREACH + ANALYTICS      │
                    └──────────────────────────────┘
```

## 🚀 Quickstart (sin API key, 100% funcional)

```bash
git clone https://github.com/<tu-usuario>/carterax-agent.git
cd carterax-agent

# 1. Generar cartera sintética realista (300 deudores)
python scripts/generate_data.py

# 2. Correr la campaña de cobranza end-to-end
python examples/demo_campaign.py

# 3. Correr los tests
python -m unittest discover tests -v
```

Salida esperada: plan de pago negociado por deudor, decisiones de escalado,
métricas de recuperación y reporte CSV en `output/campaign_report.csv`.

## 🧩 Módulos

| Módulo | Responsabilidad |
|---|---|
| `src/scoring.py` | Score de riesgo 0–100 (probabilidad de recuperar) y prioridad |
| `src/policies.py` | Motor de políticas: máx. descuento, máx. cuotas, umbrales de antigüedad |
| `src/negotiation.py` | Loop de negociación con utilidad del deudor y concesiones acotadas |
| `src/outreach.py` | Generador de mensajes email/SMS/WhatsApp personalizados por perfil |
| `src/escalator.py` | Detección de sentimiento/hostilidad y reglas de escalado a humano |
| `src/analytics.py` | Métricas de campaña: recovery rate, ROI, ahorro vs. gestión humana |
| `src/agent.py` | Orquestador del ciclo completo |

## ⚖️ Autonomía acotada (lo que lo hace enterprise)

El agente **nunca** puede:
- Ofrecer descuento mayor al `MAX_DISCOUNT` configurado por segmento.
- Exceder `MAX_INSTALLMENTS` ni aceptar primera cuota < `MIN_FIRST_PAYMENT`.
- Continuar negociando con un deudor hostil (escalación inmediata).
- Cerrar un plan con valor presente recuperado < `MIN_RECOVERY_PV`.

Cada decisión queda auditada en el `trace` con la política que la habilitó.

## 📁 Estructura

```
carterax-agent/
├── src/                 # Módulos del agente
├── scripts/generate_data.py   # Generador de cartera sintética
├── examples/demo_campaign.py  # Demo end-to-end
├── tests/test_carterax.py     # Suite de tests
├── docs/ARCHITECTURE.md       # Diseño técnico
└── docs/BUSINESS_CASE.md      # Caso de negocio y ROI
```

## 🔌 Extensiones reales (roadmap)

- [ ] Conector LLM para mensajes naturales (OpenAI/Anthropic)
- [ ] Integración con WhatsApp Business API / Twilio
- [ ] Modelo de scoring entrenado (XGBoost sobre historial real)
- [ ] API FastAPI + dashboard Streamlit para el equipo de cobranza
- [ ] Aprendizaje de políticas por bandit (qué descuento funciona por segmento)

## 📄 Licencia

MIT — ver [LICENSE](LICENSE).
