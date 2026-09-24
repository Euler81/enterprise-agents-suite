# Postulacion — Desarrollo Spring Camp (Taligent)

**Repo principal:** <link al repo portfolio o a carterax-agent>

## Que construi?

Una suite de 9 agentes de IA enterprise en Python, cada uno resolviendo un
dolor real de negocio (cobranzas, seguros, retencion, compliance, compras,
credito, inventario, screening de RRHH, energia) con el mismo ciclo de
trabajo Planner -> Execute -> Verify que muestra Taligent, y con el patron
que considero clave en agentes enterprise: **autonomia acotada por politicas
de negocio**.

Cada agente tiene: motor de politicas con topes duros, verificacion antes
de actuar, escalado auditado a humanos, trazabilidad completa del ciclo,
datos sinteticos, demo end-to-end y suite de tests — incluyendo tests que
demuestran que el agente NO puede exceder su mandato.

## Proyecto destacado: CarteraX (cobranzas inteligentes)

Agente que negocia planes de pago con deudores: scoring de riesgo
explicable, politica de concesiones (tope de descuento, cuotas maximas,
primera cuota minima, valor presente recuperado minimo), deteccion de
hostilidad con escalado a gestores humanos y analytics de campana
(recovery rate, horas humanas ahorradas, ahorro estimado en USD).

Demo sobre 300 deudores sinteticos: ~100 acuerdos cerrados autonomamente,
~130 escalados correctamente por hostilidad o falta de acuerdo, reporte
CSV auditado.

## Por que este proyecto

Lo que mas me interesa del camp es exactamente lo que ya estuve
construyendo: agentes que **negocian y ejecutan con limites reales de
negocio**, no demos de una sola llamada a un LLM. Quiero llevar estos
prototipos a produccion con mentores que ya lo hicieron en una de las
empresas mas grandes del pais, y medir el salto que falta: LLMs en la
interaccion, persistencia, evaluacion continua y despliegue real.

**Repo/demo:** <link> - Python 3.10+, stdlib, tests en verde.
