# Page expansion state

Source of record: sibling `tex_ICLR27_rubrics_ana/iclr2027_conference.tex` and the `.tex` files it actively includes as of 2026-10-01. The deprecated `sections/appendix_vacuous_credit.tex`, excluded figures, and placeholder figures were not used. The current paper PDF is `assets/metarubric.pdf`, copied from the paper build by the main agent; this page build script does not replace it.

Figure source PDF → page PDF and PNG preview, rendered with `pdftoppm -f 1 -singlefile -png -r 180` (400 dpi for the smaller ablation chart):

- `figures/intro_motivation.pdf` → `assets/intro_motivation.{pdf,png}`
- `figures/fig_vacuous_trajectories.pdf` → `assets/fig_vacuous_trajectories.{pdf,png}`
- `figures/metarubrics_overview.pdf` → `assets/metarubrics_overview.{pdf,png}`
- `figures/ablation_results.pdf` → `assets/ablation_results.{pdf,png}`
- `figures/pubmedqa_rubric_trace.pdf` → `assets/pubmedqa_rubric_trace.{pdf,png}`

Content mapping: abstract from the active main `.tex`; intro from `sections/01_introduction.tex`; Vacuous Credit trajectories, deletion experiment and rates from `sections/02_vacuous_credit.tex`; method from `sections/03_method.tex`; main results from `tables/main_summary.tex` and `sections/04_experiments.tex`; revision, retraining, and ablation details from the corresponding active table files and `sections/04_experiments.tex`; auxiliary bank statistics, QA examples, prompt templates, and implementation details from `sections/appendix.tex`. Figure captions are paraphrased from active captions, without adding internal provenance markers to the page.

Internal checks: generated 22 main-result data rows (four reference models and six rows in each of three training families) and 12 active prompt templates. Numeric tables, links, and heading anchors should be rechecked after future source changes. Each training configuration uses one seed; no variation across runs is claimed. The paper's advantage-sign claim is described conceptually because the active Section 2 has no numerical sign-flip table. The page makes no code-release claim beyond what the paper currently supports.
