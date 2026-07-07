/* Must Love Scrubs — shared page behavior
   Parallax, fade-up reveals, mobile nav, and the Ask Esi widget. */

(function () {
  'use strict';

  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Mobile nav ---------- */

  var navToggle = document.querySelector('.nav-toggle');
  var mobileNav = document.querySelector('.mobile-nav');
  if (navToggle && mobileNav) {
    navToggle.addEventListener('click', function () {
      var open = mobileNav.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', open);
    });
    mobileNav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        mobileNav.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---------- Parallax layers ---------- */

  var layers = document.querySelectorAll('[data-parallax]');
  if (layers.length && !reducedMotion) {
    var ticking = false;
    var update = function () {
      ticking = false;
      layers.forEach(function (layer) {
        var speed = parseFloat(layer.getAttribute('data-parallax')) || 0.3;
        var box = layer.parentElement.getBoundingClientRect();
        // only move layers whose section is on screen
        if (box.bottom < 0 || box.top > window.innerHeight) return;
        layer.style.transform = 'translateY(' + (-box.top * speed) + 'px)';
      });
    };
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }

  /* ---------- Fade-up on scroll ---------- */

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('.fade-up').forEach(function (el) { observer.observe(el); });

  /* ---------- Ask Esi widget ---------- */

  var fab = document.querySelector('.esi-fab');
  var panel = document.querySelector('.esi-panel');
  if (!fab || !panel) return;

  var log = panel.querySelector('.esi-log');
  var input = panel.querySelector('.esi-input input');
  var send = panel.querySelector('.esi-send');
  var close = panel.querySelector('.esi-close');

  function openEsi() {
    document.body.classList.add('esi-open');
    setTimeout(function () { input.focus(); }, 400);
  }
  function closeEsi() { document.body.classList.remove('esi-open'); }

  fab.addEventListener('click', openEsi);
  close.addEventListener('click', closeEsi);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeEsi();
  });

  function addMsg(text, who) {
    var el = document.createElement('div');
    el.className = 'msg ' + who;
    el.textContent = text;
    log.appendChild(el);
    log.scrollTop = log.scrollHeight;
  }

  // Placeholder brain until the Claude-powered backend is wired up.
  function esiReply(question) {
    var q = question.toLowerCase();
    if (/(911|emergency|chest pain|can't breathe|cant breathe|overdose|suicide)/.test(q)) {
      return "If this is an emergency, please call 911 right now — that comes first, always. " +
        "Once you're safe, I'm here for any follow-up questions. ❤";
    }
    return "Hi, I'm Esi — your nurse in your pocket. I'm still in training (my full " +
      "Claude-powered brain is coming soon), but soon I'll answer any medical question, " +
      "help you study, find you jobs, and even shop for you. Remember: I never diagnose " +
      "or prescribe, and emergencies always start with 911.";
  }

  function submit() {
    var text = input.value.trim();
    if (!text) return;
    addMsg(text, 'user');
    input.value = '';
    setTimeout(function () { addMsg(esiReply(text), 'esi'); }, 600);
  }

  send.addEventListener('click', submit);
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') submit();
  });
})();
