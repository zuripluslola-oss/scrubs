/* Must Love Scrubs — Drug Cards.
   A searchable, filterable library of structured medication cards, plus a
   Drill mode that flips each drug into a recall card (name → class + key
   nursing point) so you study them, not just read them. Demo. */

(function () {
  'use strict';
  var root = document.querySelector('.drugcards');
  if (!root) return;

  var ALL = JSON.parse(root.querySelector('script[data-drugs]').textContent);
  var grid = root.querySelector('[data-dc-grid]');
  var drill = root.querySelector('[data-dc-drill]');
  var chipsWrap = root.querySelector('[data-dc-chips]');
  var searchInp = root.querySelector('[data-dc-search]');
  var countEl = root.querySelector('[data-dc-count]');
  var emptyEl = root.querySelector('[data-dc-empty]');

  var sys = 'All', q = '', mode = 'browse';

  function esc(s) { return String(s == null ? '' : s); }
  function list(arr) { return '<ul>' + (arr || []).map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ul>'; }

  function filtered() {
    var qq = q.trim().toLowerCase();
    return ALL.filter(function (x) {
      if (sys !== 'All' && x.system !== sys) return false;
      if (!qq) return true;
      return (x.generic + ' ' + x.brand + ' ' + x.class + ' ' + x.system + ' ' + (x.uses || []).join(' ')).toLowerCase().indexOf(qq) >= 0;
    });
  }

  /* ---------- browse: structured cards ---------- */
  function cardHTML(x, i) {
    var badges =
      (x.prototype ? '<span class="dc-badge proto">Prototype</span>' : '') +
      (x.highalert ? '<span class="dc-badge alert">High-alert</span>' : '');
    var head =
      '<button class="dc-head" data-i="' + i + '">' +
        '<div class="dc-head-main"><b class="dc-generic">' + esc(x.generic) + '</b>' +
        (x.brand ? '<span class="dc-brand">' + esc(x.brand) + '</span>' : '') + '</div>' +
        '<span class="dc-class">' + esc(x.class) + '</span>' + badges +
        '<span class="dc-caret">▾</span>' +
      '</button>';
    var body =
      '<div class="dc-body">' +
        row('How it works', '<p>' + esc(x.moa) + '</p>') +
        row('Uses', list(x.uses)) +
        row('Dose &amp; route', '<p>' + esc(x.dose) + ' &middot; <i>' + esc(x.route) + '</i></p>') +
        row('Side effects', list(x.side)) +
        row('Serious / adverse', list(x.adverse), 'adverse') +
        row('Nursing considerations', list(x.nursing), 'nursing') +
        row('Monitor', list(x.labs)) +
        row('Contraindications', list(x.contra)) +
        row('Patient teaching', list(x.teaching)) +
        row('Antidote', '<p>' + esc(x.antidote) + '</p>', x.antidote && x.antidote !== 'None' ? 'antidote' : '') +
        (x.tip ? '<div class="dc-tip"><b>📝 NCLEX tip.</b> ' + esc(x.tip) + '</div>' : '') +
        (x.pearl ? '<div class="dc-tip pearl"><b>💡 Memory trick.</b> ' + md(x.pearl) + '</div>' : '') +
      '</div>';
    return '<div class="dc-card' + (x.highalert ? ' is-alert' : '') + '">' + head + body + '</div>';
  }
  function row(label, inner, cls) { return '<div class="dc-row ' + (cls || '') + '"><span class="dc-lbl">' + label + '</span><div class="dc-val">' + inner + '</div></div>'; }
  function md(s) { return String(s == null ? '' : s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>'); }

  function renderBrowse() {
    drill.hidden = true; grid.hidden = false;
    var items = filtered();
    countEl.textContent = items.length;
    emptyEl.hidden = items.length > 0;
    grid.innerHTML = items.map(cardHTML).join('');
    grid.querySelectorAll('.dc-head').forEach(function (h) {
      h.addEventListener('click', function () { h.parentNode.classList.toggle('open'); });
    });
  }

  /* ---------- drill: recall cards ---------- */
  var order = [], di = 0, seen, right;
  function startDrill() {
    grid.hidden = true; drill.hidden = false;
    order = shuffle(filtered()); di = 0; seen = 0; right = 0;
    if (!order.length) { drill.innerHTML = '<div class="fc-done"><h3>No cards in this filter</h3><p>Pick another system or clear your search.</p></div>'; return; }
    renderDrill();
  }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }

  function renderDrill() {
    if (di >= order.length) {
      drill.innerHTML = '<div class="fc-done"><h3>Deck complete 🎉</h3><p>You reviewed <b>' + order.length + '</b> drug cards. ' +
        'Rated yourself solid on <b>' + right + '</b>.</p>' +
        '<button class="btn btn-coral" data-dc-restart>Drill again</button></div>';
      drill.querySelector('[data-dc-restart]').addEventListener('click', startDrill);
      return;
    }
    var x = order[di];
    drill.innerHTML =
      '<div class="dc-drill-meta"><span>Card ' + (di + 1) + ' / ' + order.length + '</span><span>' + esc(x.system) + '</span></div>' +
      '<div class="dc-flip" data-dc-flip>' +
        '<div class="dc-flip-inner">' +
          '<div class="dc-flip-face dc-front">' +
            '<span class="dc-flip-hint">What class? What\'s the #1 nursing point?</span>' +
            '<b class="dc-flip-name">' + esc(x.generic) + '</b>' +
            (x.brand ? '<span class="dc-brand">' + esc(x.brand) + '</span>' : '') +
            '<span class="dc-flip-tap">Tap to reveal</span>' +
          '</div>' +
          '<div class="dc-flip-face dc-back">' +
            '<span class="dc-class">' + esc(x.class) + '</span>' +
            '<p class="dc-flip-moa">' + esc(x.moa) + '</p>' +
            '<div class="dc-flip-key"><b>Key nursing point</b><p>' + esc((x.nursing && x.nursing[0]) || x.tip || '') + '</p></div>' +
            (x.antidote && x.antidote !== 'None' ? '<div class="dc-flip-anti"><b>Antidote:</b> ' + esc(x.antidote) + '</div>' : '') +
          '</div>' +
        '</div>' +
      '</div>' +
      '<div class="dc-drill-actions" data-dc-rate hidden>' +
        '<button class="btn btn-line" data-dc-again>Still learning</button>' +
        '<button class="btn btn-coral" data-dc-got>Got it &rarr;</button>' +
      '</div>';
    var flip = drill.querySelector('[data-dc-flip]');
    var rate = drill.querySelector('[data-dc-rate]');
    flip.addEventListener('click', function () { flip.classList.add('flipped'); rate.hidden = false; });
    drill.querySelector('[data-dc-got]').addEventListener('click', function () { right++; seen++; di++; renderDrill(); });
    drill.querySelector('[data-dc-again]').addEventListener('click', function () { seen++; order.push(x); di++; renderDrill(); });
  }

  function render() { if (mode === 'drill') startDrill(); else renderBrowse(); }

  /* ---------- wire controls ---------- */
  chipsWrap.querySelectorAll('.dc-chip').forEach(function (c) {
    c.addEventListener('click', function () {
      chipsWrap.querySelectorAll('.dc-chip').forEach(function (x) { x.classList.remove('on'); });
      c.classList.add('on'); sys = c.getAttribute('data-sys'); render();
    });
  });
  root.querySelectorAll('.dc-mode').forEach(function (m) {
    m.addEventListener('click', function () {
      root.querySelectorAll('.dc-mode').forEach(function (x) { x.classList.remove('on'); });
      m.classList.add('on'); mode = m.getAttribute('data-dc-mode'); render();
    });
  });
  searchInp.addEventListener('input', function () { q = searchInp.value; render(); });

  renderBrowse();
})();
