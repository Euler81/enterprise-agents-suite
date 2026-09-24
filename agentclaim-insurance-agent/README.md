# 🛡️ AgentClaim — Agente Autónomo de Liquidación de Siniestros

Agente enterprise que **liquida siniestros de seguros de forma autónoma y
auditada**: verifica cobertura contra la póliza, puntúa riesgo de fraude,
calcula la reserva (con deducible y depreciación) dentro de su mandato
económico, y liquida o escala a un liquidador humano con ficha completa.

> Proyecto para el **Desarrollo Spring Camp — Taligent 2026**.

## 🎯 Problema de negocio

Las aseguradoras pierden dinero por dos lados: **leakage** (sobrepagos por
liquidaciones mal calculadas) y **fraude** que pasa desapercibido en la
primera revisión. Además, el 70% de los siniestros menores son rutinarios:
cada uno atado por un liquidador cuesta USD 15–40 en tiempo.

**AgentClaim** liquida el caso rutinario en segundos y escala a humanos
exactamente los casos que lo necesitan.

## 🧠 Ciclo Planner → Execute → Verify

```
Siniestro ─▶ 1. PLANNER: verificar póliza y cobertura
           ─▶ 2. EXECUTE: scoring de fraude + cálculo de reserva
           ─▶ 3. VERIFY: ¿reserva dentro del mandato? ¿fraude bajo umbral?
                 ├─ PASS  → LIQUIDAR (documento + trazabilidad)
                 ├─ FRAUDE→ ESCALAR a investigación
                 └─ MONTO → ESCALAR a liquidador senior
```

## 🚀 Quickstart

```bash
git clone https://github.com/<tu-usuario>/agentclaim-insurance-agent.git
cd agentclaim-insurance-agent
python scripts/generate_claims.py     # 200 siniestros sintéticos
python examples/demo.py               # liquidación completa + métricas
python -m unittest discover tests -v  # tests
```

## ⚖️ Autonomía acotada

El agente nunca puede liquidar más de `MAX_AUTO_SETTLE`, ni aprobar un caso
con `fraud_score >= 0.60`, ni ignorar el período de carencia de la póliza.
Todo queda en `trace`.

## 📁 Estructura

```
src/policy.py       # Póliza + verificación de cobertura
src/fraud.py        # Scoring explicable de fraude
src/reserve.py      # Reserva: deducible + depreciación
src/liquidator.py   # Orquestador del ciclo
scripts/generate_claims.py
examples/demo.py
tests/test_agentclaim.py
```

## 🔌 Roadmap

- [ ] LLM para redactar el documento de liquidación en lenguaje natural
- [ ] OCR de denuncias y presupuestos de talleres
- [ ] Modelo de fraude entrenado ( gradient boosting sobre siniestralidad real)
- [ ] API FastAPI para integrarse al core de la aseguradora

## 📄 Licencia

MIT — ver [LICENSE](LICENSE).
