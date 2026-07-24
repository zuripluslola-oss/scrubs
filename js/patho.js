/* Must Love Scrubs — Patho (pathophysiology).
   Searchable, filterable disease library. Each condition expands into a chain:
   definition, causes, the pathophysiology mechanism (flow), signs WITH why,
   diagnostics, complications, and treatment — linked to its care plan. Demo. */

(function () {
  'use strict';
  var root = document.querySelector('.patho');
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

  var ALL = JSON.parse(root.querySelector('script[data-patho]').textContent);
  var grid = root.querySelector('[data-pt-grid]');
  var chipsWrap = root.querySelector('[data-pt-chips]');
  var searchInp = root.querySelector('[data-pt-search]');
  var countEl = root.querySelector('[data-pt-count]');
  var emptyEl = root.querySelector('[data-pt-empty]');

  var cat = 'All', q = '';
  function esc(s) { return String(s == null ? '' : s); }
  function ul(arr) { return '<ul class="pt-list">' + (arr || []).map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ul>'; }

  function match(c, qq) {
    if (!qq) return true;
    var hay = c.title + ' ' + c.category + ' ' + c.definition + ' ' + (c.causes || []).join(' ') + ' ' +
      (c.patho || []).join(' ') + ' ' + (c.signs || []).map(function (s) { return s.s; }).join(' ');
    return hay.toLowerCase().indexOf(qq) >= 0;
  }
  function filtered() {
    var qq = q.trim().toLowerCase();
    return ALL.filter(function (c) {
      if (cat !== 'All' && c.category !== cat) return false;
      return match(c, qq);
    });
  }

  function condHTML(c) {
    var flow = (c.patho || []).map(function (step, i) {
      return '<div class="pt-step"><span class="pt-step-n">' + (i + 1) + '</span><p>' + esc(step) + '</p></div>';
    }).join('<div class="pt-arrow">↓</div>');
    var signs = (c.signs || []).map(function (s) {
      return '<div class="pt-sign"><b>' + esc(s.s) + '</b><span>' + esc(s.why) + '</span></div>';
    }).join('');
    var carelink = c.carelink ? '<a class="btn btn-line pt-cplink" href="care-plans.html">See the care plan &rarr;</a>' : '';
    return '<div class="pt-card">' +
      '<button class="pt-head"><span class="pt-ic">' + svg(c.icon) + '</span>' +
      '<span class="pt-head-txt"><b>' + esc(c.title) + '</b><small>' + esc(c.definition) + '</small></span>' +
      '<span class="pt-cat-tag">' + esc(c.category) + '</span><span class="pt-caret">▾</span></button>' +
      '<div class="pt-body">' +
        '<div class="pt-block"><span class="pt-lbl">Causes / risk factors</span>' + ul(c.causes) + '</div>' +
        '<div class="pt-block"><span class="pt-lbl">How it happens (pathophysiology)</span><div class="pt-flow">' + flow + '</div></div>' +
        '<div class="pt-block"><span class="pt-lbl">Signs &amp; symptoms — and why</span><div class="pt-signs">' + signs + '</div></div>' +
        '<div class="pt-block"><span class="pt-lbl">Diagnostics</span>' + ul(c.diagnostics) + '</div>' +
        '<div class="pt-block"><span class="pt-lbl">Complications</span>' + ul(c.complications) + '</div>' +
        '<div class="pt-block"><span class="pt-lbl">Treatment</span>' + ul(c.treatment) + '</div>' +
        carelink +
      '</div></div>';
  }

  function render() {
    var qq = q.trim().toLowerCase();
    var items = filtered();
    countEl.textContent = items.length;
    emptyEl.hidden = items.length > 0;
    grid.innerHTML = items.map(condHTML).join('');
    grid.querySelectorAll('.pt-card').forEach(function (card) {
      card.querySelector('.pt-head').addEventListener('click', function (e) {
        if (e.target.closest('.pt-cplink')) return;
        card.classList.toggle('open');
      });
      if (qq) card.classList.add('open');
    });
  }

  chipsWrap.querySelectorAll('.pt-chip').forEach(function (c) {
    c.addEventListener('click', function () {
      chipsWrap.querySelectorAll('.pt-chip').forEach(function (x) { x.classList.remove('on'); });
      c.classList.add('on'); cat = c.getAttribute('data-cat'); render();
    });
  });
  searchInp.addEventListener('input', function () { q = searchInp.value; render(); });

  render();
})();
