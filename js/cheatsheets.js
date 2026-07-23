/* Must Love Scrubs — Cheat Sheets.
   Searchable, filterable, printable clinical reference sheets. Each sheet is a
   set of sections of key/value/note rows. Demo (static content). */

(function () {
  'use strict';
  var root = document.querySelector('.cheats');
  if (!root) return;

  var ICON = {
    flask: 'M9 3h6M10 3v6l-5 8.5A2 2 0 0 0 6.7 21h10.6a2 2 0 0 0 1.7-3.5L14 9V3M7.5 15h9',
    lungs: 'M12 4v9M12 9c0 5-1.5 8-4.5 8C5 17 4 15 4 12c0-2 .5-4 2-5.5M12 9c0 5 1.5 8 4.5 8 2.5 0 3.5-2 3.5-5 0-2-.5-4-2-5.5',
    drop: 'M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z',
    heartbeat: 'M3 12h4l2-5 3 9 2-5h4',
    shield: 'M12 3l8 3v6c0 4.5-3.2 7.6-8 9-4.8-1.4-8-4.5-8-9V6z',
    sheet: 'M6 2h9l5 5v15H6zM14 2v6h6M9 13h7M9 17h7'
  };
  function svg(name) {
    var d = ICON[name] || ICON.sheet;
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
      d.split('M').filter(Boolean).map(function (p) { return '<path d="M' + p + '"/>'; }).join('') + '</svg>';
  }

  var ALL = JSON.parse(root.querySelector('script[data-cheats]').textContent);
  var grid = root.querySelector('[data-cs-grid]');
  var chipsWrap = root.querySelector('[data-cs-chips]');
  var searchInp = root.querySelector('[data-cs-search]');
  var countEl = root.querySelector('[data-cs-count]');
  var emptyEl = root.querySelector('[data-cs-empty]');

  var cat = 'All', q = '';
  function esc(s) { return String(s == null ? '' : s); }

  function matchesSearch(sheet, qq) {
    if (!qq) return true;
    if ((sheet.title + ' ' + sheet.category + ' ' + (sheet.summary || '')).toLowerCase().indexOf(qq) >= 0) return true;
    return sheet.sections.some(function (s) {
      if ((s.h || '').toLowerCase().indexOf(qq) >= 0) return true;
      return (s.rows || []).some(function (r) {
        return (r.k + ' ' + r.v + ' ' + (r.note || '')).toLowerCase().indexOf(qq) >= 0;
      });
    });
  }

  function filtered() {
    var qq = q.trim().toLowerCase();
    return ALL.filter(function (s) {
      if (cat !== 'All' && s.category !== cat) return false;
      return matchesSearch(s, qq);
    });
  }

  function sheetHTML(s, i) {
    var body = s.sections.map(function (sec) {
      var rows = (sec.rows || []).map(function (r) {
        return '<tr><td class="cs-k">' + esc(r.k) + '</td><td class="cs-v">' + esc(r.v) + '</td>' +
          '<td class="cs-note">' + esc(r.note) + '</td></tr>';
      }).join('');
      return '<div class="cs-sec"><h4>' + esc(sec.h) + '</h4><table class="cs-table"><tbody>' + rows + '</tbody></table></div>';
    }).join('');
    var pearl = s.pearl ? '<div class="cs-pearl"><b>💡 Remember.</b> ' + esc(s.pearl) + '</div>' : '';
    return '<div class="cs-card" data-i="' + i + '">' +
      '<button class="cs-head"><span class="cs-ic">' + svg(s.icon) + '</span>' +
      '<span class="cs-head-txt"><b>' + esc(s.title) + '</b><small>' + esc(s.summary) + '</small></span>' +
      '<span class="cs-cat-tag">' + esc(s.category) + '</span><span class="cs-caret">▾</span></button>' +
      '<div class="cs-body">' + body + pearl + '</div></div>';
  }

  function render() {
    var qq = q.trim().toLowerCase();
    var items = filtered();
    countEl.textContent = items.length;
    emptyEl.hidden = items.length > 0;
    grid.innerHTML = items.map(sheetHTML).join('');
    grid.querySelectorAll('.cs-card').forEach(function (card) {
      var head = card.querySelector('.cs-head');
      head.addEventListener('click', function () { card.classList.toggle('open'); });
      // auto-open when actively searching so matches are visible
      if (qq) card.classList.add('open');
    });
  }

  chipsWrap.querySelectorAll('.cs-chip').forEach(function (c) {
    c.addEventListener('click', function () {
      chipsWrap.querySelectorAll('.cs-chip').forEach(function (x) { x.classList.remove('on'); });
      c.classList.add('on'); cat = c.getAttribute('data-cat'); render();
    });
  });
  searchInp.addEventListener('input', function () { q = searchInp.value; render(); });

  render();
})();
