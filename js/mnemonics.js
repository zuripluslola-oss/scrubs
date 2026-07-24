/* Must Love Scrubs — Mnemonics.
   Searchable, filterable library of nursing mnemonics. Each shows the acronym,
   what it's for, a letter-by-letter breakdown, an emoji visual cue (lightweight
   picmonic), and an explanation. Demo (static content). */

(function () {
  'use strict';
  var root = document.querySelector('.mnemonics');
  if (!root) return;

  var ALL = JSON.parse(root.querySelector('script[data-mnems]').textContent);
  var grid = root.querySelector('[data-mn-grid]');
  var chipsWrap = root.querySelector('[data-mn-chips]');
  var searchInp = root.querySelector('[data-mn-search]');
  var countEl = root.querySelector('[data-mn-count]');
  var emptyEl = root.querySelector('[data-mn-empty]');

  var cat = 'All', q = '';
  function esc(s) { return String(s == null ? '' : s); }

  function filtered() {
    var qq = q.trim().toLowerCase();
    return ALL.filter(function (m) {
      if (cat !== 'All' && m.category !== cat) return false;
      if (!qq) return true;
      var hay = m.title + ' ' + m.for + ' ' + m.category + ' ' + (m.explain || '') + ' ' +
        m.letters.map(function (x) { return x.l + ' ' + x.m; }).join(' ');
      return hay.toLowerCase().indexOf(qq) >= 0;
    });
  }

  function mnemHTML(m) {
    var rows = m.letters.map(function (x) {
      return '<div class="mn-row"><span class="mn-l">' + esc(x.l) + '</span><span class="mn-m">' + esc(x.m) + '</span></div>';
    }).join('');
    var visual = m.emoji ? '<div class="mn-visual" title="Visual cue">' + esc(m.emoji) + '</div>' : '';
    return '<div class="mn-card">' +
      '<div class="mn-head">' +
        '<div class="mn-head-txt"><b class="mn-title">' + esc(m.title) + '</b><small>' + esc(m.for) + '</small></div>' +
        '<span class="mn-cat-tag">' + esc(m.category) + '</span>' +
      '</div>' + visual +
      '<div class="mn-rows">' + rows + '</div>' +
      (m.explain ? '<p class="mn-explain">' + esc(m.explain) + '</p>' : '') +
      '</div>';
  }

  function render() {
    var items = filtered();
    countEl.textContent = items.length;
    emptyEl.hidden = items.length > 0;
    grid.innerHTML = items.map(mnemHTML).join('');
  }

  chipsWrap.querySelectorAll('.mn-chip').forEach(function (c) {
    c.addEventListener('click', function () {
      chipsWrap.querySelectorAll('.mn-chip').forEach(function (x) { x.classList.remove('on'); });
      c.classList.add('on'); cat = c.getAttribute('data-cat'); render();
    });
  });
  searchInp.addEventListener('input', function () { q = searchInp.value; render(); });

  render();
})();
