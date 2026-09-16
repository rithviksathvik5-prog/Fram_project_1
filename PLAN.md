# PLAN.md — execution order

Work through these phases in order. Each phase has a **GATE** that must pass before moving on.
Do not skip ahead. If a gate fails, fix it before continuing — every later result depends on it.

Mark phases done as you go.

---

## Phase 0 — Environment

- [x] Confirm Python is installed and report the version
- [x] Install anything missing: `pandas numpy statsmodels matplotlib jupyter ipykernel`
- [x] Confirm the notebook kernel points at the same environment those were installed into

**GATE 0:** a code cell running `import pandas, numpy, statsmodels, matplotlib` succeeds inside
a notebook, not just in a terminal.

If a notebook cell raises `ModuleNotFoundError` for something just installed, the notebook is on
a different kernel. Fix the kernel selection, don't reinstall.

---

## Phase 1 — Get the repo

- [x] Clone into the CURRENT folder, not a subfolder:

```
git clone https://github.com/Byomakesh-Debata/FIN-F414-FRAM-Lab1.git .
```

The trailing dot matters. If git refuses because the folder isn't empty, clone to a temp folder
and move the contents up one level.

**GATE 1:** all five `.ipynb` files, `README.md` and `data.docx` sit in the same folder as
`CLAUDE.md`, `PLAN.md`, `get_data.py` and `fama.pdf`. No nested `FIN-F414-FRAM-Lab1/` folder.

---

## Phase 2 — Download the data

- [x] Run `python get_data.py`
- [x] Read its output carefully

`get_data.py` is untested against the live site. If any URL 404s, the script names the file.
Download that one manually from the data library page, section "Developed Markets Factors and
Returns", and rename it per the table in `data.docx`.

**GATE 2:** `raw_data/` contains exactly eight CSVs with these exact names:

```
developed_3_factors.csv          japan_3_factors.csv
developed_momentum.csv           japan_momentum.csv
developed_25_size_bm.csv         japan_25_size_bm.csv
developed_25_size_momentum.csv   japan_25_size_momentum.csv
```

A single character wrong in a filename makes the next phase fail.

---

## Phase 3 — Clean the data

- [x] Open `00_clean_data.ipynb` and run every cell top to bottom
- [x] Read the summary printed after the last cell

**GATE 3 — the most important gate in this plan.** Every cleaned file must show:

- 245 observations
- date range November 1990 to March 2011
- zero missing values
- zero duplicate dates

Also confirm returns are in percent — values around 0.85, not 0.0085.

If any file is off, stop and fix it. Everything in all four notebooks inherits this. A units or
date error found here costs ten minutes; found on the 17th it costs the project.

---

## Phase 4 — Notebook 01 (Table 1, factor statistics)

Three code cells. Expect about an hour.

- [x] Task 1 — Global factor statistics. **STOP, we check the table.**
- [x] Task 2 — Japan factor statistics
- [x] Task 4 — the 8-panel figure, 4 rows x 2 columns

Tasks 3 and 5 are written-only, no code cell. Whoever is writing does those from the printed
output while coding continues.

**GATE 4:** two stat tables and one figure with all eight panels visible and titled.

---

## Phase 5 — Notebook 02 (Table 2, portfolio grids)

Two code cells. Expect under an hour.

- [x] Task 1 — excess returns for all four combinations. Subtract the market-specific `RF`
      column only, never `Mkt-RF`. **STOP, we check row counts are 245.**
- [x] Task 2 — 5x5 mean and std dev grids for each of the four

Task 3 is written-only.

**GATE 5:** eight 5x5 grids (mean and std dev for each of the four combinations), rows Small to
Big, columns Low to High or Losers to Winners.

---

## Phase 6 — Notebook 03 (Tables 3 and 4) — THE HARD ONE

Eight code cells. Budget an evening. This is where GRS and SR(a) get built.

- [x] Write the shared helpers first, in a cell near the top:
      - a function that runs one model across a set of portfolios and returns fitted results
      - a GRS function
      - an SR(a) function
      - a function that assembles the reporting table
- [x] Test the GRS function on synthetic data before using it on real data
- [x] Task 1 — Global portfolios, Global factors, 5x5. **STOP, we check against the paper.**
- [x] Task 2 — Global portfolios, Global factors, 4x5
- [x] Task 3 — Japan portfolios, **Global** factors, 5x5
- [x] Task 4 — Japan portfolios, **Global** factors, 4x5
- [x] Task 5 — Japan portfolios, Japan factors, 5x5
- [x] Task 6 — Japan portfolios, Japan factors, 4x5
- [x] Task 7 — individual alphas, Global portfolios with Global factors
- [x] Task 8 — individual alphas, Japan portfolios with Japan factors (notebook says: three-factor model only)

Tasks 2 through 6 should be near-identical calls to the same helpers with different inputs. If
the code is being rewritten each time, the helpers aren't general enough — fix that instead.

**GATE 6:** six scorecard tables with three model rows each, plus two alpha grids. 5x5 tables
carry five statistics, 4x5 tables carry three.

---

## Phase 7 — Notebook 04 (Tables 6 and 7)

Eight code cells, but only the four-factor model. Much faster than Phase 6 if the helpers are
reusable — it is the same eight tasks on size-momentum portfolios.

- [x] Tasks 1 through 8, same structure as notebook 03

**GATE 7:** six scorecard tables with one model row each, plus two alpha grids.

---

## Phase 8 — Export

For each of notebooks 01 through 04, in order:

- [x] `Kernel → Restart & Run All`
- [x] Confirm every cell ran, and every table and figure is visible
- [x] Save
- [x] `File → Save and Export Notebook As → HTML`
- [ ] Open the HTML in a browser and look at it

**GATE 8:** four HTML files, each opening correctly with all outputs visible. A notebook that
fails a clean restart is not reproducible, and reproducibility is a grading criterion.

---

## Phase 9 — Report and submit

- [ ] Every task has its table or figure pasted in, under a heading matching the notebook's
      own task numbering
- [ ] Every result has an interpretation covering: what it reports, whether it's close to the
      paper, important numerical differences, the main patterns, what we understand from them
- [ ] Save as Word or PDF
- [ ] Zip exactly 9 files: four `.ipynb`, four `.html`, one report
- [ ] Confirm `00_clean_data.ipynb` is NOT in the zip
- [ ] Confirm no file has been renamed

---

## Running notes

Keep a short log here as you go — anything that differed from the paper, any fix applied, any
file downloaded manually. It makes writing the report's "numerical differences" sections much
faster.

- Env: Python 3.13.3, pandas 3.0.5, numpy 2.3.3, statsmodels 0.15.0, matplotlib 3.10.7.
- Repo cloned to %TEMP%\fram_repo and its 7 files copied flat into the project folder (pristine copy kept there).
- Data vintage: all eight CSVs say "created using the 202607 Bloomberg database" (downloaded 2026-09-15). All eight via get_data.py, none manual.
- Raw files code missing values as -99.99; must not survive into the Nov 1990 to Mar 2011 sample.
- 00_clean_data ran unmodified under pandas 3.0.5, 0 errors. All 8 files: 245 rows, Nov 1990 to Mar 2011, 0 missing, 0 duplicate dates, 0 leftover -99.99/-999, no month gaps. Portfolio rows verified against the raw Value Weighted Monthly section.
- Developed RF and Japan RF are identical in all 245 months (paper: excess returns are over the US one-month T-bill). RF mean 0.28.
- Notebook 01: Tasks 1, 2 cross-checked against scipy one-sample t-tests (identical). t-Mean = mean / (sample std / sqrt(245)). Figure uses a shared y-scale per row so Global and Japan are comparable.
- Notebook 02: all 200 grid values (4 combinations x mean/std x 25) recomputed by looking portfolios up by column NAME, not position: identical. Std dev is the sample std (n - 1).
- Notebooks 03/04 judgment call, GRS: exact finite-sample form GRS = (T-N-K)/N * a'S^-1 a / (1 + f'W^-1 f), S and W divided by T. Equivalent to the (T/N)(T-N-K)/(T-K-1) form with S divided by T-K-1. df = (N, T-N-K); reproduces the paper's printed critical values 1.41/1.56/1.69/1.86/2.25 exactly.
- Notebooks 03/04 judgment call, SR(a): (a'S^-1 a)^(1/2) with S = residual covariance divided by T, the same S as GRS, so SR(a)^2 equals the max-Sharpe-ratio difference in the paper's section 5. Dividing by T-K-1 instead would multiply SR(a) by 1.004 to 1.010.
- GRS/SR(a) synthetic tests (run on the exact helper code in both notebooks): matches the max-Sharpe-ratio identity to 1e-13; under zero alphas, 1000 simulations: mean GRS 1.002 (theory 1.009), 5.1% rejection at 95%, KS p = 0.39 vs F(25, 217); nonzero alphas rejected 100%.
- Notebooks 03/04: every scorecard number and every alpha / t(a) grid recomputed with numpy only (no statsmodels): identical. All regressions: 245 obs, adjusted R2 in [0, 1], 245 overlapping dates.
- 4x5 GRS uses N = 20 (the notebook asks for one GRS from the 20 regressions). The paper notes it judges the 4x5 GRS against the 25-portfolio critical values.
- paper_comparison.md (not for submission): Paper / Ours / Difference for every Global and Japan number in Tables 1, 2, 3, 4, 6, 7. Numbers only, no verdicts. Paper values transcription-checked against the paper's own arithmetic (Table 2 only against the PDF text layer).
- Phase 8 (2026-09-16): notebooks 01-04 each run in place on a fresh kernel with `jupyter nbconvert --execute --inplace` (same as Restart & Run All), then exported with `jupyter nbconvert --to html` (the engine behind JupyterLab's HTML export). Verified: 0 errors, every code cell ran in order, 2/4/10/8 result tables, 1 figure in 01, no error output in any HTML. Only the 21 "Write your code here" cells differ from the professor's originals; every markdown and prefilled cell is byte-identical.
- 
