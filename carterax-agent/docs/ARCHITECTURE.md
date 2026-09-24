# Arquitectura — CarteraX

## Principios de diseño

1. **Autonomía acotada por políticas**: el negociador propone, el
   `PolicyEngine` dispone. Ninguna oferta sale al deudor sin pasar el chequeo.
2. **Determinismo auditado**: cada ronda de negociación queda en `trace`
   con la oferta, la respuesta y el sentimiento — trazabilidad enterprise.
3. **Separación de responsabilidades**: scoring, políticas, negociación,
   escalado, comunicación y analytics son módulos independientes con
   interfaces claras (testeables y reemplazables).
4. **Sin dependencias en el core**: corre con stdlib. LLMs, WhatsApp y
   ML entran como adaptadores posteriores.

## Flujo de una negociación

```
Debtor → risk_score() → tier P1/P2/P3
       → hostility >= 0.8 ? → ESCALATE inmediato
       → Negotiator:
           ronda 1: oferta inicial estricta (50% adelanto, 2 cuotas, 0% dto.)
           ronda n: concesión sistemática (+1 cuota → -10% adelanto → +10% dto.)
           cada oferta validada por PolicyEngine.check_offer()
           sentimiento < -0.5 ? → ESCALATE
           deudor acepta y oferta válida ? → AGREED + VERIFY final
           agota rondas ? → PASSIVE (campaña de mensajes)
```

## El Verifier (doble chequeo)

Incluso cuando el deudor acepta, el agente re-valida el plan cerrado contra
todas las políticas antes de darlo por finalizado. Si falla, escala.

## Reemplazos reales (roadmap técnico)

| Componente | Versión demo | Versión producción |
|---|---|---|
| DebtorSimulator | Utilidad determinística | LLM con perfil de cliente |
| Scoring | Reglas ponderadas | XGBoost sobre historial |
| Outreach | Plantillas | LLM + WhatsApp Business API |
| Persistencia | CSV | Postgres + event log |
