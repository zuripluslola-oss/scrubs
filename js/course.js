/* Must Love Scrubs — audio-scene lesson interactions.
   The audio file is a placeholder; playback is simulated so the full
   experience (waveform, synced transcript, unlock) works before real
   recorded/AI-voiced audio is dropped in. Swap simulateScene() for a real
   <audio> element + timeupdate listener when audio lands. */

(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- Audio scene player ---- */
  var player = document.querySelector('.player');
  if (player) {
    var playBtn = player.querySelector('.play-btn');
    var lines = Array.prototype.slice.call(player.querySelectorAll('.line'));
    var cur = player.querySelector('.cur-time');
    var bars = Array.prototype.slice.call(player.querySelectorAll('.waveform i'));
    var total = lines.length;
    var idx = -1, timer = null, playing = false;

    function setLine(i) {
      lines.forEach(function (l, n) { l.classList.toggle('active', n === i); });
      if (lines[i]) lines[i].scrollIntoView({ block: 'nearest', behavior: reduce ? 'auto' : 'smooth' });
      var pct = Math.round(((i + 1) / total) * 100);
      var lit = Math.round((bars.length * (i + 1)) / total);
      bars.forEach(function (b, n) { b.classList.toggle('on', n < lit); });
      if (cur) cur.textContent = fmt(Math.round(((i + 1) / total) * 372));
    }
    function fmt(s) { var m = Math.floor(s / 60); var r = s % 60; return m + ':' + (r < 10 ? '0' : '') + r; }

    function step() {
      idx++;
      if (idx >= total) { finish(); return; }
      setLine(idx);
      timer = setTimeout(step, reduce ? 400 : 2600);
    }
    function play() {
      playing = true; player.classList.add('playing');
      if (idx >= total - 1) { idx = -1; player.classList.remove('done'); }
      step();
    }
    function pause() { playing = false; player.classList.remove('playing'); clearTimeout(timer); }
    function finish() {
      pause(); player.classList.add('done');
      setLine(total - 1);
      // unlock the quiz
      var q = document.querySelector('.quiz-band');
      if (q) q.removeAttribute('hidden');
    }
    playBtn.addEventListener('click', function () { playing ? pause() : play(); });
  }

  /* ---- Flip cards ---- */
  document.querySelectorAll('.flip').forEach(function (card) {
    card.addEventListener('click', function () { card.classList.toggle('flipped'); });
    card.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); card.classList.toggle('flipped'); }
    });
  });

  /* ---- Confidence check ---- */
  var conf = document.querySelector('.confidence');
  if (conf) {
    conf.querySelector('.conf-btn').addEventListener('click', function () { conf.classList.add('revealed'); });
  }

  /* ---- Sort-it drill (Low / Normal / High) ---- */
  document.querySelectorAll('.sort-row').forEach(function (row) {
    var answer = row.getAttribute('data-answer');
    var btns = Array.prototype.slice.call(row.querySelectorAll('.sort-btn'));
    var done = false;
    btns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (done) return; done = true;
        row.classList.add('done');
        btns.forEach(function (b) {
          b.setAttribute('disabled', '');
          if (b.getAttribute('data-zone') === answer) b.classList.add('right');
          else if (b === btn) b.classList.add('miss');
        });
      });
    });
  });

  /* ---- Quiz (single-answer MC + Select-All-That-Apply) ---- */
  var score = 0, answered = 0;
  document.querySelectorAll('.quiz-card').forEach(function (card) {
    var multi = card.classList.contains('sata');
    var opts = Array.prototype.slice.call(card.querySelectorAll('.opt'));
    var checkBtn = card.querySelector('.check-btn');
    var rationale = card.querySelector('.rationale');
    var locked = false;
    opts.forEach(function (o) {
      o.addEventListener('click', function () {
        if (locked) return;
        if (multi) { o.classList.toggle('selected'); }
        else { opts.forEach(function (x) { x.classList.remove('selected'); }); o.classList.add('selected'); }
      });
    });
    checkBtn.addEventListener('click', function () {
      if (locked) return;
      if (!opts.some(function (o) { return o.classList.contains('selected'); })) return;
      locked = true;
      var allRight = true;
      opts.forEach(function (o) {
        o.setAttribute('disabled', '');
        var isC = o.getAttribute('data-correct') === '1';
        var sel = o.classList.contains('selected');
        if (isC) o.classList.add('correct');
        if (sel && !isC) { o.classList.add('wrong'); allRight = false; }
        if (isC && !sel) allRight = false;
      });
      if (allRight) score++;
      answered++;
      if (rationale) rationale.classList.add('show');
      checkBtn.textContent = 'Answer locked';
      checkBtn.style.opacity = '0.6';
      updateResult();
    });
  });

  function updateResult() {
    var total = document.querySelectorAll('.quiz-card').length;
    var scoreEl = document.querySelector('[data-quiz-score]');
    if (scoreEl) scoreEl.textContent = score + '/' + total;
    if (answered === total && total > 0) {
      var res = document.querySelector('.result-reveal');
      if (res) res.removeAttribute('hidden');
      // award points once (demo)
      if (!sessionStorage.getItem('labScenePts')) {
        sessionStorage.setItem('labScenePts', '1');
        var earned = 15 + score * 5;
        var bal = parseInt(localStorage.getItem('mlsPoints') || '0', 10) + earned;
        localStorage.setItem('mlsPoints', String(bal));
        var won = document.querySelector('[data-pts-won]');
        if (won) won.textContent = '+' + earned + ' points earned';
      }
      var res2 = document.querySelector('.result-reveal');
      if (res2) res2.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
    }
  }
})();
