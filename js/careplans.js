/* Must Love Scrubs — Care Plans.
   Searchable, filterable library of nursing care plans in ADPIE format:
   nursing diagnosis, assessment data, outcomes, interventions with rationales,
   and evaluation. Demo (static content). */

(function () {
  'use strict';
  var root = document.querySelector('.careplans');
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

  var ALL = JSON.parse(root.querySelector('script[data-careplans]').textContent);
  var grid = root.querySelector('[data-cp-grid]');
  var chipsWrap = root.querySelector('[data-cp-chips]');
  var searchInp = root.querySelector('[data-cp-search]');
  var countEl = root.querySelector('[data-cp-count]');
  var emptyEl = root.querySelector('[data-cp-empty]');

  var cat = 'All', q = '';
  function esc(s) { return String(s == null ? '' : s); }
  function ul(arr) { return '<ul class="cp-list">' + (arr || []).map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ul>'; }

  function plansMatch(p, qq) {
    if (!qq) return true;
    if ((p.title + ' ' + p.category + ' ' + (p.summary || '')).toLowerCase().indexOf(qq) >= 0) return true;
    return (p.diagnoses || []).some(function (d) {
      return (d.dx + ' ' + d.related + ' ' + d.aeb).toLowerCase().indexOf(qq) >= 0;
    });
  }

  function filtered() {
    var qq = q.trim().toLowerCase();
    return ALL.filter(function (p) {
      if (cat !== 'All' && p.category !== cat) return false;
      return plansMatch(p, qq);
    });
  }

  function dxHTML(d) {
    var interventions = (d.interventions || []).map(function (x) {
      return '<div class="cp-int"><div class="cp-int-i">' + esc(x.i) + '</div><div class="cp-int-r"><b>Rationale:</b> ' + esc(x.r) + '</div></div>';
    }).join('');
    var subj = (d.subjective && d.subjective.length) ? '<div class="cp-sub"><b>Subjective</b>' + ul(d.subjective) + '</div>' : '';
    var obj = (d.objective && d.objective.length) ? '<div class="cp-sub"><b>Objective</b>' + ul(d.objective) + '</div>' : '';
    return '<div class="cp-dx">' +
      '<div class="cp-dx-name">' + esc(d.dx) + '</div>' +
      '<p class="cp-dx-rel">' + esc(d.related) + '<br><i>' + esc(d.aeb) + '</i></p>' +
      '<div class="cp-block"><span class="cp-lbl">Assessment</span><div class="cp-assess">' + subj + obj + '</div></div>' +
      '<div class="cp-block"><span class="cp-lbl">Expected outcomes</span>' + ul(d.outcomes) + '</div>' +
      '<div class="cp-block"><span class="cp-lbl">Interventions &amp; rationales</span>' + interventions + '</div>' +
      '<div class="cp-block"><span class="cp-lbl">Evaluation</span><p class="cp-eval">' + esc(d.evaluation) + '</p></div>' +
      '</div>';
  }

  function planHTML(p) {
    var dxs = p.diagnoses.map(dxHTML).join('');
    var dxCount = p.diagnoses.length;
    return '<div class="cp-card">' +
      '<button class="cp-head"><span class="cp-ic">' + svg(p.icon) + '</span>' +
      '<span class="cp-head-txt"><b>' + esc(p.title) + '</b><small>' + esc(p.summary) + '</small></span>' +
      '<span class="cp-dxn">' + dxCount + ' dx</span><span class="cp-cat-tag">' + esc(p.category) + '</span>' +
      '<span class="cp-caret">▾</span></button>' +
      '<div class="cp-body">' + dxs + '</div></div>';
  }

  function render() {
    var qq = q.trim().toLowerCase();
    var items = filtered();
    countEl.textContent = items.length;
    emptyEl.hidden = items.length > 0;
    grid.innerHTML = items.map(planHTML).join('');
    grid.querySelectorAll('.cp-card').forEach(function (card) {
      card.querySelector('.cp-head').addEventListener('click', function () { card.classList.toggle('open'); });
      if (qq) card.classList.add('open');
    });
  }

  chipsWrap.querySelectorAll('.cp-chip').forEach(function (c) {
    c.addEventListener('click', function () {
      chipsWrap.querySelectorAll('.cp-chip').forEach(function (x) { x.classList.remove('on'); });
      c.classList.add('on'); cat = c.getAttribute('data-cat'); render();
    });
  });
  searchInp.addEventListener('input', function () { q = searchInp.value; render(); });

  render();
})();
