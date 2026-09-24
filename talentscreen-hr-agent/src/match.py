"""Matching explicable: skills 60%, experiencia 25%, salario 15%."""
from __future__ import annotations

from .jd import JobDescription
from .candidate import Candidate


def match_score(jd: JobDescription, c: Candidate) -> tuple[float, dict]:
    covered = {s: w for s, w in jd.required_skills.items() if s in c.skills}
    skill_score = sum(covered.values()) / jd.total_skill_weight

    exp_score = min(1.0, c.years_experience / max(jd.min_years * 2, 1))

    if jd.salary_min <= c.salary_expectation <= jd.salary_max:
        salary_score = 1.0
    elif c.salary_expectation < jd.salary_min:
        salary_score = 0.8   # dentro o debajo de banda: aceptable
    else:
        over = (c.salary_expectation - jd.salary_max) / max(jd.salary_max, 1)
        salary_score = max(0.0, 1.0 - over * 2)

    total = 0.60 * skill_score + 0.25 * exp_score + 0.15 * salary_score
    missing = [s for s in jd.required_skills if s not in c.skills]
    return round(total, 4), {"skill_score": round(skill_score, 3),
                             "missing_skills": missing,
                             "exp_score": round(exp_score, 3),
                             "salary_score": round(salary_score, 3)}
