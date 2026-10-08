# Final reproducibility audit — 2026-10-09

- Notebook: 22 cells (11 executable), **one primary notebook**.
- Full local execution with nbclient: **PASS**, without skipping cells.
- Frozen A+B data integrity: 2,000 intended rows and 100 unique questions; checks PASS.
- Group-disjoint predictive split: 75 training questions and 25 held-out questions.
- Figure outputs: **19 PNG and 19 SVG**, plus response-length PDF.
- Colab final gallery asserts and displays all 19 PNGs.
- Feature importance: **horizontal ±1 SD bars** over 8 permutation repeats; notebook generates and saves exactly this version.
- Figure generation: 17 descriptive + 2 supervised diagnostics = 19 total.
- Reports preserved: 5-page technical report and 2-page non-technical report (DOCX/PDF).
- Colab itself is not executed in this environment; user must verify Restart and Run All in Colab.
- Official cohort portal requirements must be independently checked by the student.

The visual gallery may show 19 figures but only a subset are displayed at their generation cells; this is intentional.
