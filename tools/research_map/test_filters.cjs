/* Offline interaction regression checks using the committed genuine publication data. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {JSDOM} = require('jsdom');
const root = path.resolve(__dirname, '../..');
const data = JSON.parse(fs.readFileSync(path.join(root, '_data/research_map.json'), 'utf8'));

(async () => {
  const dom = new JSDOM(fs.readFileSync(path.join(root, '_pages/research.html'), 'utf8'), {
    runScripts: 'outside-only', url: 'https://example.org/research/'
  });
  const {window} = dom;
  window.fetch = async () => ({ok: true, json: async () => data});
  window.matchMedia = () => ({matches: false});
  await window.eval(fs.readFileSync(path.join(root, 'assets/js/research-map.js'), 'utf8'));
  const doc = window.document;
  const marks = [...doc.querySelectorAll('.research__point')];
  const chips = [...doc.querySelectorAll('.research__chip')];
  const slider = doc.getElementById('research-year');
  const allYears = doc.getElementById('research-all-years');
  const transforms = marks.map(mark => mark.getAttribute('transform'));
  const shown = () => data.publications.filter((_, i) => marks[i].style.display !== 'none').map(p => p.id);
  const setYear = year => { slider.value = year; slider.dispatchEvent(new window.Event('input')); };
  const select = id => marks[data.publications.findIndex(p => p.id === id)].dispatchEvent(new window.MouseEvent('click'));
  const reset = () => { allYears.checked = true; allYears.dispatchEvent(new window.Event('change')); doc.getElementById('research-show-all').click(); };
  assert.equal(allYears.checked, true);
  assert.equal(shown().length, 15);
  assert.equal(chips.length, 4);
  assert.ok(chips.every(chip => chip.getAttribute('aria-pressed') === 'true'));
  for (let year = 2016; year <= 2026; year++) {
    setYear(year);
    assert.equal(allYears.checked, false);
    assert.deepEqual(shown(), data.publications.filter(p => p.year <= year).map(p => p.id));
    assert.equal(doc.getElementById('research-year-label').textContent, String(year));
    // Check every year against each researcher-defined theme in isolation.
    for (let theme = 0; theme < chips.length; theme++) {
      chips.forEach((chip, i) => {
        if ((chip.getAttribute('aria-pressed') === 'true') !== (i === theme)) chip.click();
      });
      const expected = data.publications.filter(p => p.year <= year && p.theme === data.themes[theme].id).map(p => p.id);
      assert.deepEqual(shown(), expected);
      assert.equal([...doc.querySelectorAll('#research-publication-list li')].filter(li => !li.hidden).length, expected.length);
    }
    doc.getElementById('research-show-all').click();
    assert.deepEqual(marks.map(mark => mark.getAttribute('transform')), transforms);
  }
  reset();
  select('P01');
  setYear(2025);
  assert.equal(doc.querySelectorAll('[aria-pressed="true"].research__point').length, 0);
  assert.match(doc.getElementById('research-detail').textContent, /outside the current filters/);
  assert.equal(doc.querySelectorAll('.research__connection').length, 0);
  reset();
  chips[0].click();
  setYear(2022);
  select('P09');
  const p09 = data.publications.find(p => p.id === 'P09');
  assert.equal(doc.querySelector('h4').textContent, 'Most related publications (by textual similarity)');
  assert.deepEqual([...doc.querySelectorAll('#research-detail li button')].map(b => b.textContent),
    p09.closest.map(n => data.publications.find(p => p.id === n.id).title));
  assert.equal(doc.querySelectorAll('.research__connection').length, 0);
  assert.equal([...doc.querySelectorAll('[data-outside-id]')].filter(n => !n.hidden).length, 3);
  doc.querySelector('#research-detail li button').click();
  const neighbor = data.publications.find(p => p.id === p09.closest[0].id);
  assert.equal(doc.getElementById('research-detail-heading').textContent, neighbor.title);
  assert.ok(Number(slider.value) >= neighbor.year);
  assert.ok(shown().includes(neighbor.id));
  reset();
  for (const p of data.publications) {
    select(p.id);
    assert.equal(doc.querySelector('.research__abstract').textContent, p.abstract);
    const toggle = doc.querySelector('.research__abstract-toggle');
    assert.equal(toggle.getAttribute('aria-expanded'), 'false');
    toggle.click();
    assert.equal(doc.querySelector('.research__abstract').hidden, false);
    assert.equal(toggle.getAttribute('aria-expanded'), 'true');
    assert.deepEqual([...doc.querySelectorAll('.research__connection')].map(n => n.dataset.neighbor), p.closest.map(n => n.id));
  }
  chips.forEach(chip => chip.click());
  assert.deepEqual(shown(), []);
  assert.match(doc.getElementById('research-count').textContent, /0 of 15/);
  console.log('Passed: all 11 year cutoffs × 4 themes, inclusive years, reset, empty states, selection clearing/reveal, genuine rankings/abstracts, and fixed PCA transforms.');
  window.close();
})().catch(error => { console.error(error); process.exitCode = 1; });
