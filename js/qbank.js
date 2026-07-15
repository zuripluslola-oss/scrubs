/* Must Love Scrubs — Question Bank (interactive sample).
   Filter by category, answer, see rationale for every option, answer stats,
   Mastered/Reviewing/Learning tagging, timer, score. Demo until backend. */

(function () {
  'use strict';
  var root = document.querySelector('.qbank');
  if (!root) return;

  var dataEl = root.querySelector('script[data-qbank]');
  var ALL = JSON.parse(dataEl.textContent);
  function md(s) { return String(s == null ? '' : s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>'); }
  var stage = root.querySelector('[data-qb-stage]');
  var gate = root.querySelector('[data-qb-gate]');
  var scoreEl = root.querySelector('[data-qb-score]');
  var progEl = root.querySelector('[data-qb-prog]');
  var timerEl = root.querySelector('[data-qb-timer]');

  var list = ALL.slice();
  var idx = 0, answered = false, chosen = -1;
  var correct = 0, total = 0;

  // timer
  var start = Date.now();
  setInterval(function () {
    var s = Math.floor((Date.now() - start) / 1000);
    timerEl.textContent = Math.floor(s / 60) + ':' + ('0' + (s % 60)).slice(-2);
  }, 1000);

  function esc(s) { return s; }
  function updateMeta() {
    scoreEl.textContent = correct + '/' + total;
    progEl.textContent = Math.min(idx + 1, list.length) + '/' + list.length;
  }

  function render() {
    answered = false; chosen = -1;
    if (idx >= list.length) { stage.hidden = true; gate.hidden = false; updateMeta(); return; }
    stage.hidden = false; gate.hidden = true;
    var q = list[idx];
    var opts = q.opts.map(function (o, i) {
      return '<button class="qb-opt" data-i="' + i + '"><span class="qb-key">' + 'ABCD'[i] + '</span><span class="qb-txt">' + md(o.t) + '</span></button>';
    }).join('');
    stage.innerHTML =
      '<div class="qb-q">' +
        '<span class="qb-cat">' + q.cat + '</span>' +
        '<p class="qb-stem">' + md(q.stem) + '</p>' +
        '<div class="qb-opts">' + opts + '</div>' +
        '<div class="qb-actions"><button class="btn btn-coral qb-submit" disabled>Submit answer</button></div>' +
        '<div class="qb-reveal" hidden></div>' +
      '</div>';
    updateMeta();

    var optButtons = stage.querySelectorAll('.qb-opt');
    optButtons.forEach(function (b) {
      b.addEventListener('click', function () {
        if (answered) return;
        optButtons.forEach(function (x) { x.classList.remove('sel'); });
        b.classList.add('sel');
        chosen = parseInt(b.getAttribute('data-i'), 10);
        stage.querySelector('.qb-submit').disabled = false;
      });
    });
    stage.querySelector('.qb-submit').addEventListener('click', submit);
  }

  function submit() {
    if (answered || chosen < 0) return;
    answered = true;
    var q = list[idx];
    total++;
    if (chosen === q.correct) correct++;
    updateMeta();

    var optButtons = stage.querySelectorAll('.qb-opt');
    optButtons.forEach(function (b) {
      var i = parseInt(b.getAttribute('data-i'), 10);
      b.disabled = true;
      if (i === q.correct) b.classList.add('right');
      else if (i === chosen) b.classList.add('wrong');
      // answer-stats bar
      var bar = document.createElement('span');
      bar.className = 'qb-pct';
      bar.innerHTML = '<i style="width:' + q.pct[i] + '%"></i><b>' + q.pct[i] + '%</b>';
      b.appendChild(bar);
    });

    var rats = q.opts.map(function (o, i) {
      var cls = i === q.correct ? 'ok' : 'no';
      return '<li class="' + cls + '"><b>' + 'ABCD'[i] + '.</b> ' + md(o.r) + '</li>';
    }).join('');
    var verdict = chosen === q.correct
      ? '<span class="qb-verdict ok">Correct</span>'
      : '<span class="qb-verdict no">Not quite</span>';
    var pearl = q.pearl ? '<div class="qb-tip qb-pearl"><b>💡 Memory trick.</b> ' + md(q.pearl) + '</div>' : '';

    var rev = stage.querySelector('.qb-reveal');
    rev.hidden = false;
    rev.innerHTML =
      verdict +
      '<div class="qb-rationale"><b>Why each option:</b><ul>' + rats + '</ul></div>' +
      (q.tip ? '<div class="qb-tip"><b>📝 Tip.</b> ' + md(q.tip) + '</div>' : '') +
      pearl +
      '<div class="qb-tagrow"><span>Tag this:</span>' +
        '<button class="tagc mastered" data-tag>Mastered</button>' +
        '<button class="tagc reviewing" data-tag>Reviewing</button>' +
        '<button class="tagc learning" data-tag>Learning</button></div>' +
      '<div class="qb-actions"><button class="btn btn-coral qb-next">' +
        (idx + 1 >= list.length ? 'See results' : 'Next question') + ' &rarr;</button></div>';

    rev.querySelectorAll('[data-tag]').forEach(function (t) {
      t.addEventListener('click', function () {
        rev.querySelectorAll('[data-tag]').forEach(function (x) { x.classList.remove('picked'); });
        t.classList.add('picked');
      });
    });
    rev.querySelector('.qb-next').addEventListener('click', function () { idx++; render(); });
    stage.querySelector('.qb-submit').disabled = true;
    stage.querySelector('.qb-submit').textContent = 'Answered';
  }

  // category filter
  root.querySelectorAll('.qb-chip').forEach(function (chip) {
    chip.addEventListener('click', function () {
      root.querySelectorAll('.qb-chip').forEach(function (c) { c.classList.remove('on'); });
      chip.classList.add('on');
      var cat = chip.getAttribute('data-cat');
      list = cat === 'All' ? ALL.slice() : ALL.filter(function (q) { return q.cat === cat; });
      idx = 0; correct = 0; total = 0;
      render();
    });
  });

  render();
})();
