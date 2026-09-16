# FIN F414 FRAM Lab 1 — project context

Everything here is verified against the actual repo, README.md and data.docx. Trust it over
any assumption. For the step-by-step execution order, see PLAN.md.

## The assignment

Replicate selected results from Fama & French (2012), "Size, Value, and Momentum in
International Stock Returns," using current Kenneth French Data Library files.

Sample period is fixed: **November 1990 to March 2011, 245 monthly observations.**
"Developed" datasets represent **Global** in the paper. The other market is **Japan**.

Deadline: EOD 17 September 2026. Three of us working on one machine.

## Us

Three 2nd-year Electrical & Electronics students, finance minors. We know basic Python but have
never used pandas, numpy, matplotlib or statsmodels.

- Explain what a cell does in plain English before we run it.
- Don't re-explain the finance. We know what the portfolios, alpha, GRS and the factors are.
- When a table prints, say in one line what it is, so whoever is writing can follow.

## Folder layout

The notebooks use relative paths, so everything must sit flat in one folder:

```
project_folder/
├── CLAUDE.md
├── PLAN.md
├── get_data.py
├── fama.pdf                  the reference paper
├── raw_data/                 eight downloaded CSVs
├── cleaned_data/             created by 00_clean_data.ipynb
├── 00_clean_data.ipynb
├── 01_replicate_table1.ipynb
├── 02_replicate_table2.ipynb
├── 03_replicate_table3_table4.ipynb
└── 04_replicate_table6_table7.ipynb
```

Never create a nested subfolder for the repo. Never reorganise this structure.

## What is already written for us

The professor has written ALL the data-loading code, the `models` dictionaries, and the
portfolio-selection code (`all_portfolios`, `without_microcaps`). We only fill cells marked
`# Write your code here`. There are 21 such cells across the four notebooks.

**Never modify a markdown cell. Never rewrite a prefilled code cell.**

## The data

Eight CSVs in `raw_data/`, named exactly:

```
developed_3_factors.csv          japan_3_factors.csv
developed_momentum.csv           japan_momentum.csv
developed_25_size_bm.csv         japan_25_size_bm.csv
developed_25_size_momentum.csv   japan_25_size_momentum.csv
```

`get_data.py` downloads, unzips and renames all eight. `00_clean_data.ipynb` then produces
`cleaned_data/`.

Returns and RF are already in percent. Never divide by 100 or annualise.

## What each notebook does

### 01 — Table 1: FACTOR statistics (5 tasks, 3 code cells)
Uses factor files only, not portfolios.
- **Task 1** Global: for Mkt-RF, SMB, HML, WML compute mean, std dev, t-stat of the mean.
  Columns named Mean, Std dev, t-Mean. Round to 2dp.
- **Task 2** Same for Japan.
- **Task 3** Written comparison with the paper. No code cell.
- **Task 4** Figure with 8 panels, 4 rows x 2 columns. One row per factor
  (Mkt-RF, SMB, HML, WML); left column Global, right column Japan. Dates on x, monthly factor
  value on y, a title on each panel.
- **Task 5** Written interpretation of the graphs. No code cell.

### 02 — Table 2: 25-PORTFOLIO grids (3 tasks, 2 code cells)
Panel A = size x book-to-market. Panel B = size x momentum.
- **Task 1** Excess returns for four combinations: Developed size-BM, Japan size-BM, Developed
  size-momentum, Japan size-momentum. Subtract the **market-specific `RF` column only** — never
  `Mkt-RF`. Developed RF for Developed portfolios, Japan RF for Japan portfolios.
- **Task 2** For each of the four, the mean and std dev of each portfolio's 245 excess returns,
  arranged as 5x5. Rows Small to Big; columns Low to High B/M, or Losers to Winners. The first
  five columns are the Small row, next five row 2, and so on. Average across the 245 months per
  portfolio, NOT across the 25 portfolios. Round to 2dp.
- **Task 3** Written comparison. No code cell.

### 03 — Tables 3 and 4: model tests on size x book-to-market portfolios (8 tasks)
Models already defined: CAPM `[Mkt-RF]`, Three-factor `[Mkt-RF, SMB, HML]`,
Four-factor `[Mkt-RF, SMB, HML, WML]`.

| Task | Portfolios | Factors | Set |
|---|---|---|---|
| 1 | developed | developed | 5x5, all 25 |
| 2 | developed | developed | 4x5, `without_microcaps`, 20 |
| 3 | japan | **developed** | 5x5 |
| 4 | japan | **developed** | 4x5 |
| 5 | japan | japan | 5x5 |
| 6 | japan | japan | 4x5 |

Per task: merge on `date`, subtract `RF` from every portfolio return, add a constant, run one
regression per portfolio for each of the three models, store the fitted results, print ONE table
with the three models as rows. Round to 2dp.

- 5x5 reports: `GRS`, `|a|`, `Adjusted R2`, `s(a)`, `SR(a)`
- 4x5 reports only: `GRS`, `|a|`, `SR(a)`

Table 4:
- **Task 7** Individual portfolio alphas, Global portfolios with Global factors.
- **Task 8** Individual portfolio alphas, Japanese portfolios with Japanese factors.

### 04 — Tables 6 and 7: same tests on size x momentum portfolios (8 tasks)
Identical task structure to notebook 03, same six combinations plus Tasks 7 and 8 for
individual alphas. **Only one model here:** Four-factor `[Mkt-RF, SMB, HML, WML]`.

## The statistics

- **`|a|`** — collect alpha from every regression, take absolute values, simple average.
  25 for 5x5, 20 for 4x5.
- **`Adjusted R2`** — average of the adjusted R-squared from each regression. 5x5 only.
- **`s(a)`** — average of the standard error of the constant from each regression. 5x5 only.
- **`SR(a)`** — ONE joint value per model, never an average of per-portfolio ratios. Stack the
  alphas into a vector, build the residual covariance matrix from all regressions, combine per
  the paper's formula, take the square root.
- **`GRS`** — ONE joint statistic per model, from all alphas, all residuals, the factor returns,
  N portfolios, K factors, T observations. Never per portfolio and averaged. statsmodels does
  not provide it, so implement it and test it on synthetic data before trusting it.

## How to work

- **One task at a time.** Write the code for one task, stop, let us run it and look at the
  output. Never batch through multiple tasks.
- **Stop after the first table in each notebook** so we can check it before continuing.
- **Before any regression**, print the number of overlapping dates between the portfolio and
  factor frames. If it isn't 245, stop.
- Write the regression and statistics logic ONCE as reusable functions and call them for every
  task. Tasks 1-6 differ only in inputs. Never paste the same code eight times.
- Keep helper functions in a cell inside the notebook, not a separate .py file — the notebook
  must run standalone from a clean restart.
- If stuck on the same error after two attempts, stop and explain rather than trying variations.
- Never invent a number. If something won't compute, say so.

## Mechanical checks only

Verify these, because failing them is structurally wrong:
- 245 rows after every merge
- 25 portfolio columns for 5x5, 20 for 4x5
- Adjusted R-squared between 0 and 1
- Regression sample size equals 245

Do NOT check whether results match what the paper concluded, and do not tell us what the result
"should" be. We judge that ourselves against the paper — the README requires the interpretations
to show our own understanding.

## Not your job

Every written interpretation: Tasks 3 and 5 in notebook 01, Task 3 in notebook 02, and the
discussion of every result in the report. The README explicitly requires these in our own words
and not from AI. Produce correct numbers and figures; we write what they mean.

## Deliverable

One ZIP with 9 files: notebooks 01-04, an HTML export of each, and one report (Word or PDF).
`00_clean_data` is NOT submitted.

Report organised by notebook then task. For each result discuss: what it reports, whether it's
close to the paper, important numerical differences, the main patterns, and what we understand
from them.

Graded on: closeness of replication, task completion, correct and reproducible code, proper
comparison with the paper, and interpretations showing our own understanding.
