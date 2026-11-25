# PLP Data Analytics · Week 4 — Student EDA & Board Report

Two engagements in one repository.

| Engagement | Status | Files |
|---|---|---|
| 1 · County education office — who needs learner support? | ✅ Complete | `student_performance_eda.ipynb`, `figures/`, `student_performance.csv` |
| 2 · Duka Electronics board — one-page visual report and dashboard | ⏳ To be added | — |

## Engagement 1 — headline findings (1,200 students, seed 55)
- **Study hours is the strongest factor:** r = 0.70 with average score; about **2.1 points per extra weekly hour** (R² = 0.50).
- **99 learners (8.3%) are At Risk** (average < 60); they study a median 2.1 h/week vs 4.5 h overall and attend 69% of days vs 82%.
- **Public schools carry the risk:** 10.9% At Risk vs 1.5% in private schools; 94 of 99 At Risk learners are in public schools. The 5.5-point school-type gap persists in every attendance band and study-hour quartile.
- **County and gender are weak targeting criteria:** Nairobi has the highest At Risk share (9.2%) but a chi-square test (1.29 vs 11.07 needed) shows the county spread is consistent with chance.
- **Recommendation:** target by behaviour (study ≤ 2.9 h/week or attendance ≤ 70%: 490 learners, 88.9% of the At Risk group), prioritising public schools.

See the notebook's Task 9 for the five insights, two recommendations and the Limitations paragraph.

## Run it
```bash
pip install -r requirements.txt
python generate_data.py        # seed 55 -> student_performance.csv (1,200 rows)
jupyter nbconvert --to notebook --execute --inplace student_performance_eda.ipynb   # regenerates figures/
```

## Structure
```
generate_data.py                  course generator, unchanged (seed 55)
student_performance.csv           generated data
student_performance_eda.ipynb     Tasks 1-9, answers written in Markdown under each section
figures/                          six charts saved by the notebook (pandas .plot())
requirements.txt
```
