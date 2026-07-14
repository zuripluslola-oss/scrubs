/* Must Love Scrubs — specialty track pages (UI shell)
   Waitlist "notify me" demo until backend. */

(function () {
  'use strict';
  document.querySelectorAll('[data-soon]').forEach(function (form) {
    var done = form.parentElement.querySelector('[data-soon-done]');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var input = form.querySelector('input[type="email"]');
      if (input && !input.value) { input.focus(); return; }
      form.hidden = true;
      if (done) done.hidden = false;
    });
  });
})();
