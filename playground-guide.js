// â”€â”€ Robot Guide â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

const GUIDE_KEY = 'numclassify_guide_done_v1';

const GUIDE_STEPS = [
  {
    tab: null,
    targetSelector: '.logo-badge',
    text: "ðŸ‘‹ Hey! I'm Byte, your guide. This is the numclassify playground â€” a live Python environment running in your browser. Let me walk you through it. Takes about 30 seconds.",
    position: 'bottom',
  },
  {
    tab: 'classify',
    targetSelector: '#tab-classify .card',
    text: "This is the Classify tab. Type any integer and I'll tell you every mathematical category it belongs to â€” prime, perfect, Armstrong, and 2140+ more. Try 1729.",
    position: 'right',
  },
  {
    tab: 'search',
    targetSelector: '#tab-search .card',
    text: "The Search tab lets you find numbers by type. Want to see the first 10 perfect numbers? Or every Kaprekar number under 10000? This is where you ask.",
    position: 'right',
  },
  {
    tab: 'compare',
    targetSelector: '#tab-compare .card',
    text: "Compare two numbers side by side â€” see which properties they share and which ones are unique to each. Great for spotting mathematical relationships.",
    position: 'right',
  },
  {
    tab: 'why',
    targetSelector: '#tab-why .card',
    text: "My favourite tab. Type a property and a number, and I'll show you the actual math â€” not just True or False, but why. Try: armstrong, 153.",
    position: 'right',
  },
  {
    tab: null,
    targetSelector: null,
    text: "That's everything! The âŒ¨ shortcut overlay (press ?) shows all keyboard shortcuts. Happy classifying. ðŸŽ‰",
    position: 'center',
  },
];

let guideStep = 0;

function startGuide() {
  if (localStorage.getItem(GUIDE_KEY)) return;
  guideStep = 0;
  document.getElementById('guide-overlay').style.display = 'block';
  document.getElementById('guide-bubble').classList.add('walk-in');
  setTimeout(() => {
    document.getElementById('guide-bubble').classList.remove('walk-in');
  }, 600);
  renderGuideStep();
}

function endGuide() {
  localStorage.setItem(GUIDE_KEY, '1');
  const overlay = document.getElementById('guide-overlay');
  overlay.style.opacity = '0';
  overlay.style.transition = 'opacity 0.3s ease';
  setTimeout(() => {
    overlay.style.display = 'none';
    overlay.style.opacity = '';
    overlay.style.transition = '';
  }, 300);
}

function guideNext() {
  const robot = document.getElementById('guide-robot');
  robot.classList.add('waving');
  setTimeout(() => robot.classList.remove('waving'), 450);
  guideStep++;
  if (guideStep >= GUIDE_STEPS.length) {
    endGuide();
    return;
  }
  renderGuideStep();
}

function renderGuideStep() {
  const step = GUIDE_STEPS[guideStep];
  const isLast = guideStep === GUIDE_STEPS.length - 1;

  if (step.tab) switchTab(step.tab);

  document.getElementById('guide-text').textContent = step.text;

  document.getElementById('guide-next').textContent = isLast ? 'Done âœ“' : 'Next â†’';

  const robot = document.getElementById('guide-robot');
  robot.classList.toggle('celebrating', isLast);

  setTimeout(() => positionGuide(step), step.tab ? 500 : 0);
}

function positionGuide(step) {
  const spotlight = document.getElementById('guide-spotlight');
  const bubble    = document.getElementById('guide-bubble');

  if (!step.targetSelector) {
    spotlight.style.opacity = '0';
    bubble.style.top       = '50%';
    bubble.style.left      = '50%';
    bubble.style.transform = 'translate(-50%, -50%)';
    return;
  }

  const target = document.querySelector(step.targetSelector);
  if (!target) { spotlight.style.opacity = '0'; return; }

  target.scrollIntoView({ behavior: 'smooth', block: 'center' });

  setTimeout(() => {
    const rect = target.getBoundingClientRect();
    const pad  = 10;

    spotlight.style.opacity = '1';
    spotlight.style.left    = (rect.left - pad) + 'px';
    spotlight.style.top     = (rect.top  - pad) + 'px';
    spotlight.style.width   = (rect.width  + pad * 2) + 'px';
    spotlight.style.height  = (rect.height + pad * 2) + 'px';

    const bw = 340;
    let bLeft, bTop;

    if (step.position === 'right') {
      bLeft = rect.right + pad + 12;
      bTop  = rect.top;
      if (bLeft + bw > window.innerWidth - 16) {
        bLeft = rect.left - bw - 12 - pad;
      }
    } else {
      bLeft = rect.left;
      bTop  = rect.bottom + pad + 12;
    }

    const bh = document.getElementById('guide-bubble').offsetHeight || 160;
    if (bTop + bh > window.innerHeight - 16) bTop = window.innerHeight - bh - 16;
    if (bTop < 72) bTop = 72;
    if (bLeft < 16) bLeft = 16;
    if (bLeft + bw > window.innerWidth - 16) bLeft = window.innerWidth - bw - 16;

    bubble.style.left      = bLeft + 'px';
    bubble.style.top       = bTop  + 'px';
    bubble.style.transform = 'none';
  }, 400);
}
