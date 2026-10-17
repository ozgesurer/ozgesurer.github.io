# Research page prototype

The page at `/research/` uses the site's existing default layout, typography,
navigation, and footer. Its SCSS and plain JavaScript are loaded only by the
Research layout. It adds no visualization dependencies, external API calls, or
embedding computation. Homepage, Publications, and Talks sources are untouched.
The old duplicate Research collection document was removed to give `/research/`
a single source in `_pages/research.html`.

## Data source

`_data/research_map.json` contains the genuine corrected analysis exported from
`research_analysis/results-corrected/` on branch `work`, commit
`00a947e9886cecc6af6b8e66a36b726020c851eb`. All 15 abstracts match the current
website corpus, including P09's corrected breakup-reactions abstract. The original
analysis files remain unchanged on `work`; they are not required at website runtime.
The page is ready to render from the committed JSON without Python or a model.

From the repository root, with the completed analysis results available:

```bash
python -m pip install PyYAML==6.0.2
python tools/research_map/export.py --results research_analysis/results-corrected
```

Required files: `publications.json`, `pca_coordinates.csv`,
`similarity_matrix.csv`, and `run_metadata.json`. The exporter writes only
`_data/research_map.json`; it never changes the analysis files. Commit that export
on this feature branch to make the static page work on GitHub Pages.
The full matrix is validated; neighbors use its original values with ID order
as a deterministic tiebreaker. Source artifact SHA256 hashes record provenance.
Titles and abstracts must match the current corpus (ignoring whitespace only).
If the original analysis used an outdated abstract, the exporter rejects the
mismatch rather than silently presenting it as current research.

## Design and interaction

The four themes and their publication assignments are researcher-defined.
The SVG uses one uniform affine scale of original PCA coordinates, with the
vertical axis flipped for screen coordinates. No clustering, jitter, force
layout, or category-based repositioning is applied. Filtering leaves the scale
and point positions fixed. Similarities in the detail panel come from the full
embedding space and include publications in other/hidden themes; selecting a
neighbor reveals its theme. Displayed scores are rounded to three decimals only.

Mouse hover and keyboard focus show titles and years. Enter/Space or a tap opens
the publication detail panel; all selection actions also have native buttons in
the title list for mobile and assistive technology. Theme checkboxes provide a
legend and filtering. All themes may be deselected, with a clear empty state.
Publication abstracts remain available without JavaScript. On narrow screens,
the detail panel stacks below the map and the title list provides larger targets.

## Verification

```bash
node --check assets/js/research-map.js
python -m unittest discover -s tools/research_map -p 'test_*.py'
bundle install
bundle exec jekyll build
bundle exec jekyll serve --host 0.0.0.0 --port 4000
```

After exporting genuine data, check `/research/` at desktop and mobile widths:
select each theme, clear all themes, restore all, use Tab/Enter/Space, select a
publication and its three neighbors, and inspect each link. Verify markers do
not move during filtering and compare PC1/PC2 and neighbor values to the source
CSVs. Review the homepage, Publications, and Talks for unchanged rendering.

JavaScript syntax, SCSS compilation, Python syntax, and all four exporter
validation tests pass. All 15 coordinate pairs and 45 displayed neighbor scores
match the corrected source CSVs exactly. DOM checks using the corrected data
cover marker creation, abstract text, neighbor ordering, all/none filtering,
unchanged positions, and keyboard selection.

## Preview before merging

Open a Codespace on `feature/research-map` (not `work` or `master`). From the
repository root:

```bash
git switch feature/research-map
git pull --ff-only origin feature/research-map
bundle install
bundle exec jekyll serve --host 0.0.0.0 --port 4000
```

In the Codespaces **Ports** panel, open port **4000** in your browser and append
`/research/` to the forwarded URL. This previews the branch without deploying
or merging it. The analysis model does not need to be installed or run.

The PR's **Research prototype build** workflow also runs a production Jekyll
build and uploads a `research-site-preview` artifact. It never deploys the site.
To view a downloaded artifact locally, unzip it, run `python -m http.server 4000`
inside the unzipped directory, and visit `http://localhost:4000/research/`.
