# ⚖️ ComplianceWatch — Agente de Cumplimiento Regulatorio

Agente enterprise que **monitorea cambios normativos, los traduce a impacto
operativo sobre los procesos de la empresa y genera un plan de acción con
deadlines**. Lo crítico escala a legal/compliance humano con ficha completa.

> Proyecto para el **Desarrollo Spring Camp — Taligent 2026**.

## 🎯 Problema de negocio

El compliance es uno los mayores costos ocultos de las empresas reguladas
(finanzas, salud, telecom): equipos enteros leyendo boletines oficiales para
detectar qué norma nueva los afecta, con riesgo de multas por incumplimiento
tardío. En Argentina: BCRA, CNV, AFIP, AAIP (datos personales), entre otros.

**ComplianceWatch** lee la norma, la mapea contra el inventario de procesos
internos y produce: qué procesos se ven afectados, quién es el owner, cuánto
tiempo queda y qué tan grave es.

## 🧠 Ciclo

```
Norma nueva ─▶ PLANNER: interpretar área, severidad, deadline
            ─▶ EXECUTE: cruzar contra inventario de procesos → impacto
            ─▶ VERIFY: ¿crítica o <15 días? → ESCALAR a compliance
                        si no → reporte de acción al owner del proceso
```

## 🚀 Quickstart

```bash
git clone https://github.com/<tu-usuario>/compliancewatch-agent.git
cd compliancewatch-agent
python examples/demo.py
python -m unittest discover tests -v
```

## 📁 Estructura

```
src/norms.py       # Base de normas y parser
src/inventory.py   # Inventario de procesos internos
src/impact.py      # Motor de mapeo norma → impacto
src/agent.py       # Orquestador + verificador + escalado
examples/demo.py
tests/test_compliance.py
```

## 🔌 Roadmap

- [ ] Scraper real de Boletín Oficial / CNV / BCRA
- [ ] LLM que resume la norma en obligaciones concretas
- [ ] Workflow de aceptación por el owner del proceso
- [ ] Matriz de riesgo regulatorio histórica

## 📄 Licencia

MIT — ver [LICENSE](LICENSE).
