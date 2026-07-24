/* Must Love Scrubs — Study Plan Calendar (the conductor), now personalized.
   Tell it: exam (RN/PN), plan length, up to 2 specialties, which days you can
   study, and time per day. It builds a schedule AROUND your life and runs
   reading, flashcards, spaced review, pop quizzes, case studies, mnemonic
   games, weekly tests, and readiness exams — the same adaptive engine (spaced
   repetition, active recall, interleaving) as the CAT. Demo via localStorage. */

(function () {
  'use strict';
  var root = document.querySelector('[data-planner]');
  if (!root) return;

  var CORE = ['Pharmacology', 'Lab Values', 'Cardiovascular', 'Respiratory', 'Endocrine',
    'Fundamentals & Safety', 'Maternal / Newborn', 'Pediatrics', 'Mental Health', 'Med-Surg',
    'Management of Care', 'Reduction of Risk'];
  var WEEKS = { 1: 4, 2: 8, 3: 13, 6: 26 };
  var HOURS_ACTS = { '30m': 2, '1h': 3, '2h': 4, '3h': 6 };

  var lenWrap = root.querySelector('[data-plan-len]');
  var examWrap = root.querySelector('[data-plan-exam]');
  var specsWrap = root.querySelector('[data-plan-specs]');
  var daysWrap = root.querySelector('[data-plan-days]');
  var hoursWrap = root.querySelector('[data-plan-hours]');
  var startInp = root.querySelector('[data-plan-start]');
  var goBtn = root.querySelector('[data-plan-go]');
  var cal = root.querySelector('[data-plan-cal]');
  var doneEl = root.querySelector('[data-plan-done]'), totalEl = root.querySelector('[data-plan-total]');
  var streakEl = root.querySelector('[data-plan-streak]'), bar = root.querySelector('[data-plan-bar]');
  var modal = document.querySelector('[data-plan-modal]'), modalBody = document.querySelector('[data-plan-modal-body]');

  var len = 2, exam = 'RN', specs = [], availDays = [1, 2, 3, 4, 5, 6], hours = '1h';
  var days = [], done = {};
  try {
    var saved = JSON.parse(localStorage.getItem('mlsPlan')) || {};
    done = saved.done || {};
    if (saved.len) len = saved.len;
    if (saved.exam) exam = saved.exam;
    if (Array.isArray(saved.specs)) specs = saved.specs;
    if (Array.isArray(saved.availDays)) availDays = saved.availDays;
    if (saved.hours) hours = saved.hours;
    if (saved.start) startInp.value = saved.start;
  } catch (e) {}
  if (!startInp.value) startInp.value = new Date().toISOString().slice(0, 10);

  function setSeg(wrap, attr, val) { if (!wrap) return; wrap.querySelectorAll('button').forEach(function (b) { b.classList.toggle('on', b.getAttribute(attr) === String(val)); }); }
  setSeg(lenWrap, 'data-len', len);
  setSeg(examWrap, 'data-exam', exam);
  setSeg(hoursWrap, 'data-hours', hours);
  if (specsWrap) specsWrap.querySelectorAll('button').forEach(function (b) { b.classList.toggle('on', specs.indexOf(b.getAttribute('data-spec')) >= 0); });
  if (daysWrap) daysWrap.querySelectorAll('button').forEach(function (b) { b.classList.toggle('on', availDays.indexOf(+b.getAttribute('data-day')) >= 0); });

  function save() { try { localStorage.setItem('mlsPlan', JSON.stringify({ len: len, exam: exam, specs: specs, availDays: availDays, hours: hours, start: startInp.value, done: done })); } catch (e) {} }
  function key(d) { return d.toISOString().slice(0, 10); }
  function addDays(d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; }
  function fmt(d) { return d.toLocaleDateString(undefined, { weekday: 'long', month: 'long', day: 'numeric' }); }

  var A = {
    read:   { c: 'read',   label: 'Read', link: 'nclex-guide.html' },
    cards:  { c: 'cards',  label: 'Flashcards', link: 'flashcards.html' },
    review: { c: 'review', label: 'Review', link: 'flashcards.html' },
    quiz:   { c: 'quiz',   label: 'Pop quiz', link: 'tests.html' },
    case:   { c: 'case',   label: 'Case study', link: 'tests.html' },
    game:   { c: 'game',   label: 'Mnemonic game', link: 'flashcards.html' },
    test:   { c: 'test',   label: 'Review test', link: 'tests.html' },
    exam:   { c: 'exam',   label: 'Readiness exam', link: 'tests.html' }
  };
  function mk(type, topic, detail, link) { var a = A[type]; return { c: a.c, label: a.label, topic: topic, detail: detail, link: link || a.link }; }

  function topicPool() {
    var pool = CORE.slice();
    // weight chosen specialties by adding them twice so they recur more often
    specs.forEach(function (s) { pool.push(s); pool.push(s); });
    return pool;
  }

  function build() {
    var start = new Date(startInp.value + 'T00:00:00');
    var total = WEEKS[len] * 7;
    var pool = topicPool();
    var target = HOURS_ACTS[hours] || 3;
    var avail = availDays.length ? availDays : [1, 2, 3, 4, 5, 6];
    var maxDay = Math.max.apply(null, avail);
    days = [];
    var studyIdx = 0;
    for (var i = 0; i < total; i++) {
      var d = addDays(start, i), dow = d.getDay();
      var day = { date: d, key: key(d), acts: [], rest: false, milestone: false };
      if (avail.indexOf(dow) < 0) {
        day.rest = true;
        day.acts = [{ c: 'rest', label: 'Day off', link: null, detail: 'A scheduled rest day — recovery consolidates memory. Optional: 10 min of light card review.' }];
      } else {
        var focus = pool[studyIdx % pool.length];
        day.focus = focus;
        // priority order so short days still cover the highest-yield work
        var base = [];
        base.push(mk('cards', focus, 'New ' + focus + ' flashcards — active recall, adaptive levels rise as you improve.'));
        base.push(mk('quiz', focus, '10-question pop quiz on ' + focus + ' — retrieve, don\'t reread.'));
        base.push(mk('read', focus, 'Read the ' + focus + ' overview — build the concept first.'));
        if (studyIdx >= 3) { var rev = pool[(studyIdx - 3) % pool.length]; base.splice(2, 0, mk('review', rev, 'Spaced review: ' + rev + ' — revisit it right before you\'d forget.')); }
        base.push((studyIdx % 2 === 0) ? mk('case', focus, 'Work a Next Gen case study — clinical judgment in action.') : mk('game', focus, 'Mnemonic game to lock in the memory tricks.'));
        var acts = base.slice(0, Math.max(2, target));
        // milestones always added (not trimmed)
        if (dow === maxDay) { acts.push(mk('test', 'This week', 'Weekly review test — mixed topics from the week (interleaving).')); day.milestone = true; }
        if (studyIdx > 0 && studyIdx % 14 === 0) { acts.push(mk('exam', 'Milestone', 'Full-length readiness exam — see your pass-chance and weakest areas.')); day.milestone = true; }
        day.acts = acts;
        studyIdx++;
      }
      days.push(day);
    }
    save(); render();
  }

  function studyDayCount() { return days.filter(function (d) { return !d.rest; }).length; }
  function meta() {
    var total = studyDayCount();
    var completed = days.filter(function (d) { return !d.rest && done[d.key]; }).length;
    if (doneEl) doneEl.textContent = completed;
    if (totalEl) totalEl.textContent = total;
    if (bar) bar.style.width = total ? Math.round(completed / total * 100) + '%' : '0%';
    var s = 0; for (var i = days.length - 1; i >= 0; i--) { if (days[i].rest) continue; if (done[days[i].key]) s++; else if (s > 0) break; }
    if (streakEl) streakEl.textContent = s;
  }

  function render() {
    if (!days.length) return;
    var todayKey = key(new Date());
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
    var wk = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(function (w) { return '<div class="cal-wd">' + w + '</div>'; }).join('');
    cal.innerHTML = '<div class="cal-head-sum">' + exam.replace('RN', 'NCLEX-RN').replace('PN', 'NCLEX-PN') +
      ' · ' + len + '-month plan' + (specs.length ? ' · ' + specs.join(' + ') : '') + ' · ' + hours + '/day</div>' +
      '<div class="cal-grid">' + wk + cells.join('') + '</div>';
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

  // ---- control wiring ----
  function singleSeg(wrap, attr, set) {
    if (!wrap) return;
    wrap.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function () {
        wrap.querySelectorAll('button').forEach(function (x) { x.classList.remove('on'); });
        b.classList.add('on'); set(b.getAttribute(attr));
      });
    });
  }
  singleSeg(lenWrap, 'data-len', function (v) { len = +v; });
  singleSeg(examWrap, 'data-exam', function (v) { exam = v; });
  singleSeg(hoursWrap, 'data-hours', function (v) { hours = v; });
  if (specsWrap) specsWrap.querySelectorAll('button').forEach(function (b) {
    b.addEventListener('click', function () {
      var s = b.getAttribute('data-spec'), on = b.classList.contains('on');
      if (on) { b.classList.remove('on'); specs = specs.filter(function (x) { return x !== s; }); }
      else { if (specs.length >= 2) return; b.classList.add('on'); specs.push(s); }
    });
  });
  if (daysWrap) daysWrap.querySelectorAll('button').forEach(function (b) {
    b.addEventListener('click', function () {
      var day = +b.getAttribute('data-day'), on = b.classList.contains('on');
      if (on) { b.classList.remove('on'); availDays = availDays.filter(function (x) { return x !== day; }); }
      else { b.classList.add('on'); availDays.push(day); }
    });
  });
  goBtn.addEventListener('click', build);
  build();
})();
