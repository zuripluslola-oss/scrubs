/* Must Love Scrubs — Tests & Exams engine.
   Four formats:
     • Pop Quiz          — 8 questions, instant feedback per item.
     • Basic Test        — 20 questions, results at the end.
     • NCLEX Mock Test   — 85–150 items, adaptive (CAT) with a stop rule.
     • Specialty Mock    — 100 questions in one clinical area.
   Reuses the .qb-* question rendering (mc / sata / matrix / bowtie), grades
   every item, and reports a pass likelihood + per-topic breakdown. Demo state
   in localStorage. The adaptive logic is a simplified Rasch/IRT model:
   ability is tracked on the same 1–5 difficulty scale the question bank uses,
   the next item is chosen near the current ability, and the exam stops once
   we're statistically confident the candidate is clearly above or below the
   passing standard (or at the 150-item ceiling) — the way the real NCLEX works. */

(function () {
  'use strict';
  var root = document.querySelector('.exam');
  if (!root) return;

  var POOL = JSON.parse(root.querySelector('script[data-tests]').textContent);
  var LET = 'ABCDEFGH';
  function md(s) { return String(s == null ? '' : s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>'); }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }

  var MODES = {
    quiz:      { title: 'Pop Quiz',           n: 8,   adaptive: false, instant: true,  label: 'Quick check' },
    basic:     { title: 'Basic Test',         n: 20,  adaptive: false, instant: false, label: 'Topic test' },
    nclex:     { title: 'NCLEX Mock Test',    min: 85, max: 150, adaptive: true, instant: false, label: 'Adaptive · CAT' },
    specialty: { title: 'Specialty Mock Test', n: 100, adaptive: false, instant: false, label: 'Specialty' }
  };
  var PASS_STANDARD = 3.0;   // the passing line on the 1–5 ability scale

  var setup = root.querySelector('[data-exam-setup]');
  var runner = root.querySelector('[data-exam-run]');
  var bar = root.querySelector('[data-exam-bar]');
  var stage = root.querySelector('[data-exam-stage]');
  var results = root.querySelector('[data-exam-results]');
  var quitBtn = root.querySelector('[data-exam-quit]');

  var cfg, mode, queue, i, answers, timerId, startAt, ability, seField, usedIds;

  /* ---------- build the question sequence for a mode ---------- */
  function poolFor(specialty) {
    var p = POOL.slice();
    if (specialty && specialty !== 'All') p = p.filter(function (q) { return q.cat === specialty; });
    if (!p.length) p = POOL.slice();
    return p;
  }
  // draw n items without immediate repeats (cycles the shuffled pool if n > pool size)
  function draw(pool, n) {
    var out = [], bag = [];
    for (var k = 0; k < n; k++) {
      if (!bag.length) bag = shuffle(pool);
      out.push(bag.pop());
    }
    return out;
  }

  function start(name, specialty) {
    cfg = MODES[name]; mode = name;
    answers = []; i = 0; usedIds = {};
    ability = PASS_STANDARD; // start every candidate at the passing line
    var pool = poolFor(specialty);
    if (cfg.adaptive) { queue = null; adaptivePool = pool; }
    else queue = draw(pool, cfg.n);

    setup.hidden = true; runner.hidden = false; results.hidden = true; stage.hidden = false;
    startAt = Date.now();
    clearInterval(timerId);
    timerId = setInterval(tick, 1000);
    renderQ();
  }

  var adaptivePool = [];
  // adaptive: pick the unused item whose level is closest to current ability
  function nextAdaptive() {
    var target = Math.max(1, Math.min(5, Math.round(ability)));
    var avail = adaptivePool.filter(function (q) { return !usedIds[q.id]; });
    if (!avail.length) { // pool exhausted — allow reuse, reset the used set
      usedIds = {}; avail = adaptivePool.slice();
    }
    avail.sort(function (a, b) { return Math.abs((a.level || 3) - target) - Math.abs((b.level || 3) - target); });
    var best = Math.abs((avail[0].level || 3) - target);
    var band = avail.filter(function (q) { return Math.abs((q.level || 3) - target) === best; });
    var pick = shuffle(band)[0];
    usedIds[pick.id] = true;
    return pick;
  }

  function totalPlanned() { return cfg.adaptive ? cfg.max : cfg.n; }

  function tick() {
    var s = Math.floor((Date.now() - startAt) / 1000);
    var t = Math.floor(s / 60) + ':' + ('0' + (s % 60)).slice(-2);
    var count = cfg.adaptive ? (i + 1) + ' / 85–150' : (i + 1) + ' / ' + cfg.n;
    bar.innerHTML =
      '<span class="ex-mode">' + cfg.title + '</span>' +
      '<span class="ex-prog"><span class="ex-progbar"><i style="width:' +
        Math.round((i) / (cfg.adaptive ? cfg.min : cfg.n) * 100) + '%"></i></span> Q ' + count + '</span>' +
      '<span class="ex-time">⏱ ' + t + '</span>';
  }

  /* ---------- render one question (exam mode: no reveal until submit for quiz; grade-only otherwise) ---------- */
  var current, pick, answered;
  function renderQ() {
    answered = false; pick = null;
    var q = cfg.adaptive ? nextAdaptive() : queue[i];
    current = q;
    tick();
    var body =
      '<span class="qb-cat">' + q.cat + (q.difficulty ? ' · ' + q.difficulty : '') + '</span>' +
      '<p class="qb-stem">' + md(q.stem) + '</p>' +
      (q.type === 'matrix' ? renderMatrix(q) : q.type === 'bowtie' ? renderBowtie(q) : renderOpts(q)) +
      '<div class="qb-actions"><button class="btn btn-coral ex-submit" disabled>' +
        (cfg.instant ? 'Submit answer' : (isLast() ? 'Finish' : 'Next question')) + '</button></div>' +
      '<div class="qb-reveal" hidden></div>';
    stage.innerHTML = '<div class="qb-q">' + body + '</div>';
    if (q.type === 'mc') wireMC();
    else if (q.type === 'sata') wireSATA(q);
    else if (q.type === 'matrix') wireMatrix(q);
    else if (q.type === 'bowtie') wireBowtie(q);
    stage.querySelector('.ex-submit').addEventListener('click', onSubmit);
  }
  function isLast() { return !cfg.adaptive && i + 1 >= cfg.n; }
  function submitBtn() { return stage.querySelector('.ex-submit'); }

  /* ---------- option renderers (shared with the question bank) ---------- */
  function renderOpts(q) {
    var hint = q.type === 'sata' ? '<p class="qb-hint">Select all that apply.</p>' : '';
    var opts = (q.opts || []).map(function (o, k) {
      return '<button class="qb-opt" data-i="' + k + '"><span class="qb-key">' + LET[k] + '</span><span class="qb-txt">' + md(o.t) + '</span></button>';
    }).join('');
    return hint + '<div class="qb-opts">' + opts + '</div>';
  }
  function wireMC() {
    var btns = stage.querySelectorAll('.qb-opt');
    btns.forEach(function (b) { b.addEventListener('click', function () {
      if (answered) return;
      btns.forEach(function (x) { x.classList.remove('sel'); });
      b.classList.add('sel'); pick = parseInt(b.getAttribute('data-i'), 10);
      submitBtn().disabled = false;
    }); });
  }
  function wireSATA(q) {
    pick = {};
    stage.querySelectorAll('.qb-opt').forEach(function (b) { b.addEventListener('click', function () {
      if (answered) return;
      var k = b.getAttribute('data-i');
      if (pick[k]) { delete pick[k]; b.classList.remove('sel'); } else { pick[k] = true; b.classList.add('sel'); }
      submitBtn().disabled = Object.keys(pick).length === 0;
    }); });
  }
  function renderMatrix(q) {
    var head = '<tr><th></th>' + q.cols.map(function (c) { return '<th>' + c + '</th>'; }).join('') + '</tr>';
    var rows = q.rows.map(function (r, ri) {
      var cells = q.cols.map(function (c, ci) { return '<td class="qb-cell"><button data-row="' + ri + '" data-col="' + ci + '" aria-label="' + c + '"></button></td>'; }).join('');
      return '<tr><td class="qb-rlabel">' + md(r.t) + '</td>' + cells + '</tr>';
    }).join('');
    return '<div class="qb-matrix-wrap"><table class="qb-matrix"><thead>' + head + '</thead><tbody>' + rows + '</tbody></table></div>';
  }
  function wireMatrix(q) {
    pick = {};
    stage.querySelectorAll('.qb-cell button').forEach(function (b) { b.addEventListener('click', function () {
      if (answered) return;
      var ri = b.getAttribute('data-row');
      stage.querySelectorAll('.qb-cell button[data-row="' + ri + '"]').forEach(function (x) { x.classList.remove('sel'); });
      b.classList.add('sel'); pick[ri] = parseInt(b.getAttribute('data-col'), 10);
      submitBtn().disabled = Object.keys(pick).length < q.rows.length;
    }); });
  }
  function btGroup(q, key, cls) {
    var g = q[key];
    var chips = g.options.map(function (o, k) { return '<button class="bt-opt" data-grp="' + key + '" data-i="' + k + '">' + md(o.t) + '</button>'; }).join('');
    return '<div class="bt-col ' + cls + '"><span class="bt-label">' + g.prompt + '</span><div class="bt-opts">' + chips + '</div></div>';
  }
  function renderBowtie(q) { return '<div class="bt-grid">' + btGroup(q, 'actions', 'left') + btGroup(q, 'condition', 'mid') + btGroup(q, 'parameters', 'right') + '</div>'; }
  function btComplete(q) { return pick.condition != null && Object.keys(pick.actions).length === (q.actions.pick || 2) && Object.keys(pick.parameters).length === (q.parameters.pick || 2); }
  function wireBowtie(q) {
    pick = { condition: null, actions: {}, parameters: {} };
    stage.querySelectorAll('.bt-opt').forEach(function (b) { b.addEventListener('click', function () {
      if (answered) return;
      var grp = b.getAttribute('data-grp'), k = parseInt(b.getAttribute('data-i'), 10);
      if (grp === 'condition') { stage.querySelectorAll('.bt-opt[data-grp="condition"]').forEach(function (x) { x.classList.remove('sel'); }); b.classList.add('sel'); pick.condition = k; }
      else { var set = pick[grp], cap = q[grp].pick || 2; if (set[k]) { delete set[k]; b.classList.remove('sel'); } else if (Object.keys(set).length < cap) { set[k] = true; b.classList.add('sel'); } }
      submitBtn().disabled = !btComplete(q);
    }); });
  }

  /* ---------- grading ---------- */
  function sameSet(obj, arr) { return Object.keys(obj).length === arr.length && arr.every(function (k) { return obj[k]; }); }
  function grade(q, p) {
    if (q.type === 'mc') return p === q.correct;
    if (q.type === 'sata') { var c = {}; q.correct.forEach(function (k) { c[k] = true; }); return Object.keys(c).length === Object.keys(p).length && q.correct.every(function (k) { return p[k]; }); }
    if (q.type === 'matrix') return q.rows.every(function (r, ri) { return p[ri] === r.correct; });
    if (q.type === 'bowtie') return p.condition === q.condition.correct && sameSet(p.actions, q.actions.correct) && sameSet(p.parameters, q.parameters.correct);
    return false;
  }

  /* ---------- submit / advance ---------- */
  function onSubmit() {
    if (answered) return;
    answered = true;
    var q = current, isCorrect = grade(q, pick);
    answers.push({ q: q, pick: pick, correct: isCorrect });

    // update ability estimate (adaptive): move toward difficulty on a hit, away on a miss
    var step = 0.9 / Math.sqrt(answers.length + 1);
    ability += (isCorrect ? 1 : -1) * step * (0.6 + Math.abs((q.level || 3) - ability) * 0.3);
    ability = Math.max(1, Math.min(5, ability));

    if (cfg.instant) { revealInstant(q, isCorrect); return; } // pop quiz: show rationale now
    advance();
  }

  function advance() {
    i++;
    if (isDone()) { finish(); return; }
    renderQ();
  }
  function isDone() {
    if (!cfg.adaptive) return i >= cfg.n;
    if (i >= cfg.max) return true;               // 150-item ceiling
    if (i < cfg.min) return false;               // must reach 85
    // 95%-confidence stop rule: SE shrinks with items; stop when the band clears the standard
    var se = 1.9 / Math.sqrt(i);
    return Math.abs(ability - PASS_STANDARD) > 1.96 * se;
  }

  // pop-quiz instant reveal (rationale for every option, then Next)
  function revealInstant(q, isCorrect) {
    if (q.type === 'mc') {
      stage.querySelectorAll('.qb-opt').forEach(function (b) { var k = parseInt(b.getAttribute('data-i'), 10); b.disabled = true; if (k === q.correct) b.classList.add('right'); else if (k === pick) b.classList.add('wrong'); });
    } else if (q.type === 'sata') {
      var c = {}; q.correct.forEach(function (k) { c[k] = true; });
      stage.querySelectorAll('.qb-opt').forEach(function (b) { var k = parseInt(b.getAttribute('data-i'), 10); b.disabled = true; var sel = !!pick[k]; if (c[k] && sel) b.classList.add('right'); else if (c[k]) b.classList.add('missed'); else if (sel) b.classList.add('wrong'); });
    }
    var rev = stage.querySelector('.qb-reveal'); rev.hidden = false;
    rev.innerHTML =
      (isCorrect ? '<span class="qb-verdict ok">Correct</span>' : '<span class="qb-verdict no">Not quite</span>') +
      reviewBody(q, pick) +
      (q.tip ? '<div class="qb-tip"><b>📝 Tip.</b> ' + md(q.tip) + '</div>' : '') +
      '<div class="qb-actions"><button class="btn btn-coral ex-next">' + (i + 1 >= cfg.n ? 'See results' : 'Next question') + ' &rarr;</button></div>';
    submitBtn().disabled = true;
    rev.querySelector('.ex-next').addEventListener('click', advance);
  }

  /* ---------- rationale body for review ---------- */
  function reviewBody(q, p) {
    if (q.type === 'mc' || q.type === 'sata') {
      var cset = {}; (q.type === 'sata' ? q.correct : [q.correct]).forEach(function (k) { cset[k] = true; });
      var items = q.opts.map(function (o, k) { return '<li class="' + (cset[k] ? 'ok' : 'no') + '"><b>' + LET[k] + '.</b> ' + md(o.r) + '</li>'; }).join('');
      return '<div class="qb-rationale"><b>Why each option:</b><ul>' + items + '</ul></div>';
    }
    if (q.type === 'matrix') {
      var rrows = q.rows.map(function (r) { return '<li class="ok"><b>' + md(r.t) + '</b> — ' + md(r.r || q.cols[r.correct]) + '</li>'; }).join('');
      return '<div class="qb-rationale"><b>Why each row:</b><ul>' + rrows + '</ul></div>';
    }
    if (q.type === 'bowtie') {
      function part(g, isC) { var li = g.options.map(function (o, k) { return '<li class="' + (isC(k) ? 'ok' : 'no') + '"><b>' + md(o.t) + ':</b> ' + md(o.r) + '</li>'; }).join(''); return '<div class="qb-rationale"><b>' + g.prompt + '</b><ul>' + li + '</ul></div>'; }
      return part(q.condition, function (k) { return k === q.condition.correct; }) +
             part(q.actions, function (k) { return q.actions.correct.indexOf(k) >= 0; }) +
             part(q.parameters, function (k) { return q.parameters.correct.indexOf(k) >= 0; });
    }
    return '';
  }

  /* ---------- results ---------- */
  function finish() {
    clearInterval(timerId);
    stage.hidden = true; results.hidden = false;
    var n = answers.length, right = answers.filter(function (a) { return a.correct; }).length;
    var pctScore = Math.round(right / n * 100);
    var secs = Math.floor((Date.now() - startAt) / 1000);

    // verdict from ability vs standard (adaptive) or raw score (fixed)
    var verdict, vclass, vsub;
    if (cfg.adaptive) {
      if (ability >= PASS_STANDARD + 0.35) { verdict = 'Likely to PASS'; vclass = 'pass'; }
      else if (ability >= PASS_STANDARD - 0.2) { verdict = 'Borderline'; vclass = 'border'; }
      else { verdict = 'Not yet — keep prepping'; vclass = 'fail'; }
      vsub = 'Ability estimate ' + ability.toFixed(1) + ' / 5 · passing line ' + PASS_STANDARD.toFixed(1) + ' · exam ended at ' + n + ' items';
    } else {
      if (pctScore >= 75) { verdict = 'Strong — ' + pctScore + '%'; vclass = 'pass'; }
      else if (pctScore >= 60) { verdict = 'Almost there — ' + pctScore + '%'; vclass = 'border'; }
      else { verdict = 'Needs work — ' + pctScore + '%'; vclass = 'fail'; }
      vsub = right + ' of ' + n + ' correct · ' + Math.floor(secs / 60) + 'm ' + (secs % 60) + 's';
    }

    // per-topic breakdown
    var byCat = {};
    answers.forEach(function (a) { var c = a.q.cat; (byCat[c] = byCat[c] || { r: 0, n: 0 }); byCat[c].n++; if (a.correct) byCat[c].r++; });
    var cats = Object.keys(byCat).sort(function (x, y) { return (byCat[x].r / byCat[x].n) - (byCat[y].r / byCat[y].n); });
    var bars = cats.map(function (c) {
      var o = byCat[c], p = Math.round(o.r / o.n * 100);
      var tone = p >= 75 ? 'good' : p >= 50 ? 'mid' : 'low';
      return '<div class="ex-topic"><div class="ex-topic-head"><span>' + c + '</span><b>' + o.r + '/' + o.n + '</b></div><div class="ex-topic-bar ' + tone + '"><i style="width:' + p + '%"></i></div></div>';
    }).join('');

    var ring = '<div class="ex-ring ' + vclass + '"><span>' + pctScore + '%</span></div>';
    results.innerHTML =
      '<div class="ex-result-top">' + ring +
        '<div><span class="ex-verdict ' + vclass + '">' + verdict + '</span><p class="ex-vsub">' + vsub + '</p>' +
        (cfg.adaptive ? '<p class="ex-note">Like the real NCLEX, this exam stopped as soon as it was 95% confident where you stand — that\'s why it ran ' + n + ' items, not a fixed number.</p>' : '') +
        '</div></div>' +
      '<h3 class="ex-h">Where you stand, by topic</h3><div class="ex-topics">' + bars + '</div>' +
      '<h3 class="ex-h">Review every question</h3><div class="ex-review">' + reviewList() + '</div>' +
      '<div class="ex-result-cta"><button class="btn btn-coral" data-exam-again>Take another test</button>' +
        '<a class="btn btn-line" href="nclex-complete.html#pricing">Unlock the full 2,600+ bank</a></div>';

    results.querySelector('[data-exam-again]').addEventListener('click', reset);
    results.querySelectorAll('.ex-rev-q').forEach(function (h) { h.addEventListener('click', function () { h.parentNode.classList.toggle('open'); }); });
    saveHistory(mode, cfg.title, pctScore, n, vclass);
    window.scrollTo(0, 0);
  }

  function reviewList() {
    return answers.map(function (a, k) {
      return '<div class="ex-rev' + (a.correct ? ' ok' : ' no') + '">' +
        '<button class="ex-rev-q"><span class="ex-rev-i">' + (a.correct ? '✓' : '✕') + '</span><span>Q' + (k + 1) + ' · ' + a.q.cat + '</span><span class="ex-rev-caret">▾</span></button>' +
        '<div class="ex-rev-body"><p class="qb-stem">' + md(a.q.stem) + '</p>' + reviewBody(a.q, a.pick) + '</div></div>';
    }).join('');
  }

  function reset() { clearInterval(timerId); setup.hidden = false; runner.hidden = true; results.hidden = true; window.scrollTo(0, 0); }
  quitBtn.addEventListener('click', function () { if (confirm('End this test? Your progress won\'t be saved.')) reset(); });

  /* ---------- history (localStorage) ---------- */
  function saveHistory(m, title, score, items, vclass) {
    try {
      var h = JSON.parse(localStorage.getItem('mlsTests')) || [];
      h.unshift({ m: m, title: title, score: score, items: items, v: vclass, at: Date.now() });
      localStorage.setItem('mlsTests', JSON.stringify(h.slice(0, 12)));
    } catch (e) {}
    renderHistory();
  }
  function renderHistory() {
    var wrap = document.querySelector('[data-exam-history]');
    if (!wrap) return;
    var h = [];
    try { h = JSON.parse(localStorage.getItem('mlsTests')) || []; } catch (e) {}
    if (!h.length) { wrap.hidden = true; return; }
    wrap.hidden = false;
    wrap.innerHTML = '<h3 class="ex-h">Your recent tests</h3>' + h.map(function (r) {
      var d = new Date(r.at); var when = d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
      return '<div class="ex-hist ' + r.v + '"><span class="ex-hist-t">' + r.title + '</span><span class="ex-hist-m">' + r.items + ' items · ' + when + '</span><b class="ex-hist-s">' + r.score + '%</b></div>';
    }).join('');
  }

  /* ---------- wire the mode cards ---------- */
  root.querySelectorAll('[data-test-start]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var m = btn.getAttribute('data-test-start');
      var sel = root.querySelector('[data-test-specialty]');
      start(m, m === 'specialty' && sel ? sel.value : null);
    });
  });
  renderHistory();
})();
