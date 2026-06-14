let pyodide = null;
let pyReady = false;
let categoryMap = {};
let allProperties = [];
let searchPage = 0;
const SEARCH_PAGE_SIZE = 50;
let searchResultsAll = [];
let batchMode = false;

// ── Utility ──────────────────────────────────────────────────────────────

function $(id) { return document.getElementById(id); }

function toast(msg, duration = 2500) {
  const el = $('toast');
  el.textContent = msg;
  el.classList.remove('show');
  void el.offsetWidth;
  el.classList.add('show');
  clearTimeout(el._timer);
  el._timer = setTimeout(() => el.classList.remove('show'), duration);
}

function setProgress(pct, text) {
  $('progress-bar').style.width = pct + '%';
  $('loader-text').textContent = text;
}

function requireReady() {
  if (!pyReady) { toast('Python still loading...'); return false; }
  return true;
}

// ── Tab Switching ────────────────────────────────────────────────────────

function switchTab(name) {
  const names = ['classify', 'search', 'compare', 'notd'];
  document.querySelectorAll('.tab').forEach((t, i) => {
    t.classList.toggle('active', names[i] === name);
  });
  document.querySelectorAll('.tab-panel').forEach(p => {
    p.classList.remove('active');
  });
  const panel = $('tab-' + name);
  panel.classList.add('active');
  // Re-trigger animation by removing/re-adding
  panel.style.animation = 'none';
  void panel.offsetWidth;
  panel.style.animation = '';
}

// ── Ripple Effect ────────────────────────────────────────────────────────

function applyRipple(e) {
  const btn = e.currentTarget;
  const rect = btn.getBoundingClientRect();
  const x = ((e.clientX - rect.left) / rect.width * 100).toFixed(1);
  const y = ((e.clientY - rect.top) / rect.height * 100).toFixed(1);
  btn.style.setProperty('--ripple-x', x + '%');
  btn.style.setProperty('--ripple-y', y + '%');
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.btn').forEach(b => b.addEventListener('mousedown', applyRipple));
});

// ── History ──────────────────────────────────────────────────────────────

function getHistory() {
  try { return JSON.parse(localStorage.getItem('nc_history') || '[]'); }
  catch { return []; }
}

function saveHistory(entry) {
  let h = getHistory();
  h = h.filter(e => e.n !== entry.n);
  h.unshift(entry);
  if (h.length > 20) h = h.slice(0, 20);
  localStorage.setItem('nc_history', JSON.stringify(h));
  renderHistory();
}

function clearHistory() {
  localStorage.removeItem('nc_history');
  renderHistory();
}

function renderHistory() {
  const h = getHistory();
  const container = $('history-items');
  const clearBtn = $('clear-history');
  if (!container) return;
  if (!h.length) {
    container.innerHTML = '<span class="empty-state" style="font-size:12px;">No history yet.</span>';
    if (clearBtn) clearBtn.style.display = 'none';
    return;
  }
  if (clearBtn) clearBtn.style.display = 'inline-block';
  container.innerHTML = h.map(e =>
    `<div class="history-item" onclick="recallHistory(${e.n})">
      <span class="h-num">${e.n}</span>
      <span class="h-score">${e.score} properties</span>
    </div>`
  ).join('');
}

function recallHistory(n) {
  $('input-classify').value = n;
  switchTab('classify');
  doClassify(n);
}

function toggleHistory() {
  const p = $('history-panel');
  const t = $('history-toggle-text');
  p.classList.toggle('open');
  t.textContent = p.classList.contains('open') ? '▼' : '▶';
}

// ── Tags ─────────────────────────────────────────────────────────────────

function getTagColor(category) {
  const colors = {
    primes: 'var(--cat-primes)',
    figurate: 'var(--cat-figurate)',
    centered_figurate: 'var(--cat-centered_figurate)',
    digital_invariants: 'var(--cat-digital_invariants)',
    divisors: 'var(--cat-divisors)',
    sequences: 'var(--cat-sequences)',
    powers: 'var(--cat-powers)',
    number_theory: 'var(--cat-number_theory)',
    combinatorial: 'var(--cat-combinatorial)',
    recreational: 'var(--cat-recreational)',
  };
  return colors[category] || 'var(--saffron)';
}

function makeTags(props, container, delayBase = 0) {
  container.innerHTML = '';
  if (!props || !props.length) {
    container.innerHTML = '<span class="empty-state">No matching properties found.</span>';
    return;
  }
  props.forEach((p, i) => {
    const tag = document.createElement('span');
    tag.className = 'tag';
    const name = typeof p === 'string' ? p : p.name;
    const cat = typeof p === 'object' ? p.category : (categoryMap[name] || '');
    tag.textContent = name.replace(/_/g, ' ');
    if (cat) {
      tag.dataset.category = cat;
      tag.style.setProperty('--tag-color', getTagColor(cat));
    }
    const rot = (Math.random() - 0.5) * 3;
    tag.style.setProperty('--tag-rotate', rot + 'deg');
    tag.style.animationDelay = (delayBase + i * 20) + 'ms';
    // Tooltip
    if (cat) {
      const tip = document.createElement('span');
      tip.className = 'tag-tooltip';
      tip.innerHTML = `<span class="tt-category">${cat.replace(/_/g, ' ')}</span>`;
      tag.appendChild(tip);
    }
    container.appendChild(tag);
  });
}

// ── Score Counter Animation ──────────────────────────────────────────────

function animateScore(target, duration = 400) {
  const counter = document.querySelector('#classify-score .score-count');
  if (!counter) return;
  const start = performance.now();
  function step(now) {
    const t = Math.min((now - start) / duration, 1);
    const ease = 1 - Math.pow(1 - t, 3);
    const current = Math.round(target * ease);
    counter.textContent = current;
    if (t < 1) requestAnimationFrame(step);
    else {
      counter.textContent = target;
      const badge = $('classify-score');
      badge.classList.remove('pulse');
      void badge.offsetWidth;
      badge.classList.add('pulse');
    }
  }
  requestAnimationFrame(step);
}

// ── Number Digit Animation ───────────────────────────────────────────────

function renderNumber(el, num) {
  const digits = String(num).split('');
  el.innerHTML = digits.map((d, i) =>
    `<span class="digit" style="animation-delay:${i * 40}ms">${d}</span>`
  ).join('');
}

// ── Pyodide Init ─────────────────────────────────────────────────────────

async function initPyodide() {
  setProgress(10, 'Loading Python runtime (one-time, ~10MB)...');
  pyodide = await loadPyodide();

  setProgress(50, 'Loading micropip...');
  await pyodide.loadPackage('micropip');

  setProgress(70, 'Installing numclassify...');
  await pyodide.runPythonAsync(`
import micropip
await micropip.install('numclassify')
import numclassify as nc
import json, random, math
`);

  // Fetch category map
  try {
    const catData = await pyodide.runPythonAsync(`
import json
from numclassify._registry import REGISTRY
m = {v["name"]: v.get("category", "") for v in REGISTRY.values()}
json.dumps(m)
`);
    categoryMap = JSON.parse(catData);
    allProperties = Object.keys(categoryMap);
  } catch(e) {
    console.warn('Could not load category map', e);
  }

  // Fetch version number — prefer local source version as canonical
  const badge = $('version-badge');
  const srcVersion = badge ? badge.dataset.version : null;
  try {
    const pypiVer = await pyodide.runPythonAsync('nc.__version__');
    // Use the source version (from pyproject.toml) since PyPI may lag behind
    $('version-text').textContent = srcVersion || pypiVer;
    if (srcVersion && pypiVer !== srcVersion) {
      badge.title = 'Source: v' + srcVersion + '  |  PyPI: v' + pypiVer;
    }
  } catch(e) {
    $('version-text').textContent = srcVersion || '?';
  }

  setProgress(100, 'Ready!');
  await new Promise(r => setTimeout(r, 400));

  $('loader').style.display = 'none';
  $('app').style.display = 'block';
  pyReady = true;

  renderHistory();

  const params = new URLSearchParams(window.location.search);
  const n = params.get('n');
  if (n !== null && !isNaN(parseInt(n))) {
    $('input-classify').value = n;
    doClassify(n);
  }

  computeNOTD();
}

// ── Classify ─────────────────────────────────────────────────────────────

async function doClassify(n = null) {
  if (!requireReady()) return;
  // If no explicit number and input contains commas/spaces, go to batch mode
  if (n === null) {
    const raw = $('input-classify').value.trim();
    if (raw.includes(',') || /\s/.test(raw)) {
      return doBatchClassify();
    }
  }
  const val = n !== null ? n : parseInt($('input-classify').value);
  if (isNaN(val)) { toast('Enter a valid integer.'); return; }

  const btn = $('btn-classify');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Classifying...';

  try {
    const result = await pyodide.runPythonAsync(`
import json
r = nc.classify(${val})
json.dumps({"number": r["number"], "score": r["notable_score"], "total_score": r["score"], "props": r["true_properties"]})
`);
    const data = JSON.parse(result);

    batchMode = false;
    renderNumber($('classify-number'), data.number);
    animateScore(data.score);
    makeTags(data.props, $('classify-tags'));
    $('batch-actions').style.display = '';
    if (data.score > 50) burstConfetti();

    const res = $('result-classify');
    res.style.display = 'block';
    res.classList.remove('show');
    void res.offsetWidth;
    res.classList.add('show');

    // Save history
    saveHistory({ n: data.number, score: data.score });

    // Update URL silently
    const url = new URL(window.location);
    url.searchParams.set('n', val);
    window.history.replaceState({}, '', url);

  } catch(e) {
    toast('Error: ' + e.message.slice(0, 80));
  } finally {
    btn.disabled = false;
    btn.textContent = 'Classify';
  }
}

async function doRandom() {
  if (!requireReady()) return;
  const n = await pyodide.runPythonAsync(`nc.random_number()["number"]`);
  $('input-classify').value = n;
  await doClassify(n);
}

// ── Batch Classify ───────────────────────────────────────────────────────

async function doBatchClassify() {
  if (!requireReady()) return;
  const raw = $('input-classify').value.trim();
  if (!raw) { toast('Enter numbers.'); return; }
  const nums = raw.split(/[,\s]+/).map(s => parseInt(s)).filter(n => !isNaN(n));
  if (!nums.length) { toast('No valid numbers.'); return; }
  if (nums.length > 50) { toast('Max 50 numbers at once.'); return; }

  const btn = $('btn-classify');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Classifying...';

  try {
    const result = await pyodide.runPythonAsync(`
import json
nums = ${JSON.stringify(nums)}
results = [nc.classify(n) for n in nums]
json.dumps(results)
`);
    const results = JSON.parse(result);

    batchMode = true;
    const res = $('result-classify');
    res.style.display = 'block';
    res.classList.remove('show');
    void res.offsetWidth;
    res.classList.add('show');

    $('classify-number').innerHTML = `<span style="font-size:24px;background:none;-webkit-text-fill-color:var(--saffron);color:var(--saffron)">Batch (${results.length})</span>`;
    $('classify-score').innerHTML = '<span class="score-count"></span>';
    $('batch-actions').style.display = 'none';

    let html = '<table class="batch-table"><thead><tr><th>Number</th><th>Score</th><th>Properties</th></tr></thead><tbody>';
    results.forEach(r => {
      const tags = r.true_properties.slice(0, 8).map(p => p.replace(/_/g, ' ')).join(', ');
      const more = r.true_properties.length > 8 ? ` +${r.true_properties.length - 8} more` : '';
      html += `<tr><td class="b-num" onclick="recallHistory(${r.number})">${r.number}</td><td>${r.notable_score}</td><td class="b-tags">${tags}${more}</td></tr>`;
    });
    html += '</tbody></table>';
    $('classify-tags').innerHTML = html;

    results.forEach(r => saveHistory({ n: r.number, score: r.notable_score }));

  } catch(e) {
    toast('Error: ' + e.message.slice(0, 80));
  } finally {
    btn.disabled = false;
    btn.textContent = 'Classify';
  }
}

// ── Search ───────────────────────────────────────────────────────────────

async function doSearch(page = 0) {
  if (!requireReady()) return;
  const prop = $('input-property').value.trim().toLowerCase();
  const start = parseInt($('input-range-start').value) || 1;
  const end = parseInt($('input-range-end').value) || 1000;

  if (!prop) { toast('Enter a property name.'); return; }
  if (end - start > 10000) { toast('Range too large. Max 10000.'); return; }

  const countEl = $('search-count');
  const resultsEl = $('search-results');
  const loadMoreEl = $('load-more');
  const suggestEl = $('did-you-mean');

  if (page === 0) {
    countEl.innerHTML = '<span class="spinner"></span> Searching...';
    $('result-search').style.display = 'block';
    $('result-search').classList.remove('show');
    void $('result-search').offsetWidth;
    $('result-search').classList.add('show');
    resultsEl.innerHTML = '';
    loadMoreEl.style.display = 'none';
    suggestEl.style.display = 'none';
  }

  try {
    if (page === 0) {
      const result = await pyodide.runPythonAsync(`
import json
nums = [n for n in range(${start}, ${end}+1) if nc.get_all_properties(n).get("${prop.replace(/"/g, '')}", False)]
json.dumps(nums)
`);
      searchResultsAll = JSON.parse(result);
      searchPage = 0;

      // Fuzzy suggestion if 0 results
      if (!searchResultsAll.length) {
        const match = fuzzyFind(prop, allProperties);
        if (match) {
          suggestEl.innerHTML = `Did you mean <strong>${match.replace(/_/g, ' ')}</strong>?`;
          suggestEl.dataset.prop = match;
          suggestEl.style.display = 'block';
        }
      } else {
        suggestEl.style.display = 'none';
      }
    }

    renderSearchPage();
  } catch(e) {
    toast('Error: ' + e.message.slice(0, 80));
    countEl.textContent = 'Error during search.';
  }
}

function renderSearchPage() {
  const countEl = $('search-count');
  const resultsEl = $('search-results');
  const loadMoreEl = $('load-more');
  const total = searchResultsAll.length;
  const start = searchPage * SEARCH_PAGE_SIZE;
  const pageItems = searchResultsAll.slice(start, start + SEARCH_PAGE_SIZE);

  countEl.textContent = `Found ${total} numbers${total > SEARCH_PAGE_SIZE ? ` (showing ${start + 1}–${Math.min(start + SEARCH_PAGE_SIZE, total)})` : ''} with property "${$('input-property').value.trim()}"`;

  pageItems.forEach((n, i) => {
    const el = document.createElement('div');
    el.className = 'search-num';
    el.textContent = n;
    el.style.animationDelay = (i * 25) + 'ms';
    el.onclick = () => {
      $('input-classify').value = n;
      switchTab('classify');
      doClassify(n);
    };
    resultsEl.appendChild(el);
  });

  searchPage++;
  if (start + SEARCH_PAGE_SIZE >= total) {
    loadMoreEl.style.display = 'none';
  } else {
    loadMoreEl.style.display = 'block';
  }
}

function loadMoreSearch() {
  renderSearchPage();
}

// ── Fuzzy Search ─────────────────────────────────────────────────────────

function levenshtein(a, b) {
  const m = a.length, n = b.length;
  const dp = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));
  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;
  for (let i = 1; i <= m; i++)
    for (let j = 1; j <= n; j++)
      dp[i][j] = a[i-1] === b[j-1] ? dp[i-1][j-1] : 1 + Math.min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]);
  return dp[m][n];
}

function fuzzyFind(input, candidates) {
  const norm = input.replace(/[\s-]/g, '_').toLowerCase();
  let best = null, bestDist = Infinity;
  for (const c of candidates) {
    const d = levenshtein(norm, c);
    if (d < bestDist && d <= Math.min(4, Math.floor(c.length / 3))) {
      bestDist = d;
      best = c;
    }
  }
  return best;
}

function applySuggestion(el) {
  const prop = el.dataset.prop;
  if (prop) {
    $('input-property').value = prop;
    doSearch();
  }
}

// ── Compare ──────────────────────────────────────────────────────────────

async function doCompare() {
  if (!requireReady()) return;
  const a = parseInt($('input-compare-a').value);
  const b = parseInt($('input-compare-b').value);
  if (isNaN(a) || isNaN(b)) { toast('Enter two valid integers.'); return; }

  try {
    const result = await pyodide.runPythonAsync(`
import json
pa = set(nc.get_true_properties(${a}))
pb = set(nc.get_true_properties(${b}))
shared = sorted(pa & pb)
only_a = sorted(pa - pb)
only_b = sorted(pb - pa)
json.dumps({"only_a": only_a, "only_b": only_b, "shared": shared})
`);
    const data = JSON.parse(result);

    $('compare-title-a').textContent = a;
    $('compare-title-b').textContent = b;

    const sharedEl = $('compare-shared');
    if (!data.shared.length) {
      sharedEl.innerHTML = '<span class="empty-state">No shared properties — these numbers are mathematically unrelated.</span>';
    } else {
      makeTags(data.shared, sharedEl);
    }

    const onlyAEl = $('compare-only-a');
    if (!data.only_a.length) {
      onlyAEl.innerHTML = '<span class="empty-state">No unique properties.</span>';
    } else {
      makeTags(data.only_a, onlyAEl);
    }

    const onlyBEl = $('compare-only-b');
    if (!data.only_b.length) {
      onlyBEl.innerHTML = '<span class="empty-state">No unique properties.</span>';
    } else {
      makeTags(data.only_b, onlyBEl);
    }

    $('result-compare').style.display = 'block';
    $('result-compare').classList.remove('show');
    void $('result-compare').offsetWidth;
    $('result-compare').classList.add('show');

  } catch(e) {
    toast('Error: ' + e.message.slice(0, 80));
  }
}

// ── Number of the Day ────────────────────────────────────────────────────

async function computeNOTD(dateStr) {
  if (!pyReady) return;
  try {
    if ($('notd-content')) $('notd-content').style.display = 'none';
    if ($('notd-loading')) $('notd-loading').style.display = 'block';

    const dateParam = dateStr ? `"${dateStr}"` : 'None';
    const result = await pyodide.runPythonAsync(`
import json, datetime, random as _random
if ${dateParam} is not None:
    parts = ${dateParam}.split("-")
    today = datetime.date(int(parts[0]), int(parts[1]), int(parts[2]))
else:
    today = datetime.date.today()
seed = today.year * 10000 + today.month * 100 + today.day
_random.seed(seed)
n = _random.randint(1, 9999)
r = nc.classify(n)
json.dumps({"number": r["number"], "score": r["notable_score"], "props": r["true_properties"][:12]})
`);
    const data = JSON.parse(result);
    $('notd-number').textContent = data.number;
    makeTags(data.props, $('notd-tags'));
    $('notd-loading').style.display = 'none';
    $('notd-content').style.display = 'block';
  } catch(e) {
    if ($('notd-loading')) $('notd-loading').textContent = 'Could not compute today\'s number.';
  }
}

function classifyNotd() {
  const n = parseInt($('notd-number').textContent);
  $('input-classify').value = n;
  switchTab('classify');
  doClassify(n);
}

function onNotdDateChange(input) {
  computeNOTD(input.value);
}

// ── Copy & Share & Download ──────────────────────────────────────────────

async function copyResults() {
  if (batchMode) { toast('Cannot copy batch results — classify a single number first.'); return; }
  const num = $('classify-number').textContent;
  const score = $('classify-score').textContent;
  const tags = [...$('classify-tags').querySelectorAll('.tag')].map(t => t.textContent).join(', ');
  const text = `numclassify: ${num}\n${score}\n\n${tags}`;
  try {
    await navigator.clipboard.writeText(text);
    const btn = document.querySelector('.btn-icon[onclick*="copyResults"]');
    if (btn) { btn.classList.add('success'); setTimeout(() => btn.classList.remove('success'), 1500); }
    toast('Copied to clipboard!');
  } catch {
    toast('Copy failed — try selecting manually.');
  }
}

function shareURL() {
  const url = window.location.href;
  navigator.clipboard.writeText(url).then(() => {
    const hint = $('share-hint');
    $('share-url-text').textContent = url;
    hint.style.display = 'inline-block';
    toast('Share URL copied!');
    setTimeout(() => hint.style.display = 'none', 5000);
  });
}

function downloadJSON() {
  if (batchMode) { toast('Cannot download batch results — classify a single number first.'); return; }
  const num = $('classify-number').textContent;
  const scoreEl = document.querySelector('#classify-score .score-count');
  const score = scoreEl ? parseInt(scoreEl.textContent) || 0 : 0;
  const tags = [...$('classify-tags').querySelectorAll('.tag')].map(t => t.textContent);
  const data = { number: parseInt(num) || num, score, properties: tags };
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `numclassify_${num}.json`;
  a.click();
  URL.revokeObjectURL(url);
  toast('Downloaded!');
}

// ── Theme Toggle ─────────────────────────────────────────────────────────

function toggleTheme() {
  const html = document.documentElement;
  const current = html.getAttribute('data-theme');
  const next = current === 'light' ? '' : 'light';
  html.setAttribute('data-theme', next);
  $('theme-icon').textContent = next === 'light' ? '☀️' : '🌙';
  localStorage.setItem('nc_theme', next);
}

// ── Scroll to Top ────────────────────────────────────────────────────────

window.addEventListener('scroll', () => {
  const btn = $('scroll-top');
  if (window.scrollY > 400) btn.classList.add('visible');
  else btn.classList.remove('visible');
});

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ── Search Autocomplete ───────────────────────────────────────────────────

function setupAutocomplete() {
  const input = $('input-property');
  if (!input) return;
  const dropdown = $('ac-dropdown');
  let selectedIdx = -1;

  input.addEventListener('input', async () => {
    const val = input.value.trim().toLowerCase();
    if (!val) { dropdown.classList.remove('open'); return; }

    // Fallback: if allProperties is empty (Pyodide category fetch failed), try on-the-fly
    if (!allProperties.length && pyReady && pyodide) {
      try {
        const sample = await pyodide.runPythonAsync(`
import json
from numclassify._registry import REGISTRY
keys = list(REGISTRY.keys())
json.dumps(keys)
`);
        const keys = JSON.parse(sample);
        if (keys.length) {
          allProperties = keys;
          categoryMap = {};
          keys.forEach(k => { categoryMap[k] = ''; });
          console.log('Autocomplete: fallback loaded', keys.length, 'properties');
        }
      } catch(e) {
        console.warn('Autocomplete fallback failed', e);
      }
    }

    const matches = allProperties
      .filter(p => p.includes(val))
      .slice(0, 10);
    if (!matches.length) {
      if (!allProperties.length) {
        dropdown.innerHTML = '<div class="ac-item" style="cursor:default;color:var(--text-muted)">Loading properties...</div>';
        dropdown.classList.add('open');
      } else {
        dropdown.classList.remove('open');
      }
      return;
    }
    selectedIdx = -1;
    dropdown.innerHTML = matches.map((p, i) =>
      `<div class="ac-item${i === 0 ? ' selected' : ''}" data-prop="${p}" onclick="pickAutocomplete('${p}')">
        ${p.replace(/_/g, ' ')}
        <span class="ac-cat">${(categoryMap[p] || '').replace(/_/g, ' ')}</span>
      </div>`
    ).join('');
    dropdown.classList.add('open');
  });

  input.addEventListener('keydown', e => {
    const items = dropdown.querySelectorAll('.ac-item');
    if (!items.length) return;
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      selectedIdx = Math.min(selectedIdx + 1, items.length - 1);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      selectedIdx = Math.max(selectedIdx - 1, -1);
    } else if (e.key === 'Enter' && selectedIdx >= 0) {
      e.preventDefault();
      items[selectedIdx].click();
      return;
    } else return;
    items.forEach((el, i) => el.classList.toggle('selected', i === selectedIdx));
  });

  document.addEventListener('click', e => {
    if (!input.contains(e.target) && !dropdown.contains(e.target)) {
      dropdown.classList.remove('open');
    }
  });
}

function pickAutocomplete(prop) {
  $('input-property').value = prop;
  $('ac-dropdown').classList.remove('open');
  doSearch();
}

// ── Confetti ──────────────────────────────────────────────────────────────

function burstConfetti() {
  const container = document.createElement('div');
  container.className = 'confetti-container';
  const colors = ['#FF9933', '#FF6B6B', '#4ECDC4', '#45B7D1', '#F7DC6F', '#DDA0DD', '#98D8C8', '#BB8FCE', '#FFEAA7', '#4CAF7D'];
  for (let i = 0; i < 80; i++) {
    const piece = document.createElement('div');
    piece.className = 'confetti-piece';
    const size = 4 + Math.random() * 8;
    piece.style.width = size + 'px';
    piece.style.height = size + 'px';
    piece.style.background = colors[Math.floor(Math.random() * colors.length)];
    piece.style.left = Math.random() * 100 + '%';
    piece.style.borderRadius = Math.random() > 0.5 ? '50%' : '2px';
    piece.style.animationDuration = (1.5 + Math.random() * 2) + 's';
    piece.style.animationDelay = Math.random() * 0.5 + 's';
    container.appendChild(piece);
  }
  document.body.appendChild(container);
  setTimeout(() => container.remove(), 3500);
}

// ── Keyboard Shortcuts ────────────────────────────────────────────────────

const SHORTCUT_MAP = {
  c: 'classify',
  s: 'search',
  n: 'notd',
};

function setupShortcuts() {
  document.addEventListener('keydown', e => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    const key = e.key.toLowerCase();
    if (key === '?' || key === 'h') {
      e.preventDefault();
      $('shortcuts-overlay').classList.toggle('open');
      return;
    }
    const tab = SHORTCUT_MAP[key];
    if (tab) {
      e.preventDefault();
      switchTab(tab);
    }
  });
}

function closeShortcuts() {
  $('shortcuts-overlay').classList.remove('open');
}

// ── Init ─────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  // Enter key support
  $('input-classify')?.addEventListener('keydown', e => {
    if (e.key === 'Enter') doClassify();
  });
  $('input-property')?.addEventListener('keydown', e => {
    if (e.key === 'Enter') doSearch();
  });
  $('input-compare-b')?.addEventListener('keydown', e => {
    if (e.key === 'Enter') doCompare();
  });

  // Restore theme
  const savedTheme = localStorage.getItem('nc_theme');
  if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
    if ($('theme-icon')) $('theme-icon').textContent = savedTheme === 'light' ? '☀️' : '🌙';
  }

  setupAutocomplete();
  setupShortcuts();
  initPyodide();
});
