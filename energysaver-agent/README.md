# ⚡ EnergySaver — Agente de Auditoría Energética y Negociación Tarifaria

Agente enterprise que **audita el consumo eléctrico de una empresa, detecta
anomalías (picos, fugas, mala clasificación tarifaria) y arma un dossier de
negociación con la distribuidora**: reclamos por cargos, propuesta de
reclasificación tarifaria y oportunidades de demanda response.

> Proyecto para el **Desarrollo Spring Camp — Taligent 2026**.

## 🎯 Problema de negocio

La energía es un costo creciente (y el mercado eléctrico argentino es de los
más complejos de LatAm: tarifas segmentadas, subsidios, potencia contratada,
penalidades). Las empresas medianas **no auditan su factura**: pagan penalidades,
potencia de más y picos que podrían evitar.

**EnergySaver** lee el consumo mensual, encuentra lo que no cierra y genera
el expediente de negociación con la distribuidora.

## 🧠 Ciclo

```
Consumo 24m ─▶ PLANNER: perfil de consumo (base, pico, variabilidad)
            ─▶ EXECUTE: detección de anomalías + estimación de ahorro
            ─▶ VERIFY: ¿ahorro estimado > costo de gestión?
                  ├─ PASS → DOSSIER DE NEGOCIACIÓN con argumentos
                  └─ FAIL → REPORTE estándar (seguimiento anual)
```

## 🚀 Quickstart

```bash
git clone https://github.com/<tu-usuario>/energysaver-agent.git
cd energysaver-agent
python scripts/generate_consumption.py
python examples/demo.py
python -m unittest discover tests -v
```

## 📁 Estructura

```
src/meter.py       # Serie de consumo mensual (kWh)
src/anomaly.py     # Detección estadística de anomalías
src/dossier.py     # Generador de dossier de negociación
src/agent.py       # Orquestador + verificador
scripts/generate_consumption.py
examples/demo.py
tests/test_energysaver.py
```

## 🔌 Roadmap

- [ ] Datos reales: facturas PDF / medidores inteligentes
- [ ] Detección de fugas por correlación horaria
- [ ] Integración con plataformas de demanda response (Mercado Eléctrico)
- [ ] Benchmarking sectorial de consumo

## 📄 Licencia

MIT — ver [LICENSE](LICENSE).
