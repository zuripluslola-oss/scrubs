/* Must Love Scrubs — Lab Values reference.
   All high-yield NCLEX labs, grouped by panel. Each lab shows its normal
   range, what HIGH means, what LOW means, any critical value, and a note.
   Searchable and filterable. Demo (static content). */

(function () {
  'use strict';
  var root = document.querySelector('.labvalues');
  if (!root) return;

  var ALL = JSON.parse(root.querySelector('script[data-labs]').textContent);
  var listEl = root.querySelector('[data-lv-list]');
  var chipsWrap = root.querySelector('[data-lv-chips]');
  var searchInp = root.querySelector('[data-lv-search]');
  var countEl = root.querySelector('[data-lv-count]');
  var emptyEl = root.querySelector('[data-lv-empty]');

  var cat = 'All', q = '';
  function esc(s) { return String(s == null ? '' : s); }

  function filtered() {
    var qq = q.trim().toLowerCase();
    return ALL.filter(function (x) {
      if (cat !== 'All' && x.category !== cat) return false;
      if (!qq) return true;
      return (x.name + ' ' + (x.abbr || '') + ' ' + x.category + ' ' + x.range + ' ' +
        (x.high || '') + ' ' + (x.low || '') + ' ' + (x.note || '')).toLowerCase().indexOf(qq) >= 0;
    });
  }

  function labHTML(x) {
    var crit = x.critical ? '<span class="lv-crit">critical ' + esc(x.critical) + '</span>' : '';
    var high = x.high && x.high !== '—' ? '<div class="lv-dir up"><span>▲ High</span><p>' + esc(x.high) + '</p></div>' : '';
    var low = x.low && x.low !== '—' ? '<div class="lv-dir down"><span>▼ Low</span><p>' + esc(x.low) + '</p></div>' : '';
    var note = x.note ? '<p class="lv-note">' + esc(x.note) + '</p>' : '';
    return '<div class="lv-lab">' +
      '<div class="lv-lab-top">' +
        '<b class="lv-name">' + esc(x.name) + (x.abbr ? ' <span class="lv-abbr">' + esc(x.abbr) + '</span>' : '') + '</b>' +
        '<span class="lv-range">' + esc(x.range) + '</span>' + crit +
      '</div>' +
      '<div class="lv-dirs">' + high + low + '</div>' + note +
      '</div>';
  }

  function render() {
    var items = filtered();
    countEl.textContent = items.length;
    emptyEl.hidden = items.length > 0;
    // group by category, preserving first-seen order
    var order = [], groups = {};
    items.forEach(function (x) {
      if (!groups[x.category]) { groups[x.category] = []; order.push(x.category); }
      groups[x.category].push(x);
    });
    listEl.innerHTML = order.map(function (c) {
      return '<div class="lv-panel"><h3 class="lv-panel-h">' + esc(c) +
        ' <small>' + groups[c].length + '</small></h3>' +
        groups[c].map(labHTML).join('') + '</div>';
    }).join('');
  }

  chipsWrap.querySelectorAll('.lv-chip').forEach(function (c) {
    c.addEventListener('click', function () {
      chipsWrap.querySelectorAll('.lv-chip').forEach(function (x) { x.classList.remove('on'); });
      c.classList.add('on'); cat = c.getAttribute('data-cat'); render();
    });
  });
  searchInp.addEventListener('input', function () { q = searchInp.value; render(); });

  render();
})();
