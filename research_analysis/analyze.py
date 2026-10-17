"""Standalone semantic analysis; importing this module never downloads a model."""
import argparse
import csv
import hashlib
import importlib.metadata
import json
import re
from pathlib import Path


def read_publications(path):
    import yaml
    raw = path.read_bytes()
    items = yaml.safe_load(raw)
    if not isinstance(items, list) or len(items) < 3:
        raise ValueError('Expected a YAML list with at least three publications.')
    records = []
    for i, item in enumerate(items, 1):
        title, abstract = item.get('title'), item.get('description')
        link = item.get('link') or {}
        years = re.findall(r'\((\d{4})\)', str(link.get('display', '')))
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f'Publication {i}: missing title')
        if not isinstance(abstract, str) or not abstract.strip():
            raise ValueError(f'Publication {i}: missing description')
        if len(years) != 1 or not link.get('url'):
            raise ValueError(f'Publication {i}: expected one year and a URL')
        records.append(dict(id=f'P{i:02d}', title=title, abstract=abstract,
                            year=int(years[0]), link=link['url']))
    return records, hashlib.sha256(raw).hexdigest()


def token_windows(token_ids, capacity, overlap):
    """Cover every token; each window weight counts newly covered tokens."""
    if capacity <= overlap or overlap < 0:
        raise ValueError('Overlap must be nonnegative and smaller than window capacity')
    windows = []
    start = covered = 0
    while start < len(token_ids):
        end = min(start + capacity, len(token_ids))
        windows.append((token_ids[start:end], end - covered))
        covered = end
        if end == len(token_ids):
            break
        start = end - overlap
    return windows


def write_csv(path, rows, fields):
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=Path('_data/publist.yml'))
    parser.add_argument('--output', type=Path, default=Path('research_analysis/results'))
    parser.add_argument('--model', default='sentence-transformers/all-MiniLM-L6-v2')
    parser.add_argument('--revision', default='c9745ed1d9f207416be6d2e6f8de32d1f16199bf')
    parser.add_argument('--overlap', type=int, default=32)
    parser.add_argument('--threshold', type=float, default=0.50)
    parser.add_argument('--top-pairs', type=int, default=20)
    parser.add_argument('--expected-count', type=int, default=15)
    parser.add_argument('--validate-only', action='store_true')
    args = parser.parse_args()
    records, source_hash = read_publications(args.input)
    if len(records) != args.expected_count:
        raise ValueError(f'Found {len(records)} publications, expected {args.expected_count}. '
                         'Set --expected-count explicitly if the corpus changed.')
    if not -1 <= args.threshold <= 1 or args.top_pairs < 1:
        raise ValueError('Threshold must be between -1 and 1; top-pairs must be positive')
    print(f'Validated {len(records)} publications; source SHA256 {source_hash}')
    if args.validate_only:
        return

    import numpy as np
    import torch
    import networkx as nx
    import plotly.graph_objects as go
    from sklearn.decomposition import PCA
    from sentence_transformers import SentenceTransformer

    torch.manual_seed(0)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    # This is the only model-loading step. A download failure stops the run.
    model = SentenceTransformer(args.model, revision=args.revision, device='cpu',
                                trust_remote_code=False)
    model.eval()
    tokenizer = model.tokenizer
    capacity = model.max_seq_length - tokenizer.num_special_tokens_to_add(pair=False)
    vectors, diagnostics = [], []
    for record in records:
        text = ' '.join((record['title'] + '\n' + record['abstract']).split())
        ids = tokenizer.encode(text, add_special_tokens=False, truncation=False)
        windows = token_windows(ids, capacity, args.overlap)
        chunk_vectors, weights = [], []
        for tokens, weight in windows:
            # Pass original token IDs directly: no decode/re-tokenize drift or truncation.
            features = tokenizer.prepare_for_model(tokens, add_special_tokens=True,
                                                    truncation=False, return_tensors='pt')
            if features['input_ids'].shape[1] > model.max_seq_length:
                raise AssertionError('Window exceeds model limit')
            with torch.inference_mode():
                vector = model(dict(features))['sentence_embedding'][0].cpu().numpy()
            chunk_vectors.append(vector / np.linalg.norm(vector))
            weights.append(weight)
        vector = np.average(chunk_vectors, axis=0, weights=weights)
        vectors.append(vector / np.linalg.norm(vector))
        diagnostics.append(dict(id=record['id'], tokens=len(ids), windows=len(windows),
                                window_weights=weights))

    embeddings = np.asarray(vectors)
    if not np.isfinite(embeddings).all():
        raise ValueError('Non-finite embeddings')
    similarities = np.clip(embeddings @ embeddings.T, -1, 1)
    if not np.allclose(np.diag(similarities), 1) or not np.allclose(similarities, similarities.T):
        raise AssertionError('Invalid cosine matrix')
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    (out / 'publications.json').write_text(json.dumps(records, ensure_ascii=False, indent=2))
    write_csv(out / 'publications.csv', records, list(records[0]))
    np.save(out / 'embeddings.npy', embeddings)
    ids = [r['id'] for r in records]
    with (out / 'similarity_matrix.csv').open('w', newline='') as handle:
        writer = csv.writer(handle)
        writer.writerow(['id'] + ids)
        writer.writerows([[ids[i]] + list(row) for i, row in enumerate(similarities)])
    pairs = [dict(id_a=ids[i], id_b=ids[j], title_a=records[i]['title'],
                  title_b=records[j]['title'], cosine_similarity=float(similarities[i, j]))
             for i in range(len(ids)) for j in range(i + 1, len(ids))]
    pairs.sort(key=lambda pair: (-pair['cosine_similarity'], pair['id_a'], pair['id_b']))
    write_csv(out / 'all_pairs.csv', pairs, list(pairs[0]))
    write_csv(out / 'most_similar_pairs.csv', pairs[:args.top_pairs], list(pairs[0]))

    hover = [f"{r['id']}: {r['title']} ({r['year']})" for r in records]
    pca = PCA(n_components=2, svd_solver='full')
    coordinates = pca.fit_transform(embeddings)
    write_csv(out / 'pca_coordinates.csv',
              [dict(id=ids[i], PC1=float(x), PC2=float(y)) for i, (x, y) in enumerate(coordinates)],
              ['id', 'PC1', 'PC2'])
    fig = go.Figure(go.Scatter(x=coordinates[:, 0], y=coordinates[:, 1], mode='markers+text',
                              text=ids, textposition='top center', hovertext=hover,
                              hoverinfo='text', marker=dict(size=13, color=[r['year'] for r in records],
                                                          colorscale='Viridis', showscale=True)))
    explained = pca.explained_variance_ratio_
    fig.update_layout(title='Publication embeddings: PCA projection',
                      xaxis_title=f'PC1 ({explained[0]:.1%} variance)',
                      yaxis_title=f'PC2 ({explained[1]:.1%} variance)')
    fig.write_html(out / 'pca.html', include_plotlyjs=True)

    graph = nx.Graph()
    graph.add_nodes_from(ids)
    for pair in pairs:
        if pair['cosine_similarity'] >= args.threshold:
            graph.add_edge(pair['id_a'], pair['id_b'], weight=pair['cosine_similarity'])
    positions = nx.spring_layout(graph, seed=42, weight='weight', iterations=200)
    network = go.Figure()
    for a, b, data in graph.edges(data=True):
        x0, y0 = positions[a]; x1, y1 = positions[b]
        network.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode='lines',
                          line=dict(width=1 + 3 * data['weight'], color='#aab5c0'),
                          hoverinfo='skip', showlegend=False))
        network.add_trace(go.Scatter(x=[(x0+x1)/2], y=[(y0+y1)/2], mode='markers',
                          marker=dict(size=8, opacity=0), showlegend=False,
                          hovertext=f"{a}–{b}: {data['weight']:.4f}", hoverinfo='text'))
    network.add_trace(go.Scatter(x=[positions[i][0] for i in ids], y=[positions[i][1] for i in ids],
                     mode='markers+text', text=ids, textposition='top center', hovertext=hover,
                     hoverinfo='text', marker=dict(size=16, color=[r['year'] for r in records],
                     colorscale='Viridis', showscale=True), showlegend=False))
    network.update_layout(title=f'Publication network: cosine ≥ {args.threshold:.2f}',
                          xaxis=dict(visible=False), yaxis=dict(visible=False))
    network.write_html(out / 'network.html', include_plotlyjs=True)
    heatmap = go.Figure(go.Heatmap(z=similarities, x=ids, y=ids, zmin=-1, zmax=1,
                                 colorscale='RdBu', reversescale=True))
    heatmap.update_layout(title='Pairwise cosine similarity (see publications.csv for IDs)')
    heatmap.write_html(out / 'similarity_heatmap.html', include_plotlyjs=True)
    metadata = dict(source=str(args.input), source_sha256=source_hash, model=args.model,
                    revision=args.revision, count=len(records), dimensions=embeddings.shape[1],
                    max_sequence_length=model.max_seq_length, token_capacity=capacity,
                    overlap=args.overlap, diagnostics=diagnostics, threshold=args.threshold,
                    layout_seed=42, pca_explained_variance_ratio=explained.tolist(),
                    preprocessing='title + newline + abstract; collapse whitespace; preserve case/punctuation',
                    aggregation='L2-normalize window vectors; mean weighted by newly covered tokens; L2-normalize',
                    packages={name: importlib.metadata.version(name) for name in
                              ['sentence-transformers','transformers','torch','numpy','scikit-learn',
                               'PyYAML','plotly','networkx']})
    (out / 'run_metadata.json').write_text(json.dumps(metadata, indent=2))
    print(f'Wrote {len(pairs)} pairs and {len(ids)} × {len(ids)} matrix to {out}')


if __name__ == '__main__':
    main()
