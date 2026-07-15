/* Must Love Scrubs — Question Bank (interactive sample).
   Item types: mc (single answer), sata (select all), matrix (grid).
   Rationale for every option, answer stats, tagging, timer, score. Demo. */

(function () {
  'use strict';
  var root = document.querySelector('.qbank');
  if (!root) return;

  var ALL = JSON.parse(root.querySelector('script[data-qbank]').textContent);
  function md(s) { return String(s == null ? '' : s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>'); }
  var LET = 'ABCDEFGH';

  var stage = root.querySelector('[data-qb-stage]');
  var gate = root.querySelector('[data-qb-gate]');
  var scoreEl = root.querySelector('[data-qb-score]');
  var progEl = root.querySelector('[data-qb-prog]');
  var timerEl = root.querySelector('[data-qb-timer]');

  var list = ALL.slice();
  var idx = 0, answered = false;
  var pick = null;              // mc: int | sata: {} set | matrix: {row:col}
  var correct = 0, total = 0;

  var start = Date.now();
  setInterval(function () {
    var s = Math.floor((Date.now() - start) / 1000);
    timerEl.textContent = Math.floor(s / 60) + ':' + ('0' + (s % 60)).slice(-2);
  }, 1000);

  function meta() {
    scoreEl.textContent = correct + '/' + total;
    progEl.textContent = Math.min(idx + 1, list.length) + '/' + list.length;
  }
  function submitBtn() { return stage.querySelector('.qb-submit'); }

  function render() {
    answered = false; pick = null;
    if (idx >= list.length) { stage.hidden = true; gate.hidden = false; meta(); return; }
    stage.hidden = false; gate.hidden = true;
    var q = list[idx];
    var body =
      '<span class="qb-cat">' + q.cat + '</span>' +
      '<p class="qb-stem">' + md(q.stem) + '</p>' +
      (q.type === 'matrix' ? renderMatrix(q) : renderOpts(q)) +
      '<div class="qb-actions"><button class="btn btn-coral qb-submit" disabled>Submit answer</button></div>' +
      '<div class="qb-reveal" hidden></div>';
    stage.innerHTML = '<div class="qb-q">' + body + '</div>';
    meta();
    if (q.type === 'mc') wireMC(q);
    else if (q.type === 'sata') wireSATA(q);
    else if (q.type === 'matrix') wireMatrix(q);
    submitBtn().addEventListener('click', submit);
  }

  /* ---------- MC + SATA options ---------- */
  function renderOpts(q) {
    var hint = q.type === 'sata' ? '<p class="qb-hint">Select all that apply.</p>' : '';
    var opts = q.opts.map(function (o, i) {
      return '<button class="qb-opt" data-i="' + i + '"><span class="qb-key">' + LET[i] + '</span><span class="qb-txt">' + md(o.t) + '</span></button>';
    }).join('');
    return hint + '<div class="qb-opts">' + opts + '</div>';
  }
  function wireMC(q) {
    var btns = stage.querySelectorAll('.qb-opt');
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        if (answered) return;
        btns.forEach(function (x) { x.classList.remove('sel'); });
        b.classList.add('sel');
        pick = parseInt(b.getAttribute('data-i'), 10);
        submitBtn().disabled = false;
      });
    });
  }
  function wireSATA(q) {
    pick = {};
    var btns = stage.querySelectorAll('.qb-opt');
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        if (answered) return;
        var i = b.getAttribute('data-i');
        if (pick[i]) { delete pick[i]; b.classList.remove('sel'); }
        else { pick[i] = true; b.classList.add('sel'); }
        submitBtn().disabled = Object.keys(pick).length === 0;
      });
    });
  }

  /* ---------- Matrix ---------- */
  function renderMatrix(q) {
    var head = '<tr><th></th>' + q.cols.map(function (c) { return '<th>' + c + '</th>'; }).join('') + '</tr>';
    var rows = q.rows.map(function (r, ri) {
      var cells = q.cols.map(function (c, ci) {
        return '<td class="qb-cell"><button data-row="' + ri + '" data-col="' + ci + '" aria-label="' + c + '"></button></td>';
      }).join('');
      return '<tr><td class="qb-rlabel">' + md(r.t) + '</td>' + cells + '</tr>';
    }).join('');
    return '<div class="qb-matrix-wrap"><table class="qb-matrix"><thead>' + head + '</thead><tbody>' + rows + '</tbody></table></div>';
  }
  function wireMatrix(q) {
    pick = {};
    stage.querySelectorAll('.qb-cell button').forEach(function (b) {
      b.addEventListener('click', function () {
        if (answered) return;
        var ri = b.getAttribute('data-row');
        stage.querySelectorAll('.qb-cell button[data-row="' + ri + '"]').forEach(function (x) { x.classList.remove('sel'); });
        b.classList.add('sel');
        pick[ri] = parseInt(b.getAttribute('data-col'), 10);
        submitBtn().disabled = Object.keys(pick).length < q.rows.length;
      });
    });
  }

  /* ---------- submit / scoring ---------- */
  function submit() {
    if (answered) return;
    var q = list[idx];
    answered = true; total++;
    var isCorrect = false, body = '';

    if (q.type === 'mc') {
      isCorrect = pick === q.correct;
      stage.querySelectorAll('.qb-opt').forEach(function (b) {
        var i = parseInt(b.getAttribute('data-i'), 10);
        b.disabled = true;
        if (i === q.correct) b.classList.add('right');
        else if (i === pick) b.classList.add('wrong');
        var bar = document.createElement('span');
        bar.className = 'qb-pct';
        bar.innerHTML = '<i style="width:' + q.pct[i] + '%"></i><b>' + q.pct[i] + '%</b>';
        b.appendChild(bar);
      });
      body = optRationale(q, function (i) { return i === q.correct ? 'ok' : 'no'; });
    }
    else if (q.type === 'sata') {
      var cset = {}; q.correct.forEach(function (i) { cset[i] = true; });
      var exact = Object.keys(cset).length === Object.keys(pick).length &&
                  q.correct.every(function (i) { return pick[i]; });
      isCorrect = exact;
      stage.querySelectorAll('.qb-opt').forEach(function (b) {
        var i = parseInt(b.getAttribute('data-i'), 10);
        b.disabled = true;
        var sel = !!pick[i], isC = !!cset[i];
        if (isC && sel) b.classList.add('right');
        else if (isC && !sel) b.classList.add('missed');
        else if (!isC && sel) b.classList.add('wrong');
      });
      body = optRationale(q, function (i) { return cset[i] ? 'ok' : 'no'; }) +
        '<p class="qb-note">Select-all is all-or-nothing here — every right answer, and none of the wrong ones.</p>';
    }
    else if (q.type === 'matrix') {
      var allRight = true;
      q.rows.forEach(function (r, ri) {
        var chosen = pick[ri];
        stage.querySelectorAll('.qb-cell button[data-row="' + ri + '"]').forEach(function (b) {
          var ci = parseInt(b.getAttribute('data-col'), 10);
          b.disabled = true;
          if (ci === r.correct && ci === chosen) b.classList.add('right');
          else if (ci === chosen && ci !== r.correct) b.classList.add('wrong');
          else if (ci === r.correct) b.classList.add('should');
        });
        if (chosen !== r.correct) allRight = false;
      });
      isCorrect = allRight;
      var rrows = q.rows.map(function (r) {
        return '<li class="ok"><b>' + md(r.t) + '</b> — ' + md(r.r || q.cols[r.correct]) + '</li>';
      }).join('');
      body = '<div class="qb-rationale"><b>Why each row:</b><ul>' + rrows + '</ul></div>';
    }

    if (isCorrect) correct++;
    meta();
    showReveal(q, isCorrect, body);
    submitBtn().disabled = true; submitBtn().textContent = 'Answered';
  }

  function optRationale(q, clsFor) {
    var items = q.opts.map(function (o, i) {
      return '<li class="' + clsFor(i) + '"><b>' + LET[i] + '.</b> ' + md(o.r) + '</li>';
    }).join('');
    return '<div class="qb-rationale"><b>Why each option:</b><ul>' + items + '</ul></div>';
  }

  function showReveal(q, isCorrect, bodyHTML) {
    var verdict = isCorrect
      ? '<span class="qb-verdict ok">Correct</span>'
      : '<span class="qb-verdict no">Not quite</span>';
    var rev = stage.querySelector('.qb-reveal');
    rev.hidden = false;
    rev.innerHTML =
      verdict + bodyHTML +
      (q.tip ? '<div class="qb-tip"><b>📝 Tip.</b> ' + md(q.tip) + '</div>' : '') +
      (q.pearl ? '<div class="qb-tip qb-pearl"><b>💡 Memory trick.</b> ' + md(q.pearl) + '</div>' : '') +
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
  }

  /* ---------- category filter ---------- */
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
