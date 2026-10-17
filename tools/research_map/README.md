# Research page prototype

The page at `/research/` uses the site's existing default layout, typography,
navigation, and footer. Its SCSS and plain JavaScript are loaded only by the
Research layout. It adds no visualization dependencies, external API calls, or
embedding computation. Homepage, Publications, and Talks sources are untouched.
The only data request is for the same site's static `/assets/data/research-map.json`.
It uses no external runtime API. Serving JSON separately prevents the shared
HTML compressor from altering abstract strings.
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

The header follows the Publications/Talks spacing, and the desktop map/details
columns use a 1.9:1 ratio, stacking on mobile. Point titles appear on hover or
keyboard focus rather than as overlapping permanent labels. Selected papers have
a dark outline; their three closest papers have outer rings and subtle connecting
lines. Theme filters still hide points and their connections, while all three
original rankings and scores remain in the detail panel. No points are moved.

The detail panel initially shows an excerpt of up to 320 characters, cut at a
word boundary. Read full abstract / Show less toggles the complete original text
without rewriting it. Selecting another paper resets the excerpt view.

Theme filters are native toggle buttons styled as color-coded chips, with
`aria-pressed` state and keyboard activation. The 2016–2026 slider is inclusive:
it shows publications through the selected year. Show all years is checked by
default; moving the slider turns it off, and checking it restores 2026. Theme
and year filters intersect for the map, title list, and visible connections.
If filters hide the selected paper, the detail panel clears without moving
keyboard focus. Related papers retain their top-three collection-wide rankings;
filtered papers are marked outside current filters. Selecting one reveals its
theme and extends the year cutoff if needed. Scores and PCA coordinates never change.

The short introduction sits above the map; technical context is in About this
map. Related-work copy explains that collection-relative textual rankings do not
necessarily imply strong relationships, and connections use the original embedding
space rather than PCA distances.

Mouse hover and keyboard focus show titles and years. Enter/Space or a tap opens
the publication detail panel; all selection actions also have native buttons in
the title list for mobile and assistive technology. Theme chips provide a
legend and filtering. All themes may be deselected, with a clear empty state.
Publication abstracts remain available without JavaScript. On narrow screens,
the detail panel stacks below the map and the title list provides larger targets.

## Verification

```bash
node --check assets/js/research-map.js
python -m unittest discover -s tools/research_map -p 'test_*.py'
npm install --prefix /tmp/research-map-tests jsdom@26.1.0 --no-audit --no-fund
NODE_PATH=/tmp/research-map-tests/node_modules node tools/research_map/test_filters.cjs
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
The saved DOM regression suite exercises all 11 year cutoffs against all four
themes using the genuine committed data, inclusive boundaries, reset and empty
states, selection clearing/reveal, rankings, abstract expansion, and fixed geometry.
It also runs in the PR build workflow; jsdom is a test dependency only.
The production build passed with Ruby 3.2 and Jekyll 3.10 locally in a container
and in GitHub Actions. Chromium checks at 1280px, 390px, and 320px widths passed for all
15 original abstracts and 45 neighbor links, keyboard and pointer selection,
filters, fixed geometry, no horizontal overflow, and the no-JavaScript fallback.
The build retains existing warnings in unrelated Teaching, Software, CV, and
collection excerpts; those pages were not edited.

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
