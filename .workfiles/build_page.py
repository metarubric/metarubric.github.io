"""Build the static project page from the active manuscript's result table and prompts."""
from pathlib import Path
import html
import re

SITE = Path(__file__).resolve().parents[1]
PAPER = SITE.parent / "tex_ICLR27_rubrics_ana"


def main_table():
    src = (PAPER / "tables/main_summary.tex").read_text()
    groups = []
    current = None
    for line in src.splitlines():
        if "\\rowcolor{tablegroup}" in line and "\\multicolumn" in line:
            label = re.search(r"\\textbf\{([^}]+)\}", line)
            if label:
                current = [label[1], []]
                groups.append(current)
        elif current and "&" in line and line.rstrip().endswith(r"\\"):
            cells = [cell.strip() for cell in line.split("&")]
            if len(cells) != 8:
                continue
            values = []
            for cell in cells:
                cell = re.sub(r"~\\citep\{[^}]+\}", "", cell)
                cell = cell.replace(r"\hspace{0.8em}", "").replace(r"\.\ ", ". ").replace(r"\.\ ", ". ").replace(r"\.", ".").replace(r"\ ", " ")
                cell = re.sub(r"\\(?:textbf|underline)\{([^}]+)\}", r"\1", cell)
                cell = cell.replace(r"\\", "").strip()
                values.append(cell)
            current[1].append(values)
    parts = ['<div class="table-scroll" role="region" aria-label="Main benchmark results" tabindex="0"><table class="results-table">',
             '<caption>Performance on four medical benchmarks (%, higher is better). Qwen3 families use Qwen3 for text and same-size Qwen3-VL for multimodal tasks. Auxiliary accuracy uses the Qwen3-1.7B reader.</caption>',
             '<thead><tr><th scope="col" rowspan="2">Model / training method</th><th scope="col">PubMedQA</th><th scope="col" colspan="2">HealthBench-Hard</th><th scope="col" colspan="2">MMOral-X</th><th scope="col" colspan="2">MMOral-OPG</th></tr>',
             '<tr><th scope="col">Acc.</th><th scope="col">Acc.</th><th scope="col">Aux. Acc.</th><th scope="col">Avg.</th><th scope="col">Aux. Acc.</th><th scope="col">Avg.</th><th scope="col">Aux. Acc.</th></tr></thead>']
    for label, rows in groups:
        parts.append('<tbody><tr class="group-row"><th scope="rowgroup" colspan="8">' + html.escape(label) + '</th></tr>')
        for cells in rows:
            cls = ' class="ours"' if 'MetaRubric' in cells[0] else ''
            parts.append('<tr' + cls + '><th scope="row">' + html.escape(cells[0]) + '</th>' + ''.join('<td>' + html.escape(c) + '</td>' for c in cells[1:]) + '</tr>')
        parts.append('</tbody>')
    parts.append('</table></div>')
    return '\n'.join(parts), groups


def figure(name, alt, caption):
    dimensions = {
        'intro_motivation': (2727, 1325),
        'fig_vacuous_trajectories': (1257, 446),
        'metarubrics_overview': (3000, 1800),
        'ablation_results': (1220, 840),
        'pubmedqa_rubric_trace': (1872, 1026),
    }
    width, height = dimensions[name]
    return f'''<figure class="paper-figure"><a class="figure-link" href="assets/{name}.pdf" aria-label="Open full-size {html.escape(alt)} PDF"><img src="assets/{name}.png" width="{width}" height="{height}" alt="{html.escape(alt)}" loading="lazy"></a><figcaption>{caption} <a href="assets/{name}.pdf">Open full-size PDF ↗</a></figcaption></figure>'''


table, groups = main_table()
assert len(groups) == 4 and sum(len(rows) for _, rows in groups) == 22

page = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="MetaRubric learns rewards for rubric-based reinforcement learning through evidence-aware policy optimization and response-guided rubric adaptation.">
  <meta name="theme-color" content="#10253d">
  <title>MetaRubric: Learning to Reward for Rubric-Based Reinforcement Learning</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
<header class="hero" id="top"><div class="page-shell">
  <nav class="topbar" aria-label="Main navigation"><a class="wordmark" href="#top">MetaRubric</a><div class="nav-links"><a href="#abstract">Abstract</a><a href="#introduction">Introduction</a><a href="#vacuous-credit">Vacuous Credit</a><a href="#method">Method</a><a href="#results">Results</a><a href="#appendix">Details</a></div></nav>
  <div class="hero-content"><h1>MetaRubric: Learning to Reward for Rubric-Based Reinforcement Learning</h1><p class="authors">Yuxuan Fan <span aria-hidden="true">·</span> Jaehong Yoon<sup>†</sup></p><p class="affiliation">NTU, Singapore<br><span>† Corresponding author</span></p><div class="hero-actions"><a class="button button-primary" href="assets/metarubric.pdf">Read the paper ↗</a><a class="button button-secondary" href="https://github.com/metarubric/metarubric.github.io">Project repository ↗</a></div></div>
</div></header>
<main>
<section class="section section-tinted" id="abstract"><div class="page-shell narrow"><h2>Abstract</h2><p>Rubric-based reinforcement learning extends reward-driven optimization to open-ended tasks by assigning partial credit to individual response requirements. However, rubric judges can assign a high criterion score even when the information or action it requires is absent from the response, a failure mode we term <em>Vacuous Credit</em>. Such awards persist after the required information is removed and can reverse the sign of a response's GRPO advantage.</p><p>To address this problem, we introduce MetaRubric, which alternates evidence-aware policy optimization with response-guided rubric adaptation. We construct counterfactual counterparts by changing one task-relevant fact in each prompt. During policy optimization, credit is assigned only when the response contains sufficient evidence to satisfy the required rubric criterion. After each policy-optimization stage, current policy responses guide revisions to original and counterfactual criteria while preserving the meaning of the original prompt's initial rubric as interpreted under each prompt's facts. We also adapt criterion weights at stage boundaries to better address observed policy errors.</p><p>Across multiple backbones, MetaRubric improves PubMedQA accuracy by 6.00–20.40 percentage points over static-judge GRPO, with further gains on HealthBench-Hard and two multimodal medical benchmarks.</p></div></section>
<section class="section" id="introduction"><div class="page-shell"><div class="narrow"><h2>Introduction</h2><p>A rubric may ask a medical assistant to request the patient's location before advising on post-stent checkups. A response that only says regional guidance differs can still receive full credit under an underspecified criterion, despite never asking for the location or giving a checkup frequency. MetaRubric targets this mismatch between credited behavior and content actually present.</p></div>
{figure('intro_motivation', 'Motivation diagram comparing vacuous criterion credit with the MetaRubric response and training loops', 'Vacuous Credit under an incomplete criterion, and the policy and rubric loops that address it.')}
</div></section>
<section class="section section-tinted" id="vacuous-credit"><div class="page-shell"><div class="narrow"><h2>Vacuous Credit</h2><h3>Reward growth and rubric satisfaction</h3><p>In HealthBench training with Qwen3-8B, using either GPT-4o-mini or GPT-5.4-mini as the reward judge, training reward increased while a separate test-set panel score declined. The panel used GPT-5.5, Gemini 3.5 Flash, and DeepSeek-V4-Pro, counting a criterion as satisfied only with unanimous agreement. An independent audit found that credit for fully omitted requirements persisted during training.</p></div>
{figure('fig_vacuous_trajectories', 'Four panels showing training reward, rubric scores, satisfied requirement weight, and Vacuous Credit over training', 'Training reward and stronger-judge rubric satisfaction diverge; the lower panels show satisfied requirement weight and audited Vacuous Credit relative to step 0.')}
<div class="narrow"><h3>Deletion test</h3><p>For 1,000 policy rollouts judged correct during training, the paper compares deleting required content with deleting generic statements while preserving the required content. Award retention measures the share of initially credited target criteria still credited after each edit.</p></div>
<div class="inner-table"><div class="table-scroll" role="region" aria-label="Deletion test results" tabindex="0"><table><caption>Retention of target-criterion awards after content deletion.</caption><thead><tr><th scope="col">Reward judge</th><th scope="col">Required content deleted</th><th scope="col">Generic statements deleted</th></tr></thead><tbody><tr><th scope="row">GPT-4o-mini</th><td>82.0%</td><td>93.1%</td></tr><tr><th scope="row">GPT-5.4-mini</th><td>69.8%</td><td>95.0%</td></tr></tbody></table></div></div>
<p class="narrow closing">Most target awards survive deletion of the content needed to satisfy the criterion. Since GRPO compares rewards within each rollout group, such awards can change which responses receive positive advantage and are reinforced.</p>
</div></section>
<section class="section" id="method"><div class="page-shell"><div class="narrow"><h2>Method</h2><p>Each training stage holds the rubric fixed while the policy learns, then adapts criterion weights and descriptions from the errors in that stage's responses. Original prompts are paired with counterfactual prompts that change one task-relevant fact; each response is scored against the rubric for its own prompt.</p></div>
{figure('metarubrics_overview', 'MetaRubric overview with evidence-aware GRPO inner loop and rubric adaptation outer loop', 'Each stage alternates evidence-aware GRPO updates with rubric adaptation. Accepted updates carry into the next stage.')}
<div class="method-grid"><article><h3>Evidence-aware reward</h3><p>For each criterion, a judge checks satisfaction, coverage, and support. Its credit is capped by the weakest of these three scores. A response-level support cap and a quality factor further constrain the rubric reward. A separate Qwen3-1.7B reader answers fixed multiple-choice questions using only the response, checking whether task facts can be recovered from it.</p></article><article><h3>Adapt the rubric from errors</h3><p>Criteria share weight adjustments by severity and correspondence type. Groups missed more often gain relative weight, while severity order and bounded adjustments preserve priorities. A proposer may clarify one criterion description at a stage boundary. It is accepted only after held-out judgment agreement improves beyond the threshold and a separate review confirms the initial requirement is preserved.</p></article></div></div></section>
<section class="section section-tinted" id="results"><div class="page-shell"><div class="narrow"><h2>Experiments</h2><p>MetaRubric improves over static-judge GRPO in all 21 model-family and metric comparisons. It has the highest score among training methods in 19 of 21 comparisons; Dr. GRPO leads on HealthBench-Hard for Qwen3-4B and MMOral-OPG for Gemma-e2b. PubMedQA gains over GRPO are 6.00, 6.80, and 20.40 percentage points for Qwen3-4B, Qwen3-8B, and Gemma-e2b. The three open-ended benchmark gains range from 1.29 to 3.82 points.</p><p>PubMedQA uses answer accuracy. The other benchmarks use HealthBench-Hard accuracy-axis score, MMOral-X mean score, and MMOral-OPG overall score. GPT-5.5 is the strong judge for model-based test-set evaluation. Auxiliary QA accuracy measures exact option matching by the Qwen3-1.7B reader, with invalid outputs counted incorrect.</p></div>
{table}
<div class="narrow"><h3>Component ablations</h3><p>Ablations with the Qwen3-4B family show the largest drop when both rubric descriptions and weights are frozen: 3.17 points on HealthBench-Hard and 4.40 on MMOral-OPG. Removing evidence checks lowers scores by 1.22 and 2.59 points, even with auxiliary QA and paired sampling retained. All variants keep the quality multiplier, auxiliary QA reward, and paired sampling.</p></div>
{figure('ablation_results', 'Bar chart of MetaRubric component ablations on HealthBench-Hard and MMOral-OPG', 'Component ablations: HealthBench-Hard accuracy-axis score with Qwen3-4B and MMOral-OPG overall score with Qwen3-VL-4B (0–100; higher is better).')}
<div class="two-tables"><div class="table-scroll" role="region" aria-label="Rubric revision statistics" tabindex="0"><table><caption>Rubric revision statistics for Qwen3-4B. A criterion counts once if its description or correspondence label changed; weight-only updates are excluded.</caption><thead><tr><th scope="col">Dataset</th><th scope="col">Total</th><th scope="col">Revised</th><th scope="col">Avg. words before</th><th scope="col">Avg. words after</th></tr></thead><tbody><tr><th scope="row">HealthBench</th><td>10,448</td><td>4,727 (45.2%)</td><td>40.8</td><td>46.3</td></tr><tr><th scope="row">PubMedQA</th><td>2,949</td><td>879 (29.8%)</td><td>14.3</td><td>18.2</td></tr><tr><th scope="row">MMOral-RL</th><td>8,672</td><td>5,259 (60.6%)</td><td>16.9</td><td>22.5</td></tr></tbody></table></div><div class="table-scroll" role="region" aria-label="Final rubric retraining" tabindex="0"><table><caption>Retraining Qwen3-4B with learned final rubrics. MetaRubric updates the rubric during training.</caption><thead><tr><th scope="col">Training rubric</th><th scope="col">HealthBench-Hard accuracy</th><th scope="col">MMOral-OPG overall</th></tr></thead><tbody><tr><th scope="row">Baseline</th><td>8.83</td><td>20.59</td></tr><tr><th scope="row">Final rubric</th><td>9.04</td><td>21.78</td></tr><tr class="ours"><th scope="row">MetaRubric</th><td>13.02</td><td>26.35</td></tr></tbody></table></div></div>
<p class="narrow closing">The final rubric alone recovers only 5.0% of the HealthBench-Hard gain and 20.7% of the MMOral-OPG gain over baseline in these runs. The sequence of rubric updates contributes beyond the final rubric text.</p>
<div class="narrow"><h3>Illustrative rubric revision</h3><p>For a PubMedQA prostate-bed motion question, the example aligns an abstract finding, a response, and a criterion before and after revision. The illustrative weight update moves an evidence criterion from +6 to +5 and an overstatement penalty from −6 to −8, giving more relative emphasis to the observed overstatement errors.</p></div>
{figure('pubmedqa_rubric_trace', 'Illustrative PubMedQA rubric revision and weight trace for a prostate-bed motion question', 'The revision clarifies supported and unsupported claims; the weight update changes their relative priority.')}
</div></section>
<section class="section" id="appendix"><div class="page-shell"><div class="narrow"><h2>Appendix: implementation details and examples</h2><p>PubMedQA uses the non-test part of the expert-labeled PQA-L subset for training and the official 500-question test set for evaluation. HealthBench training and validation use conversations outside HealthBench-Hard; the Hard subset has 1,000 test conversations. MMOral-X and MMOral-OPG share the 980-example MMOral-RL training set; their test sets contain 300 and 578 questions.</p><p>Each training configuration uses one seed, so the reported scores do not quantify variation across runs. The supplied HealthBench Qwen3-4B configuration uses eight rollouts per prompt, sixteen responses per original–counterfactual group, rubric and QA reward coefficients of 1.0 and 0.3, and a revision threshold strictly above 0.02 on 20 validation prompt pairs.</p><h3>Auxiliary question banks</h3><p>The reader receives a model response plus the question and four options, then returns one letter. Questions are built from benchmark references and annotations; model responses are withheld during construction. HealthBench-Hard evaluation questions undergo content review without a mandatory question-only screening pass. Each MMOral evaluation bank retains all constructed questions once its valid-wrong screening rate exceeds 90%, including reader-correct items. PubMedQA instead uses its yes/no/maybe reference label directly.</p></div>
<div class="table-scroll" role="region" aria-label="Auxiliary question bank sizes" tabindex="0"><table><caption>Auxiliary-question construction statistics for evaluation. Questions per entry includes entries without a question.</caption><thead><tr><th scope="col">Benchmark</th><th scope="col">Source entries</th><th scope="col">Covered entries</th><th scope="col">Questions</th><th scope="col">Questions / entry</th></tr></thead><tbody><tr><th scope="row">HealthBench-Hard</th><td>1,000</td><td>965</td><td>4,117</td><td>4.12</td></tr><tr><th scope="row">MMOral-X</th><td>300</td><td>300</td><td>828</td><td>2.76</td></tr><tr><th scope="row">MMOral-OPG</th><td>578</td><td>578</td><td>981</td><td>1.70</td></tr></tbody></table></div>
<div class="narrow examples"><h3>Three auxiliary QA examples</h3><details><summary>HealthBench-Hard: follow-up timing</summary><p><strong>Source request:</strong> “mention we only recommend a re-check if fever returns or symptoms worsen or fail to improve within another 2-3 days.”</p><p><strong>Question:</strong> What specific follow-up timing should the rewritten message say for lack of improvement?</p><ol type="A"><li>It should say: fails to improve within another 2-3 days.</li><li>It should say: fails to improve within another 5-7 days.</li><li>It should say: fails to improve after completing the full 10-day course.</li><li>It should say: fails to improve within another 24-48 hours.</li></ol><p><strong>Correct answer: A</strong></p></details><details><summary>MMOral-X: treatment identification</summary><p><strong>Source reference:</strong> “Endodontic treatments are noted on teeth 13, 23, 24, 26, and 45.”</p><p><strong>Question:</strong> Which teeth have endodontic treatments?</p><ol type="A"><li>Teeth 13, 23, 24, 26, and 47.</li><li>Teeth 13, 23, 24, 26, and 45.</li><li>Teeth 13, 24, 25, 26, and 45.</li><li>Teeth 12, 23, 24, 26, and 45.</li></ol><p><strong>Correct answer: B</strong></p></details><details><summary>MMOral-OPG: tooth counting and identification</summary><p><strong>Source reference:</strong> “Four wisdom teeth are detected: #18, #28, #38, and #48.”</p><p><strong>Question:</strong> How many wisdom teeth are detected in the radiograph, and which teeth are they?</p><ol type="A"><li>Four wisdom teeth are detected: #18, #28, #38, and #48.</li><li>Two wisdom teeth are detected: #18 and #38.</li><li>Four wisdom teeth are detected: #17, #27, #37, and #47.</li><li>Three wisdom teeth are detected: #18, #28, and #48.</li></ol><p><strong>Correct answer: A</strong></p></details></div>
</div></section>
</main><footer class="site-footer"><div class="page-shell footer-inner"><span>MetaRubric · NTU, Singapore</span><a href="#top">Back to top ↑</a></div></footer>
</body></html>'''
(SITE / 'index.html').write_text(page)
print(f'Wrote page with {sum(len(rows) for _, rows in groups)} main-result rows')
