# Research page prototype

The page at `/research/` uses the site's existing default layout, typography,
navigation, and footer. Its SCSS and plain JavaScript are loaded only by the
Research layout. It adds no visualization dependencies, external API calls, or
embedding computation. Homepage, Publications, and Talks sources are untouched.
The old duplicate Research collection document was removed to give `/research/`
a single source in `_pages/research.html`.

## Genuine analysis artifacts required

The completed `research_analysis/results/` files were not present in the repository
or workspace when this prototype was prepared. No coordinates or similarities
have been invented. Until the genuine artifacts are exported, the page provides
the original publication abstracts as a static fallback and keeps the map hidden.
This prototype cannot be considered complete or visually verified with genuine
data until the following step succeeds.

From the repository root, with the completed analysis results available:

```bash
python -m pip install PyYAML==6.0.2
python tools/research_map/export.py --results research_analysis/results
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
bundle exec jekyll serve
```

After exporting genuine data, check `/research/` at desktop and mobile widths:
select each theme, clear all themes, restore all, use Tab/Enter/Space, select a
publication and its three neighbors, and inspect each link. Verify markers do
not move during filtering and compare PC1/PC2 and neighbor values to the source
CSVs. Review the homepage, Publications, and Talks for unchanged rendering.

JavaScript syntax, SCSS compilation, Python syntax, and the three exporter
validation tests pass. Ruby/Jekyll and the genuine results were unavailable in
the preparation environment, so full site build and browser checks remain pending.
