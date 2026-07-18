/* Must Love Scrubs — Flashcards & Games (adaptive).
   Study (animated flip + confidence + spaced levels), Quiz (MC from cards),
   Match game, Speed round. Difficulty 1-5 mirrors the CAT engine; level rises
   with mastery. Demo persistence via localStorage. */

(function () {
  'use strict';
  var root = document.querySelector('.flash');
  if (!root) return;
  var ALL = JSON.parse(root.querySelector('script[data-flash]').textContent);
  function md(s) { return String(s == null ? '' : s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>'); }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }

  var stage = root.querySelector('[data-fc-stage]');
  var levelEl = root.querySelector('[data-fc-level]');
  var mastEl = root.querySelector('[data-fc-mastered]');
  var streakEl = root.querySelector('[data-fc-streak]');
  var countEl = root.querySelector('[data-fc-count]');

  var S;
  try { S = JSON.parse(localStorage.getItem('mlsFlash')) || {}; } catch (e) { S = {}; }
  S.level = S.level || 1; S.mastered = S.mastered || {}; S.streak = S.streak || 0;
  function save() { try { localStorage.setItem('mlsFlash', JSON.stringify(S)); } catch (e) {} }

  var deck = 'All', mode = 'study';
  function pool() { return deck === 'All' ? ALL : ALL.filter(function (c) { return c.deck === deck; }); }
  function meta() {
    levelEl.textContent = S.level;
    mastEl.textContent = Object.keys(S.mastered).length;
    streakEl.textContent = S.streak;
    countEl.textContent = pool().length;
  }

  /* ---------- STUDY (adaptive flip) ---------- */
  var sQ = [], sI = 0;
  function buildStudy() {
    var cap = Math.min(5, S.level + 1);           // adaptive: don't show far-above-level cards
    var p = pool().filter(function (c) { return c.difficulty <= cap; });
    // unmastered first (easier first), then mastered for review
    p.sort(function (a, b) {
      var am = S.mastered[a.id] ? 1 : 0, bm = S.mastered[b.id] ? 1 : 0;
      return am - bm || a.difficulty - b.difficulty;
    });
    sQ = p; sI = 0;
  }
  function renderStudy() {
    if (!sQ.length) buildStudy();
    if (sI >= sQ.length) {
      stage.innerHTML = '<div class="fc-done"><h3>Deck complete 🎉</h3><p>You worked ' + sQ.length + ' cards at level ' + S.level + '. Level up by rating cards “Good/Easy”.</p><button class="btn btn-coral" data-fc-restart>Go again</button></div>';
      stage.querySelector('[data-fc-restart]').addEventListener('click', function () { buildStudy(); renderStudy(); });
      return;
    }
    var c = sQ[sI];
    stage.innerHTML =
      '<div class="fc-progress"><i style="width:' + Math.round(sI / sQ.length * 100) + '%"></i></div>' +
      '<div class="fc-card" data-flip>' +
        '<div class="fc-inner">' +
          '<div class="fc-face fc-front"><span class="fc-tag">' + c.deck + ' · L' + c.difficulty + '</span>' +
            '<p class="fc-q">' + md(c.front) + '</p><span class="fc-flip-hint">Tap to flip</span></div>' +
          '<div class="fc-face fc-back"><p class="fc-a">' + md(c.back) + '</p>' +
            (c.rationale ? '<p class="fc-why"><b>Why:</b> ' + md(c.rationale) + '</p>' : '') +
            (c.hint ? '<p class="fc-hint">💡 ' + md(c.hint) + '</p>' : '') + '</div>' +
        '</div>' +
      '</div>' +
      '<div class="fc-rate" hidden>' +
        '<button class="fc-r again" data-r="again">Again</button>' +
        '<button class="fc-r hard" data-r="hard">Hard</button>' +
        '<button class="fc-r good" data-r="good">Good</button>' +
        '<button class="fc-r easy" data-r="easy">Easy</button>' +
      '</div>';
    var card = stage.querySelector('.fc-card'), rate = stage.querySelector('.fc-rate');
    card.addEventListener('click', function () { card.classList.add('flipped'); rate.hidden = false; });
    rate.querySelectorAll('.fc-r').forEach(function (b) {
      b.addEventListener('click', function () {
        var r = b.getAttribute('data-r');
        if (r === 'good' || r === 'easy') {
          S.mastered[c.id] = true; S.streak++;
          if (S.streak > 0 && S.streak % 4 === 0 && S.level < 5) S.level++;
        } else { S.streak = 0; if (r === 'again') delete S.mastered[c.id]; }
        save(); meta(); sI++; renderStudy();
      });
    });
    meta();
  }

  /* ---------- QUIZ (MC generated from cards) ---------- */
  var qQ = [], qI = 0;
  function renderQuiz() {
    if (!qQ.length || qI >= qQ.length) { qQ = shuffle(pool()); qI = 0; }
    var p = pool(); var c = qQ[qI];
    var distract = shuffle(p.filter(function (x) { return x.id !== c.id; })).slice(0, 3).map(function (x) { return x.back; });
    var opts = shuffle([c.back].concat(distract));
    stage.innerHTML =
      '<div class="fc-quiz"><span class="fc-tag">' + c.deck + '</span>' +
      '<p class="fc-q">' + md(c.front) + '</p><div class="fc-opts">' +
      opts.map(function (o) { return '<button class="fc-opt">' + md(o) + '</button>'; }).join('') +
      '</div><div class="fc-reveal" hidden></div></div>';
    var reveal = stage.querySelector('.fc-reveal');
    stage.querySelectorAll('.fc-opt').forEach(function (b) {
      b.addEventListener('click', function () {
        if (reveal.dataset.done) return; reveal.dataset.done = '1';
        var ok = b.textContent === c.back.replace(/\*\*/g, '');
        stage.querySelectorAll('.fc-opt').forEach(function (x) {
          x.disabled = true;
          if (x.textContent === c.back.replace(/\*\*/g, '')) x.classList.add('right');
          else if (x === b) x.classList.add('wrong');
        });
        if (ok) { S.streak++; S.mastered[c.id] = true; } else { S.streak = 0; }
        save(); meta();
        reveal.hidden = false;
        reveal.innerHTML = '<div class="fc-why"><b>' + (ok ? 'Correct — ' : 'Answer: ' + md(c.back) + '. ') + '</b>' + md(c.rationale || '') + '</div>' +
          '<button class="btn btn-coral" data-fc-next>Next card →</button>';
        reveal.querySelector('[data-fc-next]').addEventListener('click', function () { qI++; renderQuiz(); });
      });
    });
    meta();
  }

  /* ---------- MATCH GAME ---------- */
  function renderMatch() {
    var p = shuffle(pool()).slice(0, Math.min(6, pool().length));
    var lefts = p.map(function (c) { return { id: c.id, t: c.front }; });
    var rights = shuffle(p.map(function (c) { return { id: c.id, t: c.back }; }));
    var start = Date.now(), matched = 0, pickL = null;
    stage.innerHTML = '<div class="fc-match"><div class="fc-mcol" data-side="l">' +
      lefts.map(function (x) { return '<button class="fc-tile" data-id="' + x.id + '">' + md(x.t) + '</button>'; }).join('') +
      '</div><div class="fc-mcol" data-side="r">' +
      rights.map(function (x) { return '<button class="fc-tile" data-id="' + x.id + '">' + md(x.t) + '</button>'; }).join('') +
      '</div></div><p class="fc-match-msg">Tap a term on the left, then its match on the right.</p>';
    var msg = stage.querySelector('.fc-match-msg');
    function done() {
      var secs = Math.round((Date.now() - start) / 1000);
      S.streak++; save(); meta();
      msg.innerHTML = '<b>Matched all ' + p.length + ' in ' + secs + 's! 🎉</b> <button class="btn btn-coral" data-fc-again>Play again</button>';
      msg.querySelector('[data-fc-again]').addEventListener('click', renderMatch);
    }
    stage.querySelectorAll('.fc-mcol[data-side="l"] .fc-tile').forEach(function (b) {
      b.addEventListener('click', function () {
        if (b.classList.contains('done')) return;
        stage.querySelectorAll('[data-side="l"] .fc-tile').forEach(function (x) { x.classList.remove('sel'); });
        b.classList.add('sel'); pickL = b;
      });
    });
    stage.querySelectorAll('.fc-mcol[data-side="r"] .fc-tile').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickL || b.classList.contains('done')) return;
        if (b.getAttribute('data-id') === pickL.getAttribute('data-id')) {
          b.classList.add('done'); pickL.classList.add('done'); pickL.classList.remove('sel'); pickL = null;
          matched++; if (matched === p.length) done();
        } else {
          b.classList.add('miss'); var bad = b; setTimeout(function () { bad.classList.remove('miss'); }, 400);
        }
      });
    });
    meta();
  }

  /* ---------- SPEED ROUND (brain teaser, 60s) ---------- */
  function renderSpeed() {
    var q = shuffle(pool()), i = 0, hits = 0, secs = 60, timer;
    function draw() {
      if (i >= q.length) q = shuffle(pool()), i = 0;
      var c = q[i];
      stage.innerHTML = '<div class="fc-speed"><div class="fc-timer"><i></i></div>' +
        '<div class="fc-sp-time">' + secs + 's · <b>' + hits + '</b> correct</div>' +
        '<div class="fc-sp-card"><p class="fc-q">' + md(c.front) + '</p>' +
        '<div class="fc-sp-ans" hidden><p class="fc-a">' + md(c.back) + '</p></div></div>' +
        '<div class="fc-sp-actions"><button class="btn btn-line" data-sp="reveal">Reveal</button>' +
        '<button class="btn btn-coral" data-sp="got" hidden>Got it</button>' +
        '<button class="btn btn-line" data-sp="miss" hidden>Missed</button></div></div>';
      var ans = stage.querySelector('.fc-sp-ans');
      stage.querySelector('[data-sp="reveal"]').addEventListener('click', function () {
        ans.hidden = false; this.hidden = true;
        stage.querySelector('[data-sp="got"]').hidden = false;
        stage.querySelector('[data-sp="miss"]').hidden = false;
      });
      stage.querySelector('[data-sp="got"]').addEventListener('click', function () { hits++; i++; draw(); });
      stage.querySelector('[data-sp="miss"]').addEventListener('click', function () { i++; draw(); });
      var bar = stage.querySelector('.fc-timer i'); if (bar) bar.style.width = (secs / 60 * 100) + '%';
    }
    function end() {
      clearInterval(timer);
      S.streak = 0; save(); meta();
      stage.innerHTML = '<div class="fc-done"><h3>Time! ⏱️</h3><p>You recalled <b>' + hits + '</b> cards in 60 seconds.</p><button class="btn btn-coral" data-fc-again>Run it back</button></div>';
      stage.querySelector('[data-fc-again]').addEventListener('click', renderSpeed);
    }
    draw();
    timer = setInterval(function () { secs--; var t = stage.querySelector('.fc-sp-time'); var bar = stage.querySelector('.fc-timer i'); if (t) t.innerHTML = secs + 's · <b>' + hits + '</b> correct'; if (bar) bar.style.width = (secs / 60 * 100) + '%'; if (secs <= 0) end(); }, 1000);
    // stop timer if user leaves the mode
    root._speedTimer = timer;
  }

  function render() {
    if (root._speedTimer) { clearInterval(root._speedTimer); root._speedTimer = null; }
    if (mode === 'study') { buildStudy(); renderStudy(); }
    else if (mode === 'quiz') { qQ = []; renderQuiz(); }
    else if (mode === 'match') renderMatch();
    else if (mode === 'speed') renderSpeed();
    meta();
  }

  root.querySelectorAll('.fc-chip').forEach(function (chip) {
    chip.addEventListener('click', function () {
      root.querySelectorAll('.fc-chip').forEach(function (c) { c.classList.remove('on'); });
      chip.classList.add('on'); deck = chip.getAttribute('data-deck'); render();
    });
  });
  root.querySelectorAll('.fc-mode').forEach(function (m) {
    m.addEventListener('click', function () {
      root.querySelectorAll('.fc-mode').forEach(function (x) { x.classList.remove('on'); });
      m.classList.add('on'); mode = m.getAttribute('data-mode'); render();
    });
  });

  render();
})();
