# 🧑‍💼 TalentScreen — Agente de Screening con Auditoría de Sesgo

Agente enterprise que **screenea candidatos contra un job description con
matching explicable** (skills ponderadas, experiencia, fit salarial), arma
shortlists y —lo más importante— **audita cada decisión por impacto adverso
entre grupos demográficos**.

> Proyecto para el **Desarrollo Spring Camp — Taligent 2026**.

## 🎯 Problema de negocio

El screening inicial es el cuello de botella del recruiting (200+ CVs por
puesto) y una de las fuentes de riesgo legal más grandes: procesos opacos
producen discriminación sistemática sin intención. Las empresas reguladas
necesitan **decisiones explicables Y auditadas**.

**TalentScreen** matchea con reason codes y corre una auditoría de sesgo
estadística (adverse impact ratio) sobre cada tanda de decisión.

## 🧠 Ciclo

```
JD + CVs ─▶ PLANNER: extraer skills y requisitos
         ─▶ EXECUTE: match score 0-1 explicable (skills 60%, experiencia 25%, salario 15%)
         ─▶ VERIFY: shortlist ≥ 0.70 | hold 0.40-0.70 | reject < 0.40
         ─▶ AUDIT: adverse impact ratio por grupo demográfico → flag si < 0.80
```

## 🚀 Quickstart

```bash
git clone https://github.com/<tu-usuario>/talentscreen-hr-agent.git
cd talentscreen-hr-agent
python scripts/generate_candidates.py
python examples/demo.py
python -m unittest discover tests -v
```

## ⚖️ Autonomía acotada

- Nunca rechaza: todo candidato < 0.40 queda en "hold" si la auditoría de
  sesgo está activada para su grupo.
- Toda decisión lleva reason codes (skills faltantes, seniority, salario).
- La auditoría corre SIEMPRE, aunque el matching esté limpio.

## 📁 Estructura

```
src/jd.py          # Job description con skills ponderadas
src/candidate.py   # Candidato
src/match.py       # Matching explicable
src/bias.py        # Auditoría de impacto adverso
src/agent.py       # Orquestador + verificador
scripts/generate_candidates.py
examples/demo.py
tests/test_talentscreen.py
```

## 🔌 Roadmap

- [ ] Parser de CV real (PDF/LinkedIn)
- [ ] Embeddings semánticos para skills sinónimas
- [ ] Integración ATS (Greenhouse/Lever)
- [ ] Reporte de adverse impact para legal/RRHH

## 📄 Licencia

MIT — ver [LICENSE](LICENSE).
