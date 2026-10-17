/* Static research map. Coordinates and similarities are never recomputed here. */
(async () => {
  'use strict';
  const root = document.querySelector('[data-research-map]');
  if (!root) return;
  // A local static file bypasses the shared HTML compressor, which would alter
  // whitespace inside embedded JSON abstract strings.
  const response = await fetch(root.dataset.mapUrl, {credentials: 'same-origin'});
  if (!response.ok) throw new Error('Research map data could not be loaded');
  const data = await response.json();
  if (!data || !Array.isArray(data.publications) || !data.publications.length) return;
  const byId = new Map(data.publications.map(p => [p.id, p]));
  const themes = new Map(data.themes.map(t => [t.id, t]));
  const enabled = new Set(themes.keys());
  const svg = document.getElementById('research-map');
  const detail = document.getElementById('research-detail');
  const hover = document.getElementById('research-hover');
  const filters = document.getElementById('research-filters');
  const list = document.getElementById('research-publication-list');
  const marks = new Map(), rows = new Map(), chips = new Map();
  const yearRange = document.getElementById('research-year');
  const allYears = document.getElementById('research-all-years');
  const isVisible = p => enabled.has(p.theme) && (allYears.checked || p.year <= Number(yearRange.value));
  let selected = null;
  const element = (tag, text, className) => {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    if (className) node.className = className;
    return node;
  };
  const svgElement = (tag, attributes) => {
    const node = document.createElementNS('http://www.w3.org/2000/svg', tag);
    Object.entries(attributes).forEach(([key, value]) => node.setAttribute(key, value));
    return node;
  };
  function select(id, moveFocus = true) {
    const p = byId.get(id);
    selected = id;
    // Related papers retain collection-wide rankings. Explicit navigation reveals
    // their theme/year when needed, without moving points or changing any rankings.
    enabled.add(p.theme);
    chips.get(p.theme).setAttribute('aria-pressed', 'true');
    if (!allYears.checked && p.year > Number(yearRange.value)) yearRange.value = String(p.year);
    const theme = themes.get(p.theme);
    detail.replaceChildren();
    detail.append(element('p', `${theme.name} · ${p.year}`, 'research__eyebrow'));
    const heading = element('h3', p.title);
    heading.id = 'research-detail-heading';
    heading.tabIndex = -1;
    detail.append(heading);
    const fullAbstract = element('p', p.abstract, 'research__abstract');
    fullAbstract.id = 'research-full-abstract';
    if (p.abstract.length > 320) {
      const excerpt = p.abstract.slice(0, 320);
      const preview = element('p', excerpt.slice(0, excerpt.lastIndexOf(' ')) + '…', 'research__abstract-preview');
      fullAbstract.hidden = true;
      const toggle = element('button', 'Read full abstract', 'research__abstract-toggle');
      toggle.type = 'button';
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-controls', fullAbstract.id);
      toggle.addEventListener('click', () => {
        const expanded = toggle.getAttribute('aria-expanded') !== 'true';
        toggle.setAttribute('aria-expanded', String(expanded));
        fullAbstract.hidden = !expanded;
        preview.hidden = expanded;
        toggle.textContent = expanded ? 'Show less' : 'Read full abstract';
      });
      detail.append(preview, fullAbstract, toggle);
    } else detail.append(fullAbstract);
    const link = element('a', 'Read publication ↗', 'research__paper');
    link.href = p.link;
    detail.append(link, element('h4', 'Most related publications (by textual similarity)'));
    detail.append(element('p', 'These are relative rankings within my publication collection, not necessarily strong relationships. Connections use similarities in the original embedding space, not distances in the PCA map.', 'research__note'));
    const related = element('ol');
    p.closest.forEach(neighbor => {
      const other = byId.get(neighbor.id);
      const item = element('li');
      const button = element('button', other.title);
      button.type = 'button';
      button.addEventListener('click', () => select(other.id));
      item.append(button, element('small', `${other.year} · Cosine similarity ${neighbor.similarity.toFixed(3)}`));
      const outside = element('small', 'Outside current filters · select to reveal');
      outside.dataset.outsideId = other.id;
      item.append(outside);
      related.append(item);
    });
    detail.append(related);
    update();
    if (moveFocus) {
      heading.focus({preventScroll: true});
      if (window.matchMedia('(max-width: 800px)').matches) {
        detail.scrollIntoView({block: 'start', behavior:
          window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'});
      }
    }
  }
  function update() {
    let count = 0;
    let cleared = false;
    if (selected && !isVisible(byId.get(selected))) {
      selected = null;
      cleared = true;
      detail.replaceChildren(element('p', 'Publication focus', 'research__eyebrow'));
      const heading = element('h3', 'Find a connection');
      heading.id = 'research-detail-heading';
      detail.append(heading, element('p', 'Your selection is outside the current filters. Choose a visible publication on the map or in the title list.'));
    }
    document.getElementById('research-year-label').textContent = yearRange.value;
    yearRange.setAttribute('aria-valuetext', allYears.checked ? 'All years, 2016 to 2026' : `Up to and including ${yearRange.value}`);
    const neighbors = selected ? byId.get(selected).closest : [];
    const closestIds = new Set(neighbors.map(p => p.id));
    connections.replaceChildren();
    if (selected) {
      const origin = byId.get(selected);
      neighbors.forEach(neighbor => {
        const other = byId.get(neighbor.id);
        if (isVisible(other)) connections.append(svgElement('line', {
          x1: x(origin.PC1), y1: y(origin.PC2), x2: x(other.PC1), y2: y(other.PC2),
          class: 'research__connection', 'data-neighbor': other.id
        }));
      });
    }
    data.publications.forEach(p => {
      const visible = isVisible(p);
      marks.get(p.id).style.display = visible ? '' : 'none';
      marks.get(p.id).setAttribute('aria-pressed', String(selected === p.id));
      marks.get(p.id).classList.toggle('is-neighbor', closestIds.has(p.id));
      rows.get(p.id).hidden = !visible;
      if (visible) count++;
    });
    detail.querySelectorAll('[data-outside-id]').forEach(note => { note.hidden = isVisible(byId.get(note.dataset.outsideId)); });
    document.getElementById('research-count').textContent = `${count} of ${data.publications.length} publications shown${count ? '' : ' — adjust the theme or year filters to explore'}.${cleared ? ' Selection cleared by filters.' : ''}`;
    hover.textContent = selected ? `${byId.get(selected).title} (${byId.get(selected).year})` : 'Select a point to explore its connections.';
  }
  data.themes.forEach(theme => {
    const chip = element('button', undefined, 'research__chip');
    chip.type = 'button';
    chip.style.setProperty('--theme-color', theme.color);
    chip.setAttribute('aria-pressed', 'true');
    chip.addEventListener('click', () => {
      if (enabled.has(theme.id)) enabled.delete(theme.id); else enabled.add(theme.id);
      chip.setAttribute('aria-pressed', String(enabled.has(theme.id)));
      update();
    });
    chips.set(theme.id, chip);
    const swatch = element('span', '', 'research__swatch');
    swatch.style.backgroundColor = theme.color;
    swatch.setAttribute('aria-hidden', 'true');
    const check = element('span', '✓', 'research__chip-check');
    check.setAttribute('aria-hidden', 'true');
    chip.append(swatch, document.createTextNode(theme.name), check);
    filters.append(chip);
  });
  document.getElementById('research-show-all').addEventListener('click', () => {
    themes.forEach(theme => { enabled.add(theme.id); chips.get(theme.id).setAttribute('aria-pressed', 'true'); });
    update();
  });
  yearRange.addEventListener('input', () => { allYears.checked = false; update(); });
  allYears.addEventListener('change', () => {
    if (allYears.checked) yearRange.value = yearRange.max;
    update();
  });
  // One uniform affine scale preserves PCA geometry; bounds remain fixed when filtering.
  const xs = data.publications.map(p => p.PC1), ys = data.publications.map(p => p.PC2);
  const xmin = Math.min(...xs), xmax = Math.max(...xs), ymin = Math.min(...ys), ymax = Math.max(...ys);
  const cx = (xmin + xmax) / 2, cy = (ymin + ymax) / 2;
  const scale = Math.min(650 / (xmax - xmin || 1), 360 / (ymax - ymin || 1));
  const x = value => 390 + (value - cx) * scale;
  const y = value => 250 - (value - cy) * scale;
  svg.append(svgElement('line', {x1: 35, y1: 455, x2: 745, y2: 455, class: 'research__axis'}),
             svgElement('line', {x1: 35, y1: 35, x2: 35, y2: 455, class: 'research__axis'}));
  const pc1 = svgElement('text', {x: 745, y: 480, 'text-anchor': 'end', class: 'research__axis-label'});
  pc1.textContent = 'PC1 →';
  const pc2 = svgElement('text', {x: 12, y: 25, class: 'research__axis-label'});
  pc2.textContent = 'PC2 ↑';
  svg.append(pc1, pc2);
  const connections = svgElement('g', {'aria-hidden': 'true'});
  svg.append(connections);
  data.publications.forEach(p => {
    const theme = themes.get(p.theme);
    const mark = svgElement('g', {class: 'research__point', role: 'button', tabindex: '0',
      'aria-label': `${p.title}, ${p.year}. ${theme.name}`, 'aria-pressed': 'false',
      transform: `translate(${x(p.PC1)},${y(p.PC2)})`});
    const title = svgElement('title', {});
    title.textContent = `${p.title} (${p.year})`;
    // Titles live in the native hover tooltip and caption, not overlapping SVG labels.
    mark.append(title, svgElement('circle', {r: 18, class: 'research__halo'}),
      svgElement('circle', {r: 13, fill: theme.color}));
    mark.addEventListener('click', () => select(p.id));
    mark.addEventListener('keydown', event => {
      if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); select(p.id); }
    });
    ['mouseenter', 'focus'].forEach(event => mark.addEventListener(event, () => { hover.textContent = `${p.title} (${p.year})`; }));
    mark.addEventListener('mouseleave', update);
    svg.append(mark);
    marks.set(p.id, mark);
    const item = element('li'), button = element('button', `${p.id} · ${p.title} (${p.year})`);
    button.type = 'button';
    button.addEventListener('click', () => select(p.id));
    item.append(button);
    rows.set(p.id, item);
    list.append(item);
  });
  const variance = data.provenance.pca_explained_variance_ratio;
  if (variance) document.getElementById('research-variance').textContent = `The first two components explain ${(100 * (variance[0] + variance[1])).toFixed(1)}% of embedding variance.`;
  root.querySelector('.research__interactive').hidden = false;
  document.getElementById('research-map-fallback').hidden = true;
  document.querySelector('.research__reading').open = false;
  update();
})().catch(error => { console.warn('Research map unavailable; publication abstracts remain accessible.', error); });
