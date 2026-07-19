/* Must Love Scrubs — Flashcards & Games (adaptive, multi-format).
   Card kinds: qa (flip), mc, tf, fill, odd, order, bowtie.
   Modes: Study (flip qa + interactive others), Challenge (mixed interactive),
   Quiz (MC from qa cards), Match game, Speed round. Difficulty 1-5 = CAT scale;
   level rises with mastery. Demo persistence via localStorage. */

(function () {
  'use strict';
  var root = document.querySelector('.flash');
  if (!root) return;
  var ALL = JSON.parse(root.querySelector('script[data-flash]').textContent);
  function md(s) { return String(s == null ? '' : s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>'); }
  function esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  var INTERACTIVE = ['mc','tf','fill','odd','order','bowtie'];

  var stage = root.querySelector('[data-fc-stage]');
  var levelEl = root.querySelector('[data-fc-level]'), mastEl = root.querySelector('[data-fc-mastered]');
  var streakEl = root.querySelector('[data-fc-streak]'), countEl = root.querySelector('[data-fc-count]');

  var S; try { S = JSON.parse(localStorage.getItem('mlsFlash')) || {}; } catch (e) { S = {}; }
  S.level = S.level || 1; S.mastered = S.mastered || {}; S.streak = S.streak || 0;
  function save() { try { localStorage.setItem('mlsFlash', JSON.stringify(S)); } catch (e) {} }

  var deck = 'All', mode = 'study';
  function pool() { return deck === 'All' ? ALL : ALL.filter(function (c) { return c.deck === deck; }); }
  function qaPool() { return pool().filter(function (c) { return (c.kind || 'qa') === 'qa' && c.back; }); }
  function interPool() { return pool().filter(function (c) { return INTERACTIVE.indexOf(c.kind) >= 0; }); }
  function meta() { levelEl.textContent = S.level; mastEl.textContent = Object.keys(S.mastered).length; streakEl.textContent = S.streak; countEl.textContent = pool().length; }
  function applyResult(correct, c) {
    if (correct) { S.mastered[c.id] = true; S.streak++; if (S.streak % 4 === 0 && S.level < 5) S.level++; }
    else { S.streak = 0; }
    save(); meta();
  }
  function feedbackHTML(correct, c, answerLine) {
    return '<div class="fc-fb ' + (correct ? 'ok' : 'no') + '">' +
      '<span class="fc-verdict">' + (correct ? '✓ Correct' : '✗ Not quite') + '</span>' +
      (answerLine ? '<p class="fc-ans-line">' + answerLine + '</p>' : '') +
      (c.rationale ? '<p class="fc-why"><b>Why:</b> ' + md(c.rationale) + '</p>' : '') +
      (c.hint ? '<p class="fc-hint">💡 ' + md(c.hint) + '</p>' : '') +
      '<button class="btn btn-coral fc-next">Next →</button></div>';
  }

  /* ============ interactive kinds ============ */
  function renderInteractive(c, onNext) {
    var head = '<span class="fc-tag">' + esc(c.deck) + ' · L' + c.difficulty + ' · ' + (c.kind || '').toUpperCase() + '</span>' +
               '<p class="fc-q">' + md(c.front) + '</p>';
    if (c.kind === 'mc' || c.kind === 'odd') return interChoice(c, head, onNext);
    if (c.kind === 'tf') return interTF(c, head, onNext);
    if (c.kind === 'fill') return interFill(c, head, onNext);
    if (c.kind === 'order') return interOrder(c, head, onNext);
    if (c.kind === 'bowtie') return interBowtie(c, head, onNext);
  }
  function wireNext(onNext) { var n = stage.querySelector('.fc-next'); if (n) n.addEventListener('click', onNext); }

  function interChoice(c, head, onNext) {
    stage.innerHTML = '<div class="fc-inter">' + head + '<div class="fc-opts">' +
      c.options.map(function (o, i) { return '<button class="fc-opt" data-i="' + i + '">' + md(o) + '</button>'; }).join('') +
      '</div><div class="fc-slot"></div></div>';
    stage.querySelectorAll('.fc-opt').forEach(function (b) {
      b.addEventListener('click', function () {
        var i = +b.getAttribute('data-i'); var ok = i === c.correct;
        stage.querySelectorAll('.fc-opt').forEach(function (x, xi) { x.disabled = true; if (xi === c.correct) x.classList.add('right'); else if (xi === i) x.classList.add('wrong'); });
        applyResult(ok, c);
        stage.querySelector('.fc-slot').innerHTML = feedbackHTML(ok, c, ok ? '' : 'Answer: <b>' + md(c.options[c.correct]) + '</b>');
        wireNext(onNext);
      });
    });
  }
  function interTF(c, head, onNext) {
    stage.innerHTML = '<div class="fc-inter">' + head + '<div class="fc-opts fc-tf">' +
      '<button class="fc-opt" data-v="true">True</button><button class="fc-opt" data-v="false">False</button>' +
      '</div><div class="fc-slot"></div></div>';
    stage.querySelectorAll('.fc-opt').forEach(function (b) {
      b.addEventListener('click', function () {
        var v = b.getAttribute('data-v') === 'true'; var ok = v === c.correct;
        stage.querySelectorAll('.fc-opt').forEach(function (x) { x.disabled = true; if ((x.getAttribute('data-v') === 'true') === c.correct) x.classList.add('right'); else if (x === b) x.classList.add('wrong'); });
        applyResult(ok, c);
        stage.querySelector('.fc-slot').innerHTML = feedbackHTML(ok, c, 'Answer: <b>' + (c.correct ? 'True' : 'False') + '</b>');
        wireNext(onNext);
      });
    });
  }
  function interFill(c, head, onNext) {
    stage.innerHTML = '<div class="fc-inter">' + head + '<div class="fc-fill"><input type="text" class="fc-input" placeholder="Type your answer…" autocomplete="off"><button class="btn btn-coral fc-check">Check</button></div><div class="fc-slot"></div></div>';
    var input = stage.querySelector('.fc-input');
    function norm(s) { return String(s).toLowerCase().replace(/[^a-z0-9. ]/g, '').replace(/\s+/g, ' ').trim(); }
    function check() {
      var accept = [c.answer].concat(c.accept || []).map(norm);
      var ok = accept.indexOf(norm(input.value)) >= 0;
      input.disabled = true; stage.querySelector('.fc-check').disabled = true;
      input.classList.add(ok ? 'right' : 'wrong');
      applyResult(ok, c);
      stage.querySelector('.fc-slot').innerHTML = feedbackHTML(ok, c, 'Answer: <b>' + md(c.answer) + '</b>');
      wireNext(onNext);
    }
    stage.querySelector('.fc-check').addEventListener('click', check);
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter') check(); });
    input.focus();
  }
  function interOrder(c, head, onNext) {
    var shuffled = shuffle(c.items.map(function (t, i) { return { t: t, i: i }; }));
    var chosen = [];
    stage.innerHTML = '<div class="fc-inter">' + head + '<p class="fc-sub">Tap the steps in the correct order:</p>' +
      '<div class="fc-order">' + shuffled.map(function (x) { return '<button class="fc-ord" data-t="' + esc(x.t) + '">' + md(x.t) + '</button>'; }).join('') + '</div>' +
      '<div class="fc-actions"><button class="btn btn-line fc-reset">Reset</button><button class="btn btn-coral fc-check" disabled>Check order</button></div><div class="fc-slot"></div></div>';
    function refresh() {
      stage.querySelectorAll('.fc-ord').forEach(function (b) { var idx = chosen.indexOf(b.getAttribute('data-t')); b.classList.toggle('picked', idx >= 0); b.querySelector('.fc-num') && b.querySelector('.fc-num').remove(); if (idx >= 0) { var s = document.createElement('span'); s.className = 'fc-num'; s.textContent = (idx + 1); b.prepend(s); } });
      stage.querySelector('.fc-check').disabled = chosen.length !== c.items.length;
    }
    stage.querySelectorAll('.fc-ord').forEach(function (b) {
      b.addEventListener('click', function () { var t = b.getAttribute('data-t'); var i = chosen.indexOf(t); if (i >= 0) chosen.splice(i, 1); else chosen.push(t); refresh(); });
    });
    stage.querySelector('.fc-reset').addEventListener('click', function () { chosen = []; refresh(); });
    stage.querySelector('.fc-check').addEventListener('click', function () {
      var ok = chosen.join('||') === c.items.join('||');
      stage.querySelectorAll('.fc-ord').forEach(function (b) { b.disabled = true; var pos = chosen.indexOf(b.getAttribute('data-t')); var correctPos = c.items.indexOf(b.getAttribute('data-t')); b.classList.add(pos === correctPos ? 'right' : 'wrong'); });
      applyResult(ok, c);
      var correctList = '<ol class="fc-correct-order">' + c.items.map(function (t) { return '<li>' + md(t) + '</li>'; }).join('') + '</ol>';
      stage.querySelector('.fc-slot').innerHTML = feedbackHTML(ok, c, ok ? '' : 'Correct order:' + correctList);
      wireNext(onNext);
    });
  }
  function interBowtie(c, head, onNext) {
    function grp(key, label) {
      var g = c[key];
      return '<div class="fc-bt-col"><span class="fc-bt-label">' + label + (g.pick ? ' (' + g.pick + ')' : '') + '</span>' +
        g.options.map(function (o, i) { return '<button class="fc-bt-opt" data-g="' + key + '" data-i="' + i + '">' + md(o) + '</button>'; }).join('') + '</div>';
    }
    stage.innerHTML = '<div class="fc-inter">' + head +
      '<div class="fc-bt">' + grp('actions', 'Actions') + grp('condition', 'Condition') + grp('parameters', 'Monitor') + '</div>' +
      '<div class="fc-actions"><button class="btn btn-coral fc-check" disabled>Check</button></div><div class="fc-slot"></div></div>';
    var pick = { condition: null, actions: {}, parameters: {} };
    function complete() { return pick.condition != null && Object.keys(pick.actions).length === (c.actions.pick || 2) && Object.keys(pick.parameters).length === (c.parameters.pick || 2); }
    stage.querySelectorAll('.fc-bt-opt').forEach(function (b) {
      b.addEventListener('click', function () {
        var g = b.getAttribute('data-g'), i = +b.getAttribute('data-i');
        if (g === 'condition') { stage.querySelectorAll('[data-g="condition"]').forEach(function (x) { x.classList.remove('sel'); }); b.classList.add('sel'); pick.condition = i; }
        else { var cap = c[g].pick || 2; if (pick[g][i]) { delete pick[g][i]; b.classList.remove('sel'); } else if (Object.keys(pick[g]).length < cap) { pick[g][i] = true; b.classList.add('sel'); } }
        stage.querySelector('.fc-check').disabled = !complete();
      });
    });
    stage.querySelector('.fc-check').addEventListener('click', function () {
      function set(arr) { var o = {}; arr.forEach(function (i) { o[i] = true; }); return o; }
      var cc = pick.condition === c.condition.correct;
      var ac = Object.keys(pick.actions).length === c.actions.correct.length && c.actions.correct.every(function (i) { return pick.actions[i]; });
      var pc = Object.keys(pick.parameters).length === c.parameters.correct.length && c.parameters.correct.every(function (i) { return pick.parameters[i]; });
      var ok = cc && ac && pc;
      [['condition', c.condition.correct], ['actions', c.actions.correct], ['parameters', c.parameters.correct]].forEach(function (pair) {
        var key = pair[0], cset = (key === 'condition') ? set([pair[1]]) : set(pair[1]);
        stage.querySelectorAll('[data-g="' + key + '"]').forEach(function (b) {
          var i = +b.getAttribute('data-i'); b.disabled = true;
          var sel = key === 'condition' ? (pick.condition === i) : !!pick[key][i];
          if (cset[i] && sel) b.classList.add('right'); else if (cset[i]) b.classList.add('missed'); else if (sel) b.classList.add('wrong');
        });
      });
      applyResult(ok, c);
      stage.querySelector('.fc-slot').innerHTML = feedbackHTML(ok, c, '');
      wireNext(onNext);
    });
  }

  /* ============ STUDY (flip qa + interactive others) ============ */
  var sQ = [], sI = 0;
  function buildStudy() {
    var cap = Math.min(5, S.level + 1);
    var p = pool().filter(function (c) { return c.difficulty <= cap; });
    p.sort(function (a, b) { var am = S.mastered[a.id] ? 1 : 0, bm = S.mastered[b.id] ? 1 : 0; return am - bm || a.difficulty - b.difficulty; });
    sQ = p; sI = 0;
  }
  function studyNext() { sI++; renderStudy(); }
  function renderStudy() {
    if (!sQ.length) buildStudy();
    if (sI >= sQ.length) { doneScreen('Deck complete 🎉', 'You worked ' + sQ.length + ' cards at level ' + S.level + '.', function () { buildStudy(); renderStudy(); }); return; }
    var c = sQ[sI];
    if ((c.kind || 'qa') !== 'qa') { renderInteractive(c, studyNext); prog(); return; }
    stage.innerHTML = progBar() +
      '<div class="fc-card" data-flip><div class="fc-inner">' +
      '<div class="fc-face fc-front"><span class="fc-tag">' + esc(c.deck) + ' · L' + c.difficulty + '</span><p class="fc-q">' + md(c.front) + '</p><span class="fc-flip-hint">Tap to flip</span></div>' +
      '<div class="fc-face fc-back"><p class="fc-a">' + md(c.back) + '</p>' + (c.rationale ? '<p class="fc-why"><b>Why:</b> ' + md(c.rationale) + '</p>' : '') + (c.hint ? '<p class="fc-hint">💡 ' + md(c.hint) + '</p>' : '') + '</div>' +
      '</div></div>' +
      '<div class="fc-rate" hidden><button class="fc-r again" data-r="again">Again</button><button class="fc-r hard" data-r="hard">Hard</button><button class="fc-r good" data-r="good">Good</button><button class="fc-r easy" data-r="easy">Easy</button></div>';
    var card = stage.querySelector('.fc-card'), rate = stage.querySelector('.fc-rate');
    card.addEventListener('click', function () { card.classList.add('flipped'); rate.hidden = false; });
    rate.querySelectorAll('.fc-r').forEach(function (b) { b.addEventListener('click', function () { var r = b.getAttribute('data-r'); applyResult(r === 'good' || r === 'easy', c); if (r === 'again') delete S.mastered[c.id]; save(); studyNext(); }); });
  }
  function prog() {}
  function progBar() { return '<div class="fc-progress"><i style="width:' + Math.round(sI / Math.max(1, sQ.length) * 100) + '%"></i></div>'; }

  /* ============ CHALLENGE (mixed interactive) ============ */
  var cQ = [], cI = 0;
  function renderChallenge() {
    if (!cQ.length || cI >= cQ.length) {
      var p = interPool().filter(function (c) { return c.difficulty <= Math.min(5, S.level + 1); });
      if (!p.length) { stage.innerHTML = '<div class="fc-done"><h3>No challenge cards here yet</h3><p>Pick “All” or another deck — Challenge uses multiple-choice, true/false, fill-in, odd-one-out, ordering, and bow-tie cards.</p></div>'; return; }
      cQ = shuffle(p); cI = 0;
    }
    renderInteractive(cQ[cI], function () { cI++; renderChallenge(); });
  }

  /* ============ QUIZ (MC from qa cards) ============ */
  var qQ = [], qI = 0;
  function renderQuiz() {
    var p = qaPool();
    if (p.length < 2) { stage.innerHTML = '<div class="fc-done"><h3>Quiz needs flip cards</h3><p>Choose “All” or a deck with term/definition cards.</p></div>'; return; }
    if (!qQ.length || qI >= qQ.length) { qQ = shuffle(p); qI = 0; }
    var c = qQ[qI];
    var distract = shuffle(p.filter(function (x) { return x.id !== c.id; })).slice(0, 3).map(function (x) { return x.back; });
    var opts = shuffle([c.back].concat(distract));
    stage.innerHTML = '<div class="fc-inter"><span class="fc-tag">' + esc(c.deck) + '</span><p class="fc-q">' + md(c.front) + '</p><div class="fc-opts">' +
      opts.map(function (o) { return '<button class="fc-opt">' + md(o) + '</button>'; }).join('') + '</div><div class="fc-slot"></div></div>';
    stage.querySelectorAll('.fc-opt').forEach(function (b) {
      b.addEventListener('click', function () {
        var ok = b.textContent === String(c.back).replace(/\*\*/g, '');
        stage.querySelectorAll('.fc-opt').forEach(function (x) { x.disabled = true; if (x.textContent === String(c.back).replace(/\*\*/g, '')) x.classList.add('right'); else if (x === b) x.classList.add('wrong'); });
        applyResult(ok, c);
        stage.querySelector('.fc-slot').innerHTML = feedbackHTML(ok, c, ok ? '' : 'Answer: <b>' + md(c.back) + '</b>');
        wireNext(function () { qI++; renderQuiz(); });
      });
    });
  }

  /* ============ MATCH ============ */
  function renderMatch() {
    var p = shuffle(qaPool()).slice(0, 6);
    if (p.length < 3) { stage.innerHTML = '<div class="fc-done"><h3>Match needs flip cards</h3><p>Choose “All” or a term/definition deck.</p></div>'; return; }
    var lefts = p.map(function (c) { return { id: c.id, t: c.front }; });
    var rights = shuffle(p.map(function (c) { return { id: c.id, t: c.back }; }));
    var start = Date.now(), matched = 0, pickL = null;
    stage.innerHTML = '<div class="fc-match"><div class="fc-mcol" data-side="l">' + lefts.map(function (x) { return '<button class="fc-tile" data-id="' + x.id + '">' + md(x.t) + '</button>'; }).join('') +
      '</div><div class="fc-mcol" data-side="r">' + rights.map(function (x) { return '<button class="fc-tile" data-id="' + x.id + '">' + md(x.t) + '</button>'; }).join('') + '</div></div><p class="fc-match-msg">Tap a term, then its match.</p>';
    var msg = stage.querySelector('.fc-match-msg');
    stage.querySelectorAll('[data-side="l"] .fc-tile').forEach(function (b) { b.addEventListener('click', function () { if (b.classList.contains('done')) return; stage.querySelectorAll('[data-side="l"] .fc-tile').forEach(function (x) { x.classList.remove('sel'); }); b.classList.add('sel'); pickL = b; }); });
    stage.querySelectorAll('[data-side="r"] .fc-tile').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickL || b.classList.contains('done')) return;
        if (b.getAttribute('data-id') === pickL.getAttribute('data-id')) { b.classList.add('done'); pickL.classList.add('done'); pickL.classList.remove('sel'); pickL = null; matched++; if (matched === p.length) { var secs = Math.round((Date.now() - start) / 1000); S.streak++; save(); meta(); msg.innerHTML = '<b>Matched all ' + p.length + ' in ' + secs + 's! 🎉</b> <button class="btn btn-coral fc-again">Play again</button>'; msg.querySelector('.fc-again').addEventListener('click', renderMatch); } }
        else { var bad = b; b.classList.add('miss'); setTimeout(function () { bad.classList.remove('miss'); }, 400); }
      });
    });
  }

  /* ============ SPEED (qa flip, 60s) ============ */
  function renderSpeed() {
    var p = qaPool();
    if (!p.length) { stage.innerHTML = '<div class="fc-done"><h3>Speed round needs flip cards</h3><p>Choose “All” or a term/definition deck.</p></div>'; return; }
    var q = shuffle(p), i = 0, hits = 0, secs = 60, timer;
    function draw() {
      if (i >= q.length) { q = shuffle(p); i = 0; } var c = q[i];
      stage.innerHTML = '<div class="fc-speed"><div class="fc-timer"><i style="width:' + (secs / 60 * 100) + '%"></i></div><div class="fc-sp-time">' + secs + 's · <b>' + hits + '</b> correct</div>' +
        '<div class="fc-sp-card"><p class="fc-q">' + md(c.front) + '</p><div class="fc-sp-ans" hidden><p class="fc-a">' + md(c.back) + '</p></div></div>' +
        '<div class="fc-actions"><button class="btn btn-line" data-sp="reveal">Reveal</button><button class="btn btn-coral" data-sp="got" hidden>Got it</button><button class="btn btn-line" data-sp="miss" hidden>Missed</button></div></div>';
      stage.querySelector('[data-sp="reveal"]').addEventListener('click', function () { stage.querySelector('.fc-sp-ans').hidden = false; this.hidden = true; stage.querySelector('[data-sp="got"]').hidden = false; stage.querySelector('[data-sp="miss"]').hidden = false; });
      stage.querySelector('[data-sp="got"]').addEventListener('click', function () { hits++; i++; draw(); });
      stage.querySelector('[data-sp="miss"]').addEventListener('click', function () { i++; draw(); });
    }
    draw();
    timer = setInterval(function () { secs--; var t = stage.querySelector('.fc-sp-time'), bar = stage.querySelector('.fc-timer i'); if (t) t.innerHTML = secs + 's · <b>' + hits + '</b> correct'; if (bar) bar.style.width = (secs / 60 * 100) + '%'; if (secs <= 0) { clearInterval(timer); doneScreen('Time! ⏱️', 'You recalled ' + hits + ' cards in 60 seconds.', renderSpeed); } }, 1000);
    root._t = timer;
  }

  function doneScreen(h, p, again) { stage.innerHTML = '<div class="fc-done"><h3>' + h + '</h3><p>' + p + '</p><button class="btn btn-coral fc-again">Go again</button></div>'; stage.querySelector('.fc-again').addEventListener('click', again); }

  function render() {
    if (root._t) { clearInterval(root._t); root._t = null; }
    if (mode === 'study') { buildStudy(); renderStudy(); }
    else if (mode === 'challenge') { cQ = []; renderChallenge(); }
    else if (mode === 'quiz') { qQ = []; renderQuiz(); }
    else if (mode === 'match') renderMatch();
    else if (mode === 'speed') renderSpeed();
    meta();
  }
  root.querySelectorAll('.fc-chip').forEach(function (chip) { chip.addEventListener('click', function () { root.querySelectorAll('.fc-chip').forEach(function (c) { c.classList.remove('on'); }); chip.classList.add('on'); deck = chip.getAttribute('data-deck'); render(); }); });
  root.querySelectorAll('.fc-mode').forEach(function (m) { m.addEventListener('click', function () { root.querySelectorAll('.fc-mode').forEach(function (x) { x.classList.remove('on'); }); m.classList.add('on'); mode = m.getAttribute('data-mode'); render(); }); });
  render();
})();
