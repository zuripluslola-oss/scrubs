/* Must Love Scrubs — Nurses Index: live search + category filter. */
(function () {
  'use strict';
  var input = document.querySelector('.dict-search input');
  var chips = Array.prototype.slice.call(document.querySelectorAll('.chip-filter'));
  var cards = Array.prototype.slice.call(document.querySelectorAll('.term-card'));
  var countEl = document.querySelector('.dict-count');
  var empty = document.querySelector('.dict-empty');
  if (!cards.length) return;
  var q = '', cat = 'all';

  function apply() {
    var shown = 0;
    cards.forEach(function (c) {
      var matchCat = cat === 'all' || c.getAttribute('data-cat') === cat;
      var hay = c.getAttribute('data-search');
      var matchQ = !q || hay.indexOf(q) !== -1;
      var show = matchCat && matchQ;
      c.style.display = show ? '' : 'none';
      if (show) shown++;
    });
    if (countEl) countEl.textContent = shown + (shown === 1 ? ' term' : ' terms');
    if (empty) empty.classList.toggle('show', shown === 0);
  }
  if (input) input.addEventListener('input', function () { q = input.value.trim().toLowerCase(); apply(); });
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      chips.forEach(function (c) { c.classList.remove('on'); });
      chip.classList.add('on');
      cat = chip.getAttribute('data-cat');
      apply();
    });
  });
  apply();
})();
