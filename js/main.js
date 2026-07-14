/* Must Love Scrubs — shared behavior (V2)
   Mega menu, Esi widget routing, parallax, reveals, count-up stats,
   FAQ accordion, daily points (demo via localStorage until backend). */

(function () {
  'use strict';

  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Mega menu ---------- */

  var menuBtn = document.querySelector('.menu-btn');
  var mega = document.querySelector('.mega');
  if (menuBtn && mega) {
    menuBtn.addEventListener('click', function () {
      var open = mega.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open);
    });
    document.addEventListener('click', function (e) {
      if (mega.classList.contains('open') && !mega.contains(e.target) && !menuBtn.contains(e.target)) {
        mega.classList.remove('open');
        menuBtn.setAttribute('aria-expanded', 'false');
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') mega.classList.remove('open');
    });
  }

  /* ---------- Esi widget: two-destination routing ----------
     Not subscribed -> esi.html (subscribe page)
     Subscribed     -> profile.html (dashboard with Esi)        */

  document.querySelectorAll('[data-esi-launch]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      e.preventDefault();
      var subscribed = localStorage.getItem('esiSubscribed') === 'true';
      window.location.href = subscribed ? 'profile.html' : 'esi.html';
    });
  });

  /* ---------- Parallax layers ---------- */

  var layers = document.querySelectorAll('[data-parallax]');
  if (layers.length && !reducedMotion) {
    var ticking = false;
    var update = function () {
      ticking = false;
      layers.forEach(function (layer) {
        var speed = parseFloat(layer.getAttribute('data-parallax')) || 0.25;
        var box = layer.parentElement.getBoundingClientRect();
        if (box.bottom < 0 || box.top > window.innerHeight) return;
        layer.style.transform = 'translateY(' + (-box.top * speed) + 'px)';
      });
    };
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }

  /* ---------- Fade-up reveals ---------- */

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('.fade-up').forEach(function (el) { io.observe(el); });

  /* ---------- Count-up stats ---------- */

  function countUp(el) {
    var target = parseInt(el.getAttribute('data-count'), 10);
    if (reducedMotion) { el.textContent = target.toLocaleString(); return; }
    var start = null, dur = 1600;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased).toLocaleString();
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var statIo = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        countUp(entry.target);
        statIo.unobserve(entry.target);
      }
    });
  }, { threshold: 0.6 });
  document.querySelectorAll('[data-count]').forEach(function (el) { statIo.observe(el); });

  /* ---------- FAQ accordion ---------- */

  document.querySelectorAll('.faq-item').forEach(function (item) {
    var q = item.querySelector('.faq-q');
    var a = item.querySelector('.faq-a');
    if (!q || !a) return;
    q.addEventListener('click', function () {
      var isOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(function (other) {
        other.classList.remove('open');
        other.querySelector('.faq-a').style.maxHeight = null;
      });
      if (!isOpen) {
        item.classList.add('open');
        a.style.maxHeight = a.scrollHeight + 'px';
      }
    });
  });

  /* ---------- Daily points (demo until backend) ---------- */

  var pointsEls = document.querySelectorAll('[data-points-balance]');
  function getPoints() { return parseInt(localStorage.getItem('mlsPoints') || '0', 10); }
  function renderPoints() {
    pointsEls.forEach(function (el) { el.textContent = getPoints().toLocaleString(); });
  }
  renderPoints();

  var claimBtn = document.querySelector('[data-claim-daily]');
  if (claimBtn) {
    var today = new Date().toDateString();
    var claimed = localStorage.getItem('mlsClaimedOn') === today;
    function setClaimed() {
      claimBtn.textContent = '✓ Claimed today — come back tomorrow';
      claimBtn.disabled = true;
      claimBtn.style.opacity = '0.65';
    }
    if (claimed) setClaimed();
    claimBtn.addEventListener('click', function () {
      if (localStorage.getItem('mlsClaimedOn') === new Date().toDateString()) return;
      localStorage.setItem('mlsPoints', String(getPoints() + 10));
      localStorage.setItem('mlsClaimedOn', new Date().toDateString());
      renderPoints();
      setClaimed();
    });
  }

  /* ---------- Dictionary ownership + auto-free updates (demo) ----------
     Ownership is a profile flag, not a file sale. The download always serves
     the LATEST release; owners get every future expansion free, flagged NEW.
     Real version reads this from the account/DB in Phase 2. */
  (function () {
    var LATEST = { ver: 'Core Release 3', num: 3, note: '40 new terms across your specialties — added to your library free.' };
    var wrap = document.querySelector('[data-downloads]');
    if (!wrap) return;
    function render() {
      var owned = localStorage.getItem('dictOwned') === 'true';
      var seen = parseInt(localStorage.getItem('dictSeen') || '0', 10);
      var isNew = owned && seen < LATEST.num;
      wrap.querySelector('[data-dl-owned]').hidden = !owned;
      wrap.querySelector('[data-dl-unowned]').hidden = owned;
      wrap.querySelector('[data-dl-badge]').hidden = !isNew;
      wrap.querySelector('[data-dl-ver]').textContent = LATEST.ver;
      var note = wrap.querySelector('[data-dl-note]');
      note.textContent = isNew ? ('🆕 ' + LATEST.ver + ' — ' + LATEST.note) : ('You have the latest — ' + LATEST.ver + '.');
    }
    var demo = wrap.querySelector('[data-dl-demo]');
    if (demo) demo.addEventListener('click', function () {
      localStorage.setItem('dictOwned', 'true'); localStorage.setItem('dictSeen', '2'); render();
    });
    var get = wrap.querySelector('[data-dl-get]');
    if (get) get.addEventListener('click', function () { localStorage.setItem('dictSeen', String(LATEST.num)); setTimeout(render, 60); });
    render();
  })();

  /* demo subscribe toggle on the Esi page */
  var subBtn = document.querySelector('[data-esi-subscribe]');
  if (subBtn) {
    subBtn.addEventListener('click', function (e) {
      e.preventDefault();
      localStorage.setItem('esiSubscribed', 'true');
      window.location.href = 'profile.html';
    });
  }
})();
