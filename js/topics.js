/* Must Love Scrubs — Topic Hubs.
   Each topic gathers every related resource in labeled sections (Learn it,
   Apply it, Practice, Review, Reference) so a student sees everything on one
   topic in one place. Links to the tool pages; reference items are named. */

(function () {
  'use strict';
  var root = document.querySelector('.topichubs');
  if (!root) return;

  var ICON = {
    heartbeat: 'M3 12h4l2-5 3 9 2-5h4',
    lungs: 'M12 4v9M12 9c0 5-1.5 8-4.5 8C5 17 4 15 4 12c0-2 .5-4 2-5.5M12 9c0 5 1.5 8 4.5 8 2.5 0 3.5-2 3.5-5 0-2-.5-4-2-5.5',
    drop: 'M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z',
    shield: 'M12 3l8 3v6c0 4.5-3.2 7.6-8 9-4.8-1.4-8-4.5-8-9V6z',
    sheet: 'M6 2h9l5 5v15H6zM14 2v6h6M9 13h7M9 17h7'
  };
  function svg(name) {
    var d = ICON[name] || ICON.sheet;
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
      d.split('M').filter(Boolean).map(function (p) { return '<path d="M' + p + '"/>'; }).join('') + '</svg>';
  }

  var ALL = JSON.parse(root.querySelector('script[data-topics]').textContent);
  var grid = root.querySelector('[data-th-grid]');
  var chipsWrap = root.querySelector('[data-th-chips]');
  var searchInp = root.querySelector('[data-th-search]');
  var countEl = root.querySelector('[data-th-count]');
  var emptyEl = root.querySelector('[data-th-empty]');

  var cat = 'All', q = '';
  function esc(s) { return String(s == null ? '' : s); }
  function chips(items, href) {
    return (items || []).map(function (x) {
      return '<a class="th-ref" href="' + href + '">' + esc(x) + '</a>';
    }).join('');
  }

  function filtered() {
    var qq = q.trim().toLowerCase();
    return ALL.filter(function (t) {
      if (cat !== 'All' && t.category !== cat) return false;
      if (!qq) return true;
      return (t.title + ' ' + t.category + ' ' + t.summary + ' ' + (t.drugs || []).join(' ')).toLowerCase().indexOf(qq) >= 0;
    });
  }

  function section(label, inner) {
    if (!inner) return '';
    return '<div class="th-sec"><span class="th-lbl">' + label + '</span><div class="th-links">' + inner + '</div></div>';
  }

  function topicHTML(t) {
    var learn = t.patho ? '<a class="btn btn-line th-go" href="patho.html">Pathophysiology &rarr;</a>' : '';
    var apply = t.careplan ? '<a class="btn btn-line th-go" href="care-plans.html">Care plan &rarr;</a>' : '';
    var practice = '<a class="btn btn-coral th-go" href="tests.html">Take a test &rarr;</a><a class="btn btn-line th-go" href="qbank.html">Question bank &rarr;</a>';
    var review = '<a class="btn btn-line th-go" href="flashcards.html">Flashcards' + (t.deck ? ' · ' + esc(t.deck) : '') + ' &rarr;</a>';
    var ref =
      (t.drugs && t.drugs.length ? '<div class="th-refrow"><span>Drugs:</span>' + chips(t.drugs, 'drugs.html') + '</div>' : '') +
      (t.labs && t.labs.length ? '<div class="th-refrow"><span>Labs:</span>' + chips(t.labs, 'lab-values.html') + '</div>' : '') +
      (t.cheatsheets && t.cheatsheets.length ? '<div class="th-refrow"><span>Cheat sheets:</span>' + chips(t.cheatsheets, 'cheatsheets.html') + '</div>' : '') +
      (t.mnemonics && t.mnemonics.length ? '<div class="th-refrow"><span>Mnemonics:</span>' + chips(t.mnemonics, 'mnemonics.html') + '</div>' : '');
    return '<div class="th-card">' +
      '<button class="th-head"><span class="th-ic">' + svg(t.icon) + '</span>' +
      '<span class="th-head-txt"><b>' + esc(t.title) + '</b><small>' + esc(t.summary) + '</small></span>' +
      '<span class="th-cat-tag">' + esc(t.category) + '</span><span class="th-caret">▾</span></button>' +
      '<div class="th-body">' +
        section('📖 Learn it', learn) +
        section('🩺 Apply it', apply) +
        section('✍️ Practice', practice) +
        section('🔁 Review', review) +
        (ref ? '<div class="th-sec"><span class="th-lbl">📚 Reference</span>' + ref + '</div>' : '') +
      '</div></div>';
  }

  function render() {
    var qq = q.trim().toLowerCase();
    var items = filtered();
    countEl.textContent = items.length;
    emptyEl.hidden = items.length > 0;
    grid.innerHTML = items.map(topicHTML).join('');
    grid.querySelectorAll('.th-card').forEach(function (card) {
      card.querySelector('.th-head').addEventListener('click', function (e) {
        if (e.target.closest('a')) return;
        card.classList.toggle('open');
      });
      if (qq) card.classList.add('open');
    });
  }

  chipsWrap.querySelectorAll('.th-chip').forEach(function (c) {
    c.addEventListener('click', function () {
      chipsWrap.querySelectorAll('.th-chip').forEach(function (x) { x.classList.remove('on'); });
      c.classList.add('on'); cat = c.getAttribute('data-cat'); render();
    });
  });
  searchInp.addEventListener('input', function () { q = searchInp.value; render(); });

  render();
})();
