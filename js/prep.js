/* Must Love Scrubs — NCLEX Prep interactions.
   Timed memory round, chart-trend, matrix/grid, SBAR builder,
   RN/LPN track toggle, and a demo free->paid gate (localStorage). */

(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- RN / LPN track toggle ---------- */
  var seg = document.querySelector('.segment');
  if (seg) {
    seg.addEventListener('click', function (e) {
      var btn = e.target.closest('button'); if (!btn) return;
      seg.querySelectorAll('button').forEach(function (b) { b.classList.remove('on'); });
      btn.classList.add('on');
      var track = btn.getAttribute('data-track'); // 'rn' | 'lpn'
      document.body.setAttribute('data-track', track);
      document.querySelectorAll('[data-rn]').forEach(function (el) {
        el.textContent = el.getAttribute(track === 'lpn' ? 'data-lpn' : 'data-rn');
      });
      document.querySelectorAll('.track-word').forEach(function (el) {
        el.textContent = track === 'lpn' ? 'LPN' : 'RN';
      });
    });
  }

  /* ---------- Timed memory round ---------- */
  var tmr = document.querySelector('.timed-round');
  if (tmr) {
    var PROMPTS = JSON.parse(tmr.getAttribute('data-prompts'));
    var promptEl = tmr.querySelector('.prompt');
    var gridEl = tmr.querySelector('.choice-grid');
    var barEl = tmr.querySelector('.timer-bar i');
    var idxEl = tmr.querySelector('.tmr-idx');
    var streakEl = tmr.querySelector('.tmr-streak');
    var startBtn = tmr.querySelector('.tmr-start');
    var body = tmr.querySelector('.tmr-body');
    var i = -1, streak = 0, best = 0, timeout = null, PER = reduce ? 12000 : 8000;

    function render() {
      i++;
      if (i >= PROMPTS.length) { finish(); return; }
      var q = PROMPTS[i];
      idxEl.textContent = (i + 1) + ' / ' + PROMPTS.length;
      promptEl.textContent = q.q;
      gridEl.innerHTML = '';
      q.a.forEach(function (opt) {
        var b = document.createElement('button');
        b.className = 'choice'; b.textContent = opt.t;
        b.addEventListener('click', function () { answer(b, opt.c, q); });
        gridEl.appendChild(b);
      });
      // reset timer bar
      barEl.classList.remove('run'); barEl.style.transition = 'none'; barEl.style.width = '100%';
      void barEl.offsetWidth;
      barEl.style.transition = 'width ' + PER + 'ms linear';
      barEl.style.width = '0%';
      clearTimeout(timeout);
      timeout = setTimeout(function () { timeUp(q); }, PER);
    }
    function lockRow(correctFn) {
      Array.prototype.slice.call(gridEl.children).forEach(function (b) {
        b.setAttribute('disabled', ''); if (correctFn(b)) b.classList.add('right');
      });
    }
    function answer(btn, correct, q) {
      clearTimeout(timeout); barEl.style.transition = 'none';
      lockRow(function (b) { return b.textContent === correctText(q); });
      if (correct) { streak++; best = Math.max(best, streak); } else { btn.classList.add('wrong'); streak = 0; }
      streakEl.textContent = streak;
      setTimeout(render, 900);
    }
    function timeUp(q) {
      streak = 0; streakEl.textContent = 0;
      lockRow(function (b) { return b.textContent === correctText(q); });
      setTimeout(render, 900);
    }
    function correctText(q) { for (var k = 0; k < q.a.length; k++) if (q.a[k].c) return q.a[k].t; }
    function finish() {
      clearTimeout(timeout);
      body.innerHTML = '<div class="tmr-done"><div class="big">' + best + ' &#128293;</div><p style="color:var(--ink-60);margin-top:.4rem;">Best streak. The faster you recall, the deeper it\'s locked in.</p><button class="btn btn-line tmr-start" style="margin-top:1.2rem;">Run it again</button></div>';
      body.querySelector('.tmr-start').addEventListener('click', restart);
    }
    function start() { startBtn.closest('.tmr-intro').style.display = 'none'; body.hidden = false; i = -1; streak = 0; best = 0; render(); }
    function restart() { location.reload(); }
    startBtn.addEventListener('click', start);
  }

  /* ---------- Matrix / grid ---------- */
  document.querySelectorAll('.matrix-item').forEach(function (item) {
    var rows = Array.prototype.slice.call(item.querySelectorAll('tbody tr, .matrix tr[data-answer]'));
    var checkBtn = item.querySelector('.matrix-check');
    var out = item.querySelector('.matrix-result');
    item.querySelectorAll('.mcell button').forEach(function (b) {
      b.addEventListener('click', function () {
        if (item.classList.contains('locked')) return;
        b.closest('tr').querySelectorAll('.mcell button').forEach(function (x) { x.classList.remove('sel'); });
        b.classList.add('sel');
      });
    });
    if (checkBtn) checkBtn.addEventListener('click', function () {
      item.classList.add('locked');
      var right = 0, total = 0;
      item.querySelectorAll('.matrix tr[data-answer]').forEach(function (tr) {
        total++;
        var ans = tr.getAttribute('data-answer');
        var sel = tr.querySelector('.mcell button.sel');
        tr.querySelectorAll('.mcell button').forEach(function (b) { b.setAttribute('disabled', ''); });
        var correctBtn = tr.querySelector('.mcell button[data-col="' + ans + '"]');
        if (correctBtn) correctBtn.classList.add('right');
        if (sel && sel.getAttribute('data-col') === ans) right++;
        else if (sel) sel.classList.add('wrong');
      });
      if (out) { out.hidden = false; out.querySelector('b').textContent = right + ' / ' + total + ' correct'; }
      checkBtn.style.opacity = '0.6'; checkBtn.textContent = 'Locked';
    });
  });

  /* ---------- SBAR builder ---------- */
  document.querySelectorAll('.sbar').forEach(function (sbar) {
    var armed = null;
    var pool = sbar.querySelector('.chip-pool');
    var checkBtn = sbar.querySelector('.sbar-check');
    pool.querySelectorAll('.sbar-chip').forEach(function (chip) {
      chip.addEventListener('click', function () {
        if (chip.classList.contains('used')) return;
        pool.querySelectorAll('.sbar-chip').forEach(function (c) { c.classList.remove('armed'); });
        if (armed === chip) { armed = null; return; }
        chip.classList.add('armed'); armed = chip;
      });
    });
    sbar.querySelectorAll('.sbar-slot').forEach(function (slot) {
      slot.addEventListener('click', function () {
        if (!armed || sbar.classList.contains('locked')) return;
        // return any existing chip in this slot
        var existing = slot.getAttribute('data-chip');
        if (existing) { var ex = pool.querySelector('.sbar-chip[data-id="' + existing + '"]'); if (ex) ex.classList.remove('used'); }
        var placed = slot.querySelector('.placed') || document.createElement('div');
        placed.className = 'placed'; placed.textContent = armed.textContent;
        if (!placed.parentNode) slot.appendChild(placed);
        slot.classList.add('filled');
        slot.setAttribute('data-chip', armed.getAttribute('data-id'));
        armed.classList.add('used'); armed.classList.remove('armed'); armed = null;
      });
    });
    if (checkBtn) checkBtn.addEventListener('click', function () {
      sbar.classList.add('locked');
      var right = 0;
      sbar.querySelectorAll('.sbar-slot').forEach(function (slot) {
        var ok = slot.getAttribute('data-chip') === slot.getAttribute('data-answer');
        slot.classList.add(ok ? 'ok' : 'no'); if (ok) right++;
      });
      var out = sbar.querySelector('.sbar-result');
      if (out) { out.hidden = false; out.querySelector('b').textContent = right + ' / 4 slots correct'; }
      checkBtn.style.opacity = '0.6'; checkBtn.textContent = 'Locked';
    });
  });

  /* ---------- Chart-trend + generic MC (reuse simple checker) ---------- */
  document.querySelectorAll('.mc-item').forEach(function (item) {
    var opts = Array.prototype.slice.call(item.querySelectorAll('.choice'));
    var checkBtn = item.querySelector('.mc-check');
    var rat = item.querySelector('.rationale');
    var picked = null, locked = false;
    opts.forEach(function (o) { o.addEventListener('click', function () {
      if (locked) return; opts.forEach(function (x) { x.classList.remove('sel-choice'); x.style.borderColor=''; }); o.classList.add('sel-choice'); o.style.borderColor = 'var(--coral-500)'; picked = o;
    }); });
    if (checkBtn) checkBtn.addEventListener('click', function () {
      if (locked || !picked) return; locked = true;
      opts.forEach(function (o) { o.setAttribute('disabled',''); if (o.getAttribute('data-correct')==='1') o.classList.add('right'); else if (o===picked) o.classList.add('wrong'); });
      if (rat) rat.classList.add('show'); checkBtn.style.opacity='0.6'; checkBtn.textContent='Locked';
    });
  });

  /* ---------- Free -> Paid gate (demo) ---------- */
  function applyPaid() { document.body.classList.toggle('mls-paid', localStorage.getItem('mlsPaid') === 'true'); }
  applyPaid();
  document.querySelectorAll('[data-unlock]').forEach(function (b) {
    b.addEventListener('click', function (e) { e.preventDefault(); localStorage.setItem('mlsPaid', 'true'); applyPaid();
      var p = document.querySelector('.paid-only'); if (p) p.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    });
  });
  document.querySelectorAll('[data-relock]').forEach(function (b) {
    b.addEventListener('click', function (e) { e.preventDefault(); localStorage.removeItem('mlsPaid'); applyPaid(); window.scrollTo({ top: 0, behavior: 'auto' }); });
  });
})();
