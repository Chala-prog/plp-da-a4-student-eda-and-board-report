# PLP Data Analytics · Week 4 — Student EDA & Board Report

Two engagements in one repository.

| Engagement | Status | Files |
|---|---|---|
| 1 · County education office — who needs learner support? | ✅ Complete | `student_performance_eda.ipynb`, `figures/`, `student_performance.csv` |
| 2 · Duka Electronics board — one-page visual report and live dashboard | ✅ Complete | `reports/board_report.png` / `.pdf`, `dashboard.html`, `build_report.py`, `build_dashboard.py` |

## Engagement 1 — headline findings (1,200 students, seed 55)
- **Study hours is the strongest factor:** r = 0.70 with average score; about **2.1 points per extra weekly hour** (R² = 0.50).
- **99 learners (8.3%) are At Risk** (average < 60); they study a median 2.1 h/week vs 4.5 h overall and attend 69% of days vs 82%.
- **Public schools carry the risk:** 10.9% At Risk vs 1.5% in private schools; 94 of 99 At Risk learners are in public schools. The 5.5-point school-type gap persists in every attendance band and study-hour quartile.
- **County and gender are weak targeting criteria:** Nairobi has the highest At Risk share (9.2%) but a chi-square test (1.29 vs 11.07 needed) shows the county spread is consistent with chance.
- **Recommendation:** target by behaviour (study ≤ 2.9 h/week or attendance ≤ 70%: 490 learners, 88.9% of the At Risk group), prioritising public schools.

See the notebook's Task 9 for the five insights, two recommendations and the Limitations paragraph.

## Engagement 2 — Duka board report (H1 2026, Week 3 data)
**One-page report** (`reports/board_report.png`, also `.pdf`): a tall, phone-width page with action titles, one highlight colour and direct labels. **The story:** H1 revenue was **KES 71.8M** from 1,000 orders, but **Q2 was flat on Q1 (−0.3%)**; **laptops and tablets bring 85% of revenue**; **Mombasa (−25%) and Nakuru (−27%) fell in Q2** while Eldoret (+50%) and phone orders (+18.5%, biggest baskets) grew.
**H2 recommendations:** (1) protect laptop and tablet supply; (2) diagnose Mombasa and Nakuru now; (3) pilot phone orders and Eldoret's momentum before scaling.
**Caveats stated on the page:** branch-quarter figures rest on 51–202 orders each; no cost, margin or target data.

**Live dashboard** (`dashboard.html`): self-contained interactive page with filters for branch, channel, product and month range, KPI tiles and tap-to-filter bars. Open the file in any browser, or host it for free: on GitHub go to *Settings → Pages → Deploy from branch → main / (root)*, then share `https://chala-prog.github.io/plp-da-a4-student-eda-and-board-report/dashboard.html`.

Rebuild: `python generate_data.py && python build_report.py && python build_dashboard.py`

## Run it
```bash
pip install -r requirements.txt
python generate_data.py        # seed 55 -> student_performance.csv; seed 2026 -> duka_sales.csv
jupyter nbconvert --to notebook --execute --inplace student_performance_eda.ipynb   # regenerates figures/
```

## Structure
```
generate_data.py                  both generators, unchanged (seed 55 students, seed 2026 Duka)
student_performance.csv           generated data
student_performance_eda.ipynb     Tasks 1-9, answers written in Markdown under each section
figures/                          six charts saved by the notebook (pandas .plot())
duka_sales.csv                    Week 3 sales data
build_report.py                   builds reports/board_report.png and .pdf
build_dashboard.py                builds dashboard.html
reports/                          one-page board report (PNG + PDF)
dashboard.html                    interactive dashboard
requirements.txt
```
