# 📦 StockGuard — Agente de Gestión de Inventarios y Reabastecimiento

Agente enterprise que **monitorea el catálogo, pronostica demanda, calcula
puntos de reorden con stock de seguridad y emite órdenes de compra
automatizadas** dentro de un mandato económico. Lo que supera el mandato
escala al área de compras.

> Proyecto para el **Desarrollo Spring Camp — Taligent 2026**.

## 🎯 Problema de negocio

El inventario es el activo más mal administrado de la industria: quiebres de
stock (ventas perdidas) conviven con sobreinventario (capital congelado).
Las pymes lo hacen "a ojo"; las grandes con ERP no optimizan por SKU.

**StockGuard** decide por SKU: ¿reponer, cuánto y con qué urgencia? — y mide
el capital liberado.

## 🧠 Ciclo

```
Catálogo ─▶ PLANNER: pronóstico de demanda por SKU
         ─▶ EXECUTE: punto de reorden = demanda×lead time + stock seguridad
         ─▶ VERIFY: ¿valor de la orden ≤ mandato? ¿stock proyectado sano?
               ├─ PASS  → ORDEN DE COMPRA automática
               └─ FAIL  → ESCALAR a compras con análisis completo
```

## 🚀 Quickstart

```bash
git clone https://github.com/<tu-usuario>/stockguard-inventory-agent.git
cd stockguard-inventory-agent
python scripts/generate_catalog.py
python examples/demo.py
python -m unittest discover tests -v
```

## ⚖️ Autonomía acotada

- `MAX_AUTO_ORDER`: ninguna orden automática supera el mandato configurado.
- Nunca ordena si el stock proyectado supera 90 días de demanda (sobreinventario).

## 📁 Estructura

```
src/product.py      # SKU del catálogo
src/forecast.py     # Pronóstico determinístico de demanda
src/reorder.py      # Punto de reorden + sizing de orden
src/agent.py        # Orquestador + verificador + escalado
scripts/generate_catalog.py
examples/demo.py
tests/test_stockguard.py
```

## 🔌 Roadmap

- [ ] Pronóstico ML (serie temporal por SKU)
- [ ] Integración ERP / API de proveedores
- [ ] Multi-almacén con transferencias
- [ ] Optimización conjunta (joint replenishment)

## 📄 Licencia

MIT — ver [LICENSE](LICENSE).
