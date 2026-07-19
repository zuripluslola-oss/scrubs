/* Must Love Scrubs — Study Plan Calendar (the conductor).
   Builds a day-by-day plan from proven learning science: spaced repetition,
   active recall, interleaving. Each day schedules real activities (read,
   flashcards, review, pop quiz, case study, mnemonic game, review test,
   readiness exam) that link to the actual tools. Demo state via localStorage. */

(function () {
  'use strict';
  var root = document.querySelector('[data-planner]');
  if (!root) return;

  var TOPICS = [
    { t: 'Pharmacology', link: 'flashcards.html' },
    { t: 'Lab Values', link: 'flashcards.html' },
    { t: 'Cardiovascular', link: 'flashcards.html' },
    { t: 'Respiratory', link: 'flashcards.html' },
    { t: 'Endocrine', link: 'flashcards.html' },
    { t: 'Fundamentals & Safety', link: 'flashcards.html' },
    { t: 'Maternal / Newborn', link: 'flashcards.html' },
    { t: 'Pediatrics', link: 'flashcards.html' },
    { t: 'Critical Care / ICU', link: 'flashcards.html' },
    { t: 'Emergency / ER', link: 'flashcards.html' },
    { t: 'Mental Health', link: 'flashcards.html' },
    { t: 'Med-Surg', link: 'flashcards.html' }
  ];
  var WEEKS = { 1: 4, 2: 8, 3: 13, 6: 26 };

  var lenWrap = root.querySelector('[data-plan-len]');
  var startInp = root.querySelector('[data-plan-start]');
  var goBtn = root.querySelector('[data-plan-go]');
  var cal = root.querySelector('[data-plan-cal]');
  var doneEl = root.querySelector('[data-plan-done]'), totalEl = root.querySelector('[data-plan-total]');
  var streakEl = root.querySelector('[data-plan-streak]'), bar = root.querySelector('[data-plan-bar]');
  var modal = document.querySelector('[data-plan-modal]'), modalBody = document.querySelector('[data-plan-modal-body]');

  var len = 2, days = [], done = {};
  try { var saved = JSON.parse(localStorage.getItem('mlsPlan')) || {}; done = saved.done || {}; if (saved.len) len = saved.len; if (saved.start) startInp.value = saved.start; } catch (e) {}
  if (!startInp.value) startInp.value = new Date().toISOString().slice(0, 10);
  lenWrap.querySelectorAll('button').forEach(function (b) { b.classList.toggle('on', +b.getAttribute('data-len') === len); });

  function save() { try { localStorage.setItem('mlsPlan', JSON.stringify({ len: len, start: startInp.value, done: done })); } catch (e) {} }
  function key(d) { return d.toISOString().slice(0, 10); }
  function addDays(d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; }
  function fmt(d) { return d.toLocaleDateString(undefined, { weekday: 'long', month: 'long', day: 'numeric' }); }

  var A = {
    read:   { c: 'read',   label: 'Read', link: 'nclex-guide.html' },
    cards:  { c: 'cards',  label: 'Flashcards', link: 'flashcards.html' },
    review: { c: 'review', label: 'Review', link: 'flashcards.html' },
    quiz:   { c: 'quiz',   label: 'Pop quiz', link: 'tests.html' },
    case:   { c: 'case',   label: 'Case study', link: 'nclex-complete.html' },
    game:   { c: 'game',   label: 'Mnemonic game', link: 'flashcards.html' },
    test:   { c: 'test',   label: 'Review test', link: 'tests.html' },
    exam:   { c: 'exam',   label: 'Readiness exam', link: 'tests.html' }
  };

  function build() {
    var start = new Date(startInp.value + 'T00:00:00');
    var total = WEEKS[len] * 7;
    days = [];
    var studyIdx = 0;
    for (var i = 0; i < total; i++) {
      var d = addDays(start, i), dow = d.getDay();
      var day = { date: d, key: key(d), acts: [], rest: false, milestone: false };
      if (dow === 0) { day.rest = true; day.acts = [{ c: 'rest', label: 'Rest & recharge', link: null, detail: 'Recovery matters — sleep consolidates memory. Optional: 10 min light flashcard review.' }]; }
      else {
        var focus = TOPICS[studyIdx % TOPICS.length];
        day.focus = focus.t;
        day.acts.push(mk('read', focus.t, 'Read the ' + focus.t + ' overview — build the concept first.'));
        day.acts.push(mk('cards', focus.t, 'New ' + focus.t + ' flashcards (active recall).', 'flashcards.html'));
        if (studyIdx >= 3) { var rev = TOPICS[(studyIdx - 3) % TOPICS.length].t; day.acts.push(mk('review', rev, 'Spaced review: ' + rev + ' (you learned it a few days ago — revisit before you forget).', 'flashcards.html')); }
        day.acts.push(mk('quiz', focus.t, '10-question pop quiz on ' + focus.t + ' — retrieve, don\'t reread.'));
        if (dow === 2 || dow === 5) day.acts.push(mk('case', focus.t, 'Work a Next Gen case study — clinical judgment in action.'));
        if (dow === 1 || dow === 4) day.acts.push(mk('game', focus.t, 'Mnemonic game (Match or Speed round) to lock in the memory tricks.'));
        if (dow === 6) { day.acts.push(mk('test', 'This week', 'Weekly review test — mixed topics from the past week (interleaving).')); day.milestone = true; }
        if (i > 0 && i % 14 === 0) { day.acts.push(mk('exam', 'Milestone', 'Full-length readiness exam — see your pass-chance and weakest areas.')); day.milestone = true; }
        studyIdx++;
      }
      days.push(day);
    }
    save(); render();
  }
  function mk(type, topic, detail, link) { var a = A[type]; return { c: a.c, label: a.label, topic: topic, detail: detail, link: link || a.link }; }

  function studyDayCount() { return days.filter(function (d) { return !d.rest; }).length; }
  function meta() {
    var total = studyDayCount();
    var completed = days.filter(function (d) { return !d.rest && done[d.key]; }).length;
    doneEl.textContent = completed; totalEl.textContent = total;
    bar.style.width = total ? Math.round(completed / total * 100) + '%' : '0%';
    // streak: consecutive completed study days ending at the most recent completed
    var s = 0; for (var i = days.length - 1; i >= 0; i--) { if (days[i].rest) continue; if (done[days[i].key]) s++; else if (s > 0) break; }
    streakEl.textContent = s;
  }

  function render() {
    var todayKey = key(new Date());
    // pad to start on Sunday
    var first = days[0].date, pad = first.getDay();
    var cells = [];
    for (var p = 0; p < pad; p++) cells.push('<div class="cal-cell empty"></div>');
    days.forEach(function (d, idx) {
      var chips = d.acts.slice(0, 4).map(function (a) { return '<span class="cal-dot ' + a.c + '"></span>'; }).join('');
      var cls = 'cal-cell' + (d.rest ? ' rest' : '') + (d.key === todayKey ? ' today' : '') + (done[d.key] ? ' done' : '') + (d.milestone ? ' milestone' : '');
      cells.push('<button class="' + cls + '" data-idx="' + idx + '">' +
        '<span class="cal-num">' + d.date.getDate() + '</span>' +
        (done[d.key] ? '<span class="cal-check">✓</span>' : '') +
        '<span class="cal-dots">' + chips + '</span></button>');
    });
    var wk = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].map(function (w) { return '<div class="cal-wd">' + w + '</div>'; }).join('');
    cal.innerHTML = '<div class="cal-grid">' + wk + cells.join('') + '</div>';
    cal.querySelectorAll('.cal-cell[data-idx]').forEach(function (b) { b.addEventListener('click', function () { openDay(days[+b.getAttribute('data-idx')]); }); });
    meta();
  }

  function openDay(d) {
    var acts = d.acts.map(function (a) {
      var link = a.link ? '<a class="btn btn-line pd-go" href="' + a.link + '">Start &rarr;</a>' : '';
      return '<div class="pd-act"><span class="cal-dot ' + a.c + '"></span><div class="pd-act-body"><b>' + a.label + (a.topic ? ' · ' + a.topic : '') + '</b><p>' + a.detail + '</p></div>' + link + '</div>';
    }).join('');
    var doneBtn = d.rest ? '' : '<button class="btn btn-coral pd-complete">' + (done[d.key] ? '✓ Completed — undo' : 'Mark day complete') + '</button>';
    modalBody.innerHTML = '<span class="lesson-label" style="color:var(--coral-500);">' + (d.milestone ? 'Milestone day' : d.rest ? 'Rest day' : 'Study day') + '</span>' +
      '<h3 style="margin:0.3rem 0 1rem;">' + fmt(d.date) + '</h3>' + acts +
      '<div style="margin-top:1.2rem;">' + doneBtn + '</div>';
    var cb = modalBody.querySelector('.pd-complete');
    if (cb) cb.addEventListener('click', function () { if (done[d.key]) delete done[d.key]; else done[d.key] = true; save(); render(); openDay(d); });
    modal.hidden = false;
  }
  function close() { modal.hidden = true; }
  document.querySelector('[data-plan-close]').addEventListener('click', close);
  modal.addEventListener('click', function (e) { if (e.target === modal) close(); });

  lenWrap.querySelectorAll('button').forEach(function (b) { b.addEventListener('click', function () { lenWrap.querySelectorAll('button').forEach(function (x) { x.classList.remove('on'); }); b.classList.add('on'); len = +b.getAttribute('data-len'); }); });
  goBtn.addEventListener('click', build);
  build();
})();
