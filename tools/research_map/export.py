"""Export existing analysis artifacts to Jekyll data; never runs an embedding model."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

THEMES = [
    dict(id='calibration', name='Simulation Calibration and Experimental Design', color='#23778a',
         publications=['P01', 'P02', 'P03', 'P04', 'P06', 'P13']),
    dict(id='prediction', name='Interpretable and Probabilistic Predictive Modeling', color='#a16a24',
         publications=['P05', 'P07', 'P10', 'P11']),
    dict(id='physics', name='Uncertainty Quantification in Nuclear Physics', color='#7960a3',
         publications=['P08', 'P09']),
    dict(id='decisions', name='Optimization and Decision-Making', color='#b45568',
         publications=['P12', 'P14', 'P15']),
]


def finite(value):
    result = float(value)
    if not math.isfinite(result):
        raise ValueError('Non-finite coordinate or similarity')
    return result


def load_artifacts(directory):
    publications = json.loads((directory / 'publications.json').read_text())
    metadata = json.loads((directory / 'run_metadata.json').read_text())
    expected = {f'P{i:02d}' for i in range(1, 16)}
    ids = [p['id'] for p in publications]
    if len(ids) != 15 or set(ids) != expected:
        raise ValueError('Expected exactly the 15 original publication IDs')
    coordinates = {}
    with (directory / 'pca_coordinates.csv').open(newline='') as handle:
        for row in csv.DictReader(handle):
            if row['id'] in coordinates:
                raise ValueError('Duplicate PCA ID')
            coordinates[row['id']] = (finite(row['PC1']), finite(row['PC2']))
    if set(coordinates) != expected:
        raise ValueError('PCA IDs do not match publication IDs')
    with (directory / 'similarity_matrix.csv').open(newline='') as handle:
        rows = list(csv.reader(handle))
    columns = rows[0][1:]
    if len(columns) != 15 or set(columns) != expected:
        raise ValueError('Similarity columns do not match IDs')
    matrix = {}
    for row in rows[1:]:
        if len(row) != 16 or row[0] in matrix:
            raise ValueError('Malformed or duplicated similarity row')
        matrix[row[0]] = dict(zip(columns, map(finite, row[1:])))
    if set(matrix) != expected:
        raise ValueError('Similarity rows do not match IDs')
    for a in ids:
        if not math.isclose(matrix[a][a], 1, abs_tol=1e-5):
            raise ValueError('Cosine diagonal must equal one')
        for b in ids:
            if not -1 <= matrix[a][b] <= 1 or not math.isclose(matrix[a][b], matrix[b][a], abs_tol=1e-6):
                raise ValueError('Cosine matrix must be bounded and symmetric')
    theme_for = {p: theme['id'] for theme in THEMES for p in theme['publications']}
    for p in publications:
        for key in ['title', 'abstract', 'year', 'link']:
            if not p.get(key):
                raise ValueError(f'Missing {key} for {p["id"]}')
        if not p['link'].startswith(('https://', 'http://')):
            raise ValueError('Publication link must use HTTP(S)')
        p['PC1'], p['PC2'] = coordinates[p['id']]
        p['theme'] = theme_for[p['id']]
        nearest = sorted((other for other in ids if other != p['id']),
                         key=lambda other: (-matrix[p['id']][other], other))[:3]
        p['closest'] = [dict(id=other, similarity=matrix[p['id']][other]) for other in nearest]
    names = ['publications.json', 'pca_coordinates.csv', 'similarity_matrix.csv', 'run_metadata.json']
    return dict(themes=THEMES, publications=publications,
                provenance=dict(model=metadata['model'], revision=metadata['revision'],
                    source_sha256=metadata['source_sha256'],
                    pca_explained_variance_ratio=metadata.get('pca_explained_variance_ratio'),
                    artifact_sha256={name: hashlib.sha256((directory / name).read_bytes()).hexdigest()
                                     for name in names}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, default=Path('research_analysis/results'))
    parser.add_argument('--output', type=Path, default=Path('_data/research_map.json'))
    args = parser.parse_args()
    try:
        data = load_artifacts(args.results)
    except FileNotFoundError as error:
        parser.error(f'Missing genuine analysis artifact: {error.filename}. No data was generated.')
    # Prevent silently mapping an outdated corpus to the current website publications.
    import yaml
    source = yaml.safe_load(Path('_data/publist.yml').read_text())
    by_id = {f'P{i:02d}': p for i, p in enumerate(source, 1)}
    for p in data['publications']:
        current = by_id.get(p['id'])
        if (current is None or current['title'] != p['title'] or
                current['description'].split() != p['abstract'].split()):
            raise ValueError(f'Analysis abstract differs from current publication: {p["id"]}. '
                             'Resolve the source mismatch before publishing this map.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(f'Exported 15 publications with unchanged coordinates and original similarities to {args.output}')


if __name__ == '__main__':
    main()
