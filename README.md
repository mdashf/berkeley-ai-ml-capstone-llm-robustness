# M24 Capstone — authoritative GitHub / UC Berkeley package

**Primary notebook:** `notebooks/M24_Capstone_FINAL.ipynb` (22 cells). The separate ESWA journal project is excluded.

## Scope
Frozen A+B: 100 distinct questions, 4 models, 5 conditions, 2 benchmarks, 2,000 intended responses. Blocks C+D are reserved.

## Google Colab
1. Open `notebooks/M24_Capstone_FINAL.ipynb` in Colab.
2. Runtime → Restart session and run all. When prompted, upload **the complete `M24_UCB_GITHUB_AUDITED_20261009.zip`**.
3. Confirm `Generated figure count: 19` and the final gallery of 19 figures.
4. Download `M24_Colab_Regenerated_Figures.zip` from Colab Files and replace local `figures/` contents before GitHub Desktop commit.
5. Review the technical and non-technical reports in `docs/`; confirm the cohort portal's submission requirements separately.

## Statistical cautions
- The 2,000 rows are repeated observations of 100 distinct questions, not 2,000 independent samples.
- Unacquired, unparseable, and incorrect observations are not interchangeable; strict end-to-end scores count unsuccessful intended rows as failures.
- `Fig_Feature_Importance` error bars show ±1 SD across 8 permutation repeats, **not** 95% CIs. Negative importances do not imply causation.
- This package does not claim PAMS superiority or include C+D data.

## Deliverables
- `notebooks/`: one primary analysis notebook, all 19 figures visible after Run All
- `figures/`: 19 PNG and 19 SVG files, plus response-length PDF
- `docs/`: technical (5-page) and non-technical (2-page) reports in DOCX and PDF
- `data/`: frozen grid and derived tables
- `scripts/`: standalone descriptive plotting and response-length scripts
- `provenance/`: source and output file checksums
