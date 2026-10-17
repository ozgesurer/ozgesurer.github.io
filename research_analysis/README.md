# Publication semantic analysis

Standalone exploratory analysis. No website page, layout, style, or configuration changes.
Run commands below from the repository root in a GitHub Codespace with Python 3.11
or 3.12. No merge or push is needed.

```bash
python3 -m venv research_analysis/.venv
source research_analysis/.venv/bin/activate
python -m pip install --upgrade pip
python -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r research_analysis/requirements.txt
python research_analysis/analyze.py --validate-only
python research_analysis/analyze.py
python -m pip freeze > research_analysis/results/environment.txt
```

The default input is `_data/publist.yml` in your Codespace checkout. Ensure that
checkout includes your corrected breakup-reactions abstract. The retained
`extracted/publist.yml`, `publications.json`, and `publications.csv` are the prior
GitHub extraction (Git blob `0e4b95f94628f1008010e037390103943e99aafb`).
They are preserved rather than overwritten. To analyze exactly that snapshot:

```bash
python research_analysis/analyze.py --input research_analysis/extracted/publist.yml
```

The first analysis run downloads genuine pretrained weights from Hugging Face.
If model access is blocked, the run fails; it never substitutes vectors or scores.
`--validate-only` does not import Sentence Transformers or download anything.
No weights were downloaded during script creation.

## Method

- Model: `sentence-transformers/all-MiniLM-L6-v2`, fixed revision
  `c9745ed1d9f207416be6d2e6f8de32d1f16199bf`, 384-dimensional embeddings; CPU inference.
- Input: original title plus description. Collapse whitespace only; retain case,
  punctuation, stop words, and technical terms. Years/authors/venues are excluded.
  Years are extracted from parentheses in `link.display`; missing fields fail validation.
- Tokenize the entire input without truncation. Window size is the model sequence
  limit minus special tokens, with 32-token overlap. Pass token IDs directly to the
  model so decoding/re-tokenization cannot cause hidden truncation. Every token is
  covered. Normalize window vectors, average with weights equal to newly covered
  token counts, and normalize again. This limits repeated-window weighting but
  does not exactly remove contextual influence of overlap. This document aggregation
  is an explicit heuristic, not a model trained on full-document similarity.
- Cosine similarity is the dot product of normalized document vectors. Rank the
  unique unordered pairs; omit diagonal self-similarities. With 15 publications,
  there are 105 pairs and a 15 × 15 matrix. All original publication text is exported.
- Network: all publications remain visible, including isolates. Include an edge
  when cosine ≥ 0.50. Width reflects similarity; spring positions use seed 42.
  The threshold is exploratory, not a significance threshold. Change it with
  `--threshold 0.60 --output research_analysis/results-060`.
- PCA: centered full-SVD PCA of the original normalized document embeddings,
  without feature standardization. Axis labels and metadata report explained
  variance. Two-dimensional proximity only approximates full-space relationships;
  use the cosine matrix for actual similarity. PCA axis signs are arbitrary.
- Fixed package/model versions and seeded layout support reproducibility. Metadata
  records installed dependencies and input hash; retain `environment.txt` too.
  Exact numerical values can still vary slightly across platforms.

## Outputs

`research_analysis/results/` contains:

- `publications.json` and `publications.csv`: unchanged descriptions and metadata.
- `embeddings.npy`: real document embeddings, in publication ID order.
- `similarity_matrix.csv`: labeled complete cosine matrix.
- `all_pairs.csv`: all pairs sorted by decreasing similarity.
- `most_similar_pairs.csv`: top 20 (change with `--top-pairs`).
- `network.html`, `pca.html`, `similarity_heatmap.html`: interactive, self-contained
  HTML files, including Plotly JavaScript; open downloaded files in a browser.
- `pca_coordinates.csv` and `run_metadata.json`: coordinates and audit information.

Use VS Code's Explorer in Codespaces to download/open the HTML files. Each node
has an ID and title/year hover text; IDs map to exported publications. Network edge
midpoints show similarity on hover. These artifacts are not added to the website.

## Content-based hypotheses to inspect after running

These are preserved qualitative observations, not computed rankings:

- P01/P03: stochastic calibration and exploration versus replication.
- P04/P06: sequential design targeting parameter posterior uncertainty.
- P07/P10/P11: coefficient-tree regression variants.
- P08/P09: Bayesian uncertainty analysis in different nuclear-physics applications.
- P05 versus calibration papers: a possible bridge through predictive distributions.
- P12/P13: common COVID-19 application, but different policy/calibration questions.
- P14/P15: different applications linked by constrained optimization.

Review top pairs and unexpected connections against the actual abstracts. Shared
domain vocabulary can dominate methodological relationships. Cosine similarity
is not research quality, influence, or statistical evidence of collaboration.
Do not treat these hypotheses as embedding findings until the run succeeds.

## Data quality and validation

The retained snapshot has 15 publications (2016–2026), no missing or duplicated
titles/descriptions, and descriptions of 98–304 whitespace-separated words. All
read as complete abstracts; publisher-level completeness was not verified.
The breakup-reactions duplicate is fixed. All `highlight` fields equal 1 and
`news2` fields are empty; neither is used. URLs are preserved without live resolution.

Offline checks (no model download):

```bash
python -m unittest discover -s research_analysis -p 'test_*.py'
python research_analysis/analyze.py --input research_analysis/extracted/publist.yml --validate-only
```
