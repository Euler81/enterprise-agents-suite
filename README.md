# 🧠 Agentes Enterprise — Portfolio Taligent Spring Camp 2026

Suite de **9 agentes de IA enterprise** construidos en Python puro, todos
siguiendo el ciclo de trabajo **Planner → Execute → Verify** con el patron
que diferencia un agente serio de un chatbot: **autonomia acotada por
politicas de negocio, verificacion antes de actuar y escalado auditado a
humanos**.

Cada proyecto resuelve un **dolor real de negocio** con KPIs medibles.
Ninguno usa frameworks de agents: el ciclo se implementa a mano para que
cada decision sea entendible, testeable y auditable linea por linea.

## Los 9 agentes

| # | Proyecto | Dominio | Que hace | Autonomia acotada por |
|---|----------|---------|----------|----------------------|
| 1 | [CarteraX](./carterax-agent) | Cobranzas | Negocia planes de pago con deudores de forma autonoma | Topes de descuento/cuotas, escalado por hostilidad, valor presente minimo |
| 2 | [AgentClaim](./agentclaim-insurance-agent) | Seguros | Liquida siniestros rutinarios en segundos | Mandato economico, umbral de fraude, periodos de carencia |
| 3 | [ChurnShield](./churnshield-retention-agent) | Retencion | Detecta churn y negocia ofertas de retencion rentables | Oferta solo si EV(retener) > costo; VIP criticos escalan |
| 4 | [ComplianceWatch](./compliancewatch-agent) | Regulatorio | Traduce normas nuevas a impacto operativo | Normas criticas o <15 dias escalan a legal |
| 5 | [ProcureBot](./procurebot-agent) | Compras | RFQ, comparacion multi-criterio y contraoferta | Ahorro minimo, sin empates tecnicos |
| 6 | [UnderwriteAI](./underwriteai-credit-agent) | Credito PyME | Evalua credito con datos alternativos explicables | Exposicion <=20% facturacion; zona gris deriva a analista |
| 7 | [StockGuard](./stockguard-inventory-agent) | Inventario | Reabastecimiento por SKU con stock de seguridad | Mandato de orden, tope de sobreinventario |
| 8 | [TalentScreen](./talentscreen-hr-agent) | RRHH | Screening explicable **con auditoria de sesgo estadistica** | Nunca rechaza: hold revisable; adverse impact ratio <0.80 dispara flag |
| 9 | [EnergySaver](./energysaver-agent) | Energia | Auditoria de consumo y dossier de negociacion tarifaria | Solo gestiona si ahorro > costo de gestion |

## El patron comun (por que importa)

```
ENTRADA --> PLANNER  (interpretar el caso y armar plan/estrategia)
        --> EXECUTE  (actuar con tools/scoring, siempre acotado por POLICY ENGINE)
        --> VERIFY   (validar contra politicas de negocio)
              |- PASS  --> actuar + trazabilidad completa
              +- FAIL  --> re-planificar o ESCALAR a humano con ficha del caso
```

Tres principios en los 9 proyectos:

1. **Ninguna decision sin verificacion.** El agente propone; el motor de
   politicas dispone. Los limites son duros y configurables por compliance.
2. **Trazabilidad total.** Cada ciclo deja un `trace` auditable: que se
   ofrecio, que respondio el contraparte, que politica habilito la decision.
3. **Determinismo demostrable.** Tests unitarios de cada verificador y cada
   limite: se prueba que el agente *no puede* exceder su mandato.

## Como correr cualquiera

```bash
cd <proyecto>
python scripts/generate_*.py    # datos sinteticos (donde aplica)
python examples/demo.py         # demo end-to-end con metricas
python -m unittest discover tests -v
```

Cero dependencias obligatorias: **stdlib de Python 3.10+**.

## Decisiones tecnicas

| Decision | Motivo |
|---|---|
| Sin frameworks de agents | El valor esta en entender el ciclo, no en ocultarlo |
| Scoring explicable (reglas) | Versionable a ML real; auditable por regulatoria |
| Simuladores deterministas del contraparte | Demos reproducibles sin API keys ni costos |
| `PolicyEngine` como frontera dura | Separacion clara "lo que el agente quiere" vs "lo que la empresa permite" |
| Tests de los limites, no solo del happy path | Se testea que el agente NO puede romper politica |

## KPIs que reportan las demos

Recovery rate (PV) - agreement rate - leakage evitado - EV de retencion -
tiempo de liquidacion - adverse impact ratio - ahorro de compras - horas
humanas liberadas - ahorro energetico identificado.

## Roadmap comun (produccion)

- [ ] Capa LLM para interaccion en lenguaje natural (OpenAI/Anthropic)
- [ ] Persistencia y event log (Postgres)
- [ ] APIs REST (FastAPI) + dashboards (Streamlit)
- [ ] Modelos entrenados sobre datos reales por dominio
- [ ] Despliegue con evaluacion continua de politicas

## Licencia

MIT - ver [LICENSE](LICENSE).
