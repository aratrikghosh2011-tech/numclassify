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
  document.querySelectorAll('.tab-panel').forEach(p => {
    p.classList.remove('active');
  });
  document.querySelectorAll('.tab').forEach(t => {
    t.classList.remove('active');
  });
  const panel = document.getElementById('tab-' + name);
  const btn = document.querySelector(`.tab[onclick*="${name}"]`);
  if (panel) {
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        panel.classList.add('active');
      });
    });
  }
  if (btn) btn.classList.add('active');
}

function animateResult(el) {
  el.classList.remove('result-animate');
  void el.offsetWidth;
  el.classList.add('result-animate');
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
  t.textContent = p.classList.contains('open') ? 'v' : '>';
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
    tag.style.setProperty('--tag-index', i);
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
seen = set()
m = {}
for e in REGISTRY.values():
    if e.name not in seen:
        seen.add(e.name)
        m[e.name.lower().replace(' ', '_')] = e.category
json.dumps(m)
`);
    categoryMap = JSON.parse(catData);
    allProperties = Object.keys(categoryMap);
  } catch(e) {
    console.warn('Could not load category map', e);
  }

  // Fetch version number  --  always use live installed version from PyPI
  try {
    const pypiVer = await pyodide.runPythonAsync('nc.__version__');
    $('version-text').textContent = pypiVer;
  } catch(e) {
    $('version-text').textContent = '?';
  }

  setProgress(100, 'Ready!');
  await new Promise(r => setTimeout(r, 400));

  $('loader').style.display = 'none';
  $('app').style.display = 'block';
  setTimeout(startGuide, 600);
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
