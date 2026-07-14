/* Must Love Scrubs — NCLEX Complete product page
   Schedule quiz, item tagging, Question of the Day (demo until backend). */

(function () {
  'use strict';

  /* ---------- Study-schedule quiz (1 / 2 / 3-month) ---------- */
  var squiz = document.querySelector('[data-squiz]');
  if (squiz) {
    var steps = squiz.querySelectorAll('.q');
    var bar = squiz.querySelector('.sq-progress i');
    var result = squiz.querySelector('.sq-result');
    var planEl = squiz.querySelector('[data-sq-plan]');
    var noteEl = squiz.querySelector('[data-sq-note]');
    var restart = squiz.querySelector('[data-sq-restart]');
    var total = steps.length;
    var current = 0;
    var score = 0;

    var PLANS = {
      1: { plan: '1-Month Plan', note: 'You have a strong base and a close test date — you mainly need reps and timing. The fast track keeps you sharp without dragging it out.' },
      2: { plan: '2-Month Plan', note: 'Enough runway to fix weak areas without cramming — the sweet spot for most students, and where the Pass Guarantee kicks in.' },
      3: { plan: '3-Month Plan', note: 'A gentler daily load with extra concept teaching up front — right if you work full-time or want to rebuild your fundamentals.' }
    };

    function show(i) {
      steps.forEach(function (s, idx) { s.classList.toggle('done', idx !== i); });
      if (bar) bar.style.width = Math.round(((i) / total) * 100) + '%';
    }

    function finish() {
      var avg = score / total; // 1..3
      var key = avg <= 1.6 ? 1 : (avg >= 2.4 ? 3 : 2);
      var pick = PLANS[key];
      if (planEl) planEl.textContent = pick.plan;
      if (noteEl) noteEl.textContent = pick.note;
      steps.forEach(function (s) { s.classList.add('done'); });
      if (bar) bar.style.width = '100%';
      result.classList.add('show');
    }

    squiz.querySelectorAll('.opt').forEach(function (btn) {
      btn.addEventListener('click', function () {
        score += parseInt(btn.getAttribute('data-score'), 10) || 0;
        current++;
        if (current >= total) { finish(); }
        else { show(current); }
      });
    });

    if (restart) restart.addEventListener('click', function () {
      current = 0; score = 0;
      result.classList.remove('show');
      show(0);
    });
  }

  /* ---------- Item tagging (Mastered / Reviewing / Learning) ---------- */
  document.querySelectorAll('[data-tagset]').forEach(function (set) {
    var note = set.parentElement.querySelector('[data-tag-note]');
    var LABELS = {
      mastered: "Filed as Mastered — Esi will re-test this once, later, to keep it locked in.",
      reviewing: "Filed as Reviewing — this joins your spaced-review queue for the coming days.",
      learning: "Filed as Learning — Esi will bring this back soon and more often until it sticks."
    };
    set.querySelectorAll('.tagc').forEach(function (chip) {
      chip.addEventListener('click', function () {
        set.querySelectorAll('.tagc').forEach(function (c) { c.classList.remove('picked'); });
        chip.classList.add('picked');
        if (note) note.textContent = LABELS[chip.getAttribute('data-tag')] || '';
      });
    });
  });

  /* ---------- Question of the Day ---------- */
  var qotd = document.querySelector('[data-qotd]');
  if (qotd) {
    var answered = false;
    var rat = qotd.querySelector('.qrat');
    qotd.querySelectorAll('.qo').forEach(function (opt) {
      opt.addEventListener('click', function () {
        if (answered) return;
        answered = true;
        var correct = opt.getAttribute('data-correct') === '1';
        opt.classList.add(correct ? 'right' : 'wrong');
        if (!correct) {
          qotd.querySelectorAll('.qo').forEach(function (o) {
            if (o.getAttribute('data-correct') === '1') o.classList.add('right');
          });
        }
        if (rat) rat.classList.add('show');
      });
    });

    var channel = 'phone';
    var chWrap = qotd.querySelector('[data-qotd-channel]');
    if (chWrap) chWrap.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function () {
        chWrap.querySelectorAll('button').forEach(function (x) { x.classList.remove('on'); });
        b.classList.add('on');
        channel = b.getAttribute('data-ch');
      });
    });

    var sub = qotd.querySelector('[data-qotd-sub]');
    var done = qotd.querySelector('[data-qotd-done]');
    if (sub && done) sub.addEventListener('click', function () {
      done.hidden = false;
      done.textContent = channel === 'email'
        ? '✓ You\'re set — a fresh question hits your inbox every morning.'
        : '✓ You\'re set — a fresh question texts to your phone every morning.';
    });
  }
})();
