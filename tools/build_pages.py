#!/usr/bin/env python3
"""Must Love Scrubs — static page generator.
Defines the shared chrome (tickers, header, mega menu, footer, bottom nav,
Esi widget) once and stamps out every page so they never drift apart.
Run from repo root:  python3 tools/build_pages.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- SVG icons
I = {
    "home":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11.5 12 4l9 7.5"/><path d="M5 10v10h5v-6h4v6h5V10"/></svg>',
    "book":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5a2 2 0 0 1 2-2h13v18H6a2 2 0 0 0-2 2z"/><path d="M4 19a2 2 0 0 1 2-2h13"/><path d="M11 7h4M13 5v4"/></svg>',
    "play":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="4"/><path d="M10 9.5v5l4.5-2.5z" fill="currentColor" stroke="none"/></svg>',
    "bag":    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 8h14l-1.2 12H6.2z"/><path d="M9 11V6a3 3 0 0 1 6 0v5"/></svg>',
    "user":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-3.5 4.5-5 8-5s6.5 1.5 8 5"/></svg>',
    "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    "bell":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9a6 6 0 0 1 12 0c0 5 2 6 2 6H4s2-1 2-6"/><path d="M10 20a2 2 0 0 0 4 0"/></svg>',
    "burger": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h10"/></svg>',
    "check":  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="m4 12.5 5 5L20 6.5"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 3v6c0 4.5-3.2 7.6-8 9-4.8-1.4-8-4.5-8-9V6z"/><path d="m8.8 12 2.2 2.2 4.2-4.4"/></svg>',
    "lock":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="5" y="10" width="14" height="10" rx="3"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>',
    "card":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="6" width="18" height="13" rx="3"/><path d="M3 10h18"/></svg>',
    "star":   '<svg viewBox="0 0 24 24" fill="currentColor"><path d="m12 3 2.7 5.7 6.3.8-4.6 4.3 1.2 6.2L12 17l-5.6 3 1.2-6.2L3 9.5l6.3-.8z"/></svg>',
    "fb":     '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 8.5V7a1.5 1.5 0 0 1 1.5-1.5H17V2h-3a4 4 0 0 0-4 4v2.5H7.5V12H10v10h4V12h2.6l.9-3.5z"/></svg>',
    "tiktok": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M16.5 3c.4 2.1 1.7 3.6 3.9 3.9v3.2c-1.5.1-2.8-.3-3.9-1.1v5.8a6.1 6.1 0 1 1-6.1-6.1c.3 0 .7 0 1 .1v3.3a2.9 2.9 0 1 0 2 2.7V3z"/></svg>',
    # scrub tv categories
    "er":     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 5 13h5l-1 9 8-11h-5z"/></svg>',
    "prenatal":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20s-7-4.3-7-9.5A4.2 4.2 0 0 1 12 7a4.2 4.2 0 0 1 7 3.5C19 15.7 12 20 12 20z"/><circle cx="12" cy="12" r="2"/></svg>',
    "peds":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="9" r="5.5"/><circle cx="7.5" cy="4.5" r="1.8"/><circle cx="16.5" cy="4.5" r="1.8"/><path d="M9.5 15.5 8 21m6.5-5.5L16 21"/><circle cx="10" cy="8.4" r=".6" fill="currentColor"/><circle cx="14" cy="8.4" r=".6" fill="currentColor"/></svg>',
    "icu":    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="13" rx="3"/><path d="M6 10.5h3l1.5-3 2.5 5 1.5-2h3.5"/><path d="M9 21h6"/></svg>',
    "medsurg":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="4" width="14" height="17" rx="3"/><path d="M9 4.5V3h6v1.5"/><path d="M12 9v6M9 12h6"/></svg>',
    "pharm":  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3.5" y="9" width="17" height="7" rx="3.5" transform="rotate(-35 12 12.5)"/><path d="m9 8.5 6 7"/></svg>',
    "mental": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21v-3.2A7 7 0 1 1 19 11l1.5 3H18v3a2 2 0 0 1-2 2h-2v2"/><path d="M11 8.5a2.5 2.5 0 0 1 5 0c0 1.8-2.5 2-2.5 3.5"/><circle cx="13.5" cy="14.6" r=".5" fill="currentColor"/></svg>',
    "geri":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7.5-4.6-7.5-10A4.5 4.5 0 0 1 12 7.5 4.5 4.5 0 0 1 19.5 11c0 5.4-7.5 10-7.5 10z"/><path d="M7 12h3l1.5-2.5L14 13l1.5-1.5H19"/></svg>',
    "dict":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4a1 1 0 0 1 1-1h12v18H6a1 1 0 0 1-1-1z"/><path d="M8 3v18M11 8h5M11 11h5"/></svg>',
    "bolt":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 5 13h5l-1 9 8-11h-5z"/></svg>',
    "list":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 6h12M8 12h12M8 18h12"/><circle cx="4" cy="6" r="1" fill="currentColor"/><circle cx="4" cy="12" r="1" fill="currentColor"/><circle cx="4" cy="18" r="1" fill="currentColor"/></svg>',
    "target": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1" fill="currentColor"/></svg>',
    "heart":  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20s-7-4.3-7-9.5A4.2 4.2 0 0 1 12 7a4.2 4.2 0 0 1 7 3.5C19 15.7 12 20 12 20z"/></svg>',
    "chat":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8 8 0 0 1-11.5 7.2L4 20l0.9-4.4A8 8 0 1 1 21 12z"/><path d="M9 11h6M9 14h4"/></svg>',
    "flask":  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6M10 3v6l-5 8.5A2 2 0 0 0 6.7 21h10.6a2 2 0 0 0 1.7-3.5L14 9V3"/><path d="M7.5 15h9"/></svg>',
    "lungs":  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v9"/><path d="M12 9c0 5-1.5 8-4.5 8C5 17 4 15 4 12c0-2 .5-4 2-5.5"/><path d="M12 9c0 5 1.5 8 4.5 8 2.5 0 3.5-2 3.5-5 0-2-.5-4-2-5.5"/></svg>',
    "drop":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/></svg>',
    "heartbeat":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h4l2-5 3 9 2-5h4"/></svg>',
    "sheet":  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2h9l5 5v15H6z"/><path d="M14 2v6h6M9 13h7M9 17h7"/></svg>',
}

def photo(name, grad, style=""):
    """Photo frame: real image (embedded at bundle time) layered over a gradient
    fallback so it looks intentional until the file is added to /images."""
    return (f'<div class="photo" style="background-image:url(images/{name}),{grad};'
            f'{style}"></div>')

TICKER_ESI = "".join(
    '<span>&#10022; Meet <em>Esi</em> — the AI tutor that revolutionizes how nurses learn</span>'
    '<span>&#10022; Esi guides you through the site &amp; tutors you 1-on-1</span>'
    '<span>&#10022; Add <em>Esi</em> to any prep course — study smarter, remember longer</span>'
    for _ in range(2))

TICKER_COURSES = "".join(
    '<span>&#9733; <em>NCLEX Complete</em> — our flagship prep course is live</span>'
    '<span>&#9733; 4 fresh free Scrub TV lessons every month — watch, quiz, earn points</span>'
    '<span>&#9733; Pharmacology &middot; Med-Surg &middot; Peds &middot; Mental Health &amp; more</span>'
    for _ in range(2))

def chrome(fname, title, desc, body, active=""):
    def cur(name):
        return ' aria-current="page"' if name == active else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="stylesheet" href="css/styles.css">
</head>
<body>

  <div class="tickers" aria-hidden="true">
    <div class="ticker ticker-esi"><div class="ticker-track">{TICKER_ESI}</div></div>
    <div class="ticker ticker-courses"><div class="ticker-track">{TICKER_COURSES}</div></div>
  </div>

  <header class="site-header">
    <div class="wrap">
      <a class="logo" href="index.html" aria-label="Must Love Scrubs home">
        <span class="mark">M<b>&#10084;</b>S</span>
        <span class="word">Must <i>Love</i> Scrubs</span>
      </a>
      <nav class="main-nav" aria-label="Main">
        <a href="index.html"{cur('home')}>Home</a>
        <a href="courses.html"{cur('courses')}>Courses</a>
        <a href="scrubtv.html"{cur('scrubtv')}>Scrub TV</a>
        <a href="esi.html"{cur('esi')}>Esi</a>
        <a href="store.html"{cur('store')}>Store</a>
      </nav>
      <div class="header-actions">
        <a class="icon-btn" href="search.html" aria-label="Search">{I['search']}</a>
        <a class="icon-btn" href="notifications.html" aria-label="Notifications"><span class="badge"></span>{I['bell']}</a>
        <a class="icon-btn" href="profile.html" aria-label="Profile">{I['user']}</a>
        <button class="menu-btn" aria-expanded="false" aria-label="Menu">{I['burger']} Menu</button>
      </div>
    </div>
  </header>

  <nav class="mega" aria-label="Site menu">
    <div class="wrap mega-grid">
      <div>
        <h4>Learn</h4>
        <ul class="mega-links">
          <li><a href="nclex-complete.html">NCLEX Complete <small>The flagship &middot; plans from $59</small></a></li>
          <li><a href="nclex.html">Free NCLEX Prep <small>RN &amp; LPN &middot; every NGN item type</small></a></li>
          <li><a href="qbank.html">Question Bank <small>Practice with rationales &amp; answer stats</small></a></li>
          <li><a href="tests.html">Tests &amp; Exams <small>Pop quiz, mock NCLEX &amp; specialty exams</small></a></li>
          <li><a href="flashcards.html">Flashcards &amp; Games <small>Flip cards, quizzes, match &amp; speed rounds</small></a></li>
          <li><a href="drugs.html">Drug Cards <small>Pharmacology library &middot; drill by system</small></a></li>
          <li><a href="cheatsheets.html">Cheat Sheets <small>ABGs, antidotes, diets &amp; more</small></a></li>
          <li><a href="lab-values.html">Lab Values <small>All 65 &middot; what high &amp; low mean</small></a></li>
          <li><a href="mnemonics.html">Mnemonics <small>MONA, VEAL CHOP, SLUDGE &amp; more</small></a></li>
          <li><a href="patho.html">Patho <small>Disease mechanisms made visual</small></a></li>
          <li><a href="care-plans.html">Care Plans <small>Diagnoses, interventions &amp; rationales</small></a></li>
          <li><a href="study-plan.html">Study Plan Calendar <small>Your day-by-day plan to test day</small></a></li>
          <li><a href="nclex-guide.html">Free Study Guide <small>How to pass &middot; for nurses, by nurses</small></a></li>
          <li><a href="course-lab-values.html">Free NCLEX Practice <small>Start with a free audio scene</small></a></li>
          <li><a href="specialties.html">Specialty Prep <small>22 specialty tracks &middot; rolling out</small></a></li>
          <li><a href="courses.html">Courses <small>NCLEX prep, entrance exams &amp; more</small></a></li>
          <li><a href="scrubtv.html">Scrub TV <small>4 free lessons a month, quizzes &amp; more</small></a></li>
          <li><a href="esi.html">Esi <small>Your AI tutor &amp; site guide</small></a></li>
        </ul>
      </div>
      <div>
        <h4>Community</h4>
        <ul class="mega-links">
          <li><a href="dictionary.html">Nurses Index <small>Every term, in plain language</small></a></li>
          <li><a href="spotlight.html">Nurse Spotlight <small>Real stories, beautifully told</small></a></li>
          <li><a href="jobs.html">Job Search <small>A small Indeed, just for nurses</small></a></li>
          <li><a href="blog.html">Blog <small>News, tips &amp; nurse life</small></a></li>
        </ul>
      </div>
      <div>
        <h4>More</h4>
        <ul class="mega-links slim">
          <li><a href="about.html">About</a></li>
          <li><a href="careers.html">Careers</a></li>
          <li><a href="help.html">Help Center</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="support.html">Support</a></li>
          <li><a href="settings.html">Settings</a></li>
        </ul>
      </div>
      <a class="mega-promo" href="nclex-complete.html">
        <span class="art">NCLEX</span>
        <b>NCLEX Complete</b>
        <p>50 cases, 2,600+ questions, 4 readiness exams &amp; Esi — from $59.</p>
        <span class="btn btn-coral" style="padding:0.6rem 1.3rem; font-size:0.85rem;">See the plans</span>
      </a>
    </div>
  </nav>

{body}

  <footer class="site-footer">
    <div class="wrap footer-main">
      <div class="footer-brand">
        <a class="logo" href="index.html">
          <span class="mark">M<b>&#10084;</b>S</span>
          <span class="word" style="color:#fff;">Must <i>Love</i> Scrubs</span>
        </a>
        <p>Education with a pulse. Free NCLEX practice, warm community, and tools built for the nurse you're becoming.</p>
        <div class="footer-social">
          <a href="https://facebook.com/mustlovescrubs" aria-label="Facebook">{I['fb']}</a>
          <a href="https://tiktok.com/@mustlovescrubs" aria-label="TikTok">{I['tiktok']}</a>
        </div>
      </div>
      <div class="footer-col">
        <h5>Learn</h5>
        <ul>
          <li><a href="nclex-complete.html">NCLEX Complete</a></li>
          <li><a href="qbank.html">Question Bank</a></li>
          <li><a href="tests.html">Tests &amp; Exams</a></li>
          <li><a href="flashcards.html">Flashcards &amp; Games</a></li>
          <li><a href="drugs.html">Drug Cards</a></li>
          <li><a href="cheatsheets.html">Cheat Sheets</a></li>
          <li><a href="lab-values.html">Lab Values</a></li>
          <li><a href="mnemonics.html">Mnemonics</a></li>
          <li><a href="patho.html">Patho</a></li>
          <li><a href="care-plans.html">Care Plans</a></li>
          <li><a href="study-plan.html">Study Plan Calendar</a></li>
          <li><a href="nclex-guide.html">Free Study Guide</a></li>
          <li><a href="specialties.html">Specialty Prep</a></li>
          <li><a href="courses.html">Courses</a></li>
          <li><a href="course-lab-values.html">Free NCLEX Practice</a></li>
          <li><a href="scrubtv.html">Scrub TV</a></li>
          <li><a href="esi.html">Esi Tutoring</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Discover</h5>
        <ul>
          <li><a href="dictionary.html">Nurses Index</a></li>
          <li><a href="spotlight.html">Spotlight</a></li>
          <li><a href="jobs.html">Job Search</a></li>
          <li><a href="blog.html">Blog</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Company</h5>
        <ul>
          <li><a href="about.html">About</a></li>
          <li><a href="help.html">Help Center</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="support.html">Support</a></li>
        </ul>
      </div>
    </div>
    <div class="wrap footer-bottom">
      <span>&copy; 2026 Must Love Scrubs. All rights reserved. &middot; hello@mustlovescrubs.com &middot; Educational content only, not clinical advice.</span>
      <div class="legal-links">
        <a href="privacy.html">Privacy</a>
        <a href="terms.html">Terms</a>
      </div>
    </div>
  </footer>

  <nav class="bottom-nav" aria-label="Quick navigation">
    <a class="bn-item{' active' if active == 'home' else ''}" href="index.html">{I['home']}<span>Home</span></a>
    <a class="bn-item{' active' if active == 'courses' else ''}" href="courses.html">{I['book']}<span>Courses</span></a>
    <a class="bn-item bn-center" href="scrubtv.html"><span class="puck">{I['play']}</span><span>Scrub TV</span></a>
    <a class="bn-item{' active' if active == 'dictionary' else ''}" href="dictionary.html">{I['dict']}<span>Index</span></a>
    <a class="bn-item{' active' if active == 'profile' else ''}" href="profile.html">{I['user']}<span>Profile</span></a>
  </nav>

  <button class="esi-fab" data-esi-launch aria-label="Esi — your AI tutor">
    <span class="orb"></span>
    <span>Esi</span>
  </button>

  <a class="feedback-fab" href="mailto:zuripluslola@gmail.com?subject=Must%20Love%20Scrubs%20feedback&amp;body=What%20I%20tried%3A%0A%0AWhat%20I%20loved%3A%0A%0AWhat%20was%20confusing%20or%20missing%3A%0A%0AWould%20I%20use%20this%20to%20study%3F%20" aria-label="Send feedback">
    {I['chat']}
    <span>Feedback</span>
  </a>

  <script src="js/main.js"></script>
</body>
</html>
"""

def page_hero(title_html, sub, extra=""):
    return f"""  <div class="page-hero">
    <div class="wrap inner">
      <h1>{title_html}</h1>
      <p>{sub}</p>
      {extra}
    </div>
  </div>
"""

CATS = [
    ("er", "ER / Trauma", "c1"), ("prenatal", "Prenatal &amp; L&amp;D", "c2"),
    ("peds", "Pediatrics", "c3"), ("icu", "ICU / Critical Care", "c4"),
    ("medsurg", "Med-Surg", "c2"), ("pharm", "Pharmacology", "c1"),
    ("mental", "Mental Health", "c4"), ("geri", "Geriatrics", "c3"),
]

def cat_grid():
    cells = []
    for icon, label, color in CATS:
        cells.append(f'<a class="cat fade-up" href="scrubtv.html"><span class="ico {color}">{I[icon]}</span><b>{label}</b><span>Watch &middot; Quiz &middot; Earn</span></a>')
    return '<div class="cat-grid">' + "".join(cells) + '</div>'

VIDEOS = [
    ("ER / TRAUMA", "Triage in 90 seconds: who do you see first?", "linear-gradient(140deg,#4d2b9e,#7a45f0)", 25),
    ("PHARMACOLOGY", "Beta blockers, explained the way you'll remember", "linear-gradient(140deg,#1a0942,#14b8a8)", 25),
    ("PRENATAL & L&D", "Decels decoded: early, late &amp; variable", "linear-gradient(140deg,#4d2b9e,#d99a1f)", 25),
]

def video_row():
    out = []
    for meta, title, grad, pts in VIDEOS:
        out.append(f"""<a class="vid fade-up" href="scrubtv.html">
          <span class="bg" style="background:{grad};"></span>
          <span class="play">{I['play']}</span>
          <span class="meta">{meta}</span>
          <b>{title}</b>
          <span class="pts">{I['star']} +{pts} pts with quiz</span>
        </a>""")
    return '<div class="video-row">' + "".join(out) + '</div>'

COURSE_SHELF = [
    ("Pharmacology Mastery", "220 questions · flashcards · mnemonics", "$59", "linear-gradient(140deg,#7a45f0,#4d2b9e)", "RX"),
    ("Med-Surg Essentials", "8 systems · case studies · mock exams", "$69", "linear-gradient(140deg,#14b8a8,#1a0942)", "MS"),
    ("Prioritization &amp; Delegation", "NGN-style clinical judgment drills", "$49", "linear-gradient(140deg,#d99a1f,#7a45f0)", "NGN"),
    ("Dosage Calculation Bootcamp", "Step-by-step method · 300 practice problems", "$49", "linear-gradient(140deg,#4d2b9e,#14b8a8)", "CALC"),
]

def course_shelf():
    out = []
    for name, desc, price, grad, tag in COURSE_SHELF:
        out.append(f"""<article class="course-card fade-up">
          <div class="cover" style="background:{grad};">{tag}</div>
          <div class="body">
            <b>{name}</b><small>{desc}</small>
            <div class="foot"><span class="p">{price}</span><a href="courses.html">View course &rarr;</a></div>
          </div>
        </article>""")
    return '<div class="course-shelf">' + "".join(out) + '</div>'

# -------- Subscription pricing (3 tiers, Esi included, duration-based) --------
TIERS = [
    {"dur": "1 Month", "sub": "of full access", "was": "$99", "now": "59", "permo": "$59/mo",
     "save": "Save $40", "rec": "", "feat": False, "guar": False,
     "blurb": "Testing soon and just need reps and a plan? Start here."},
    {"dur": "2 Months", "sub": "of full access", "was": "$169", "now": "99", "permo": "$50/mo",
     "save": "Save $70", "rec": "Most popular", "feat": True, "guar": True,
     "blurb": "The timeline most students choose &mdash; room to fix every weak area."},
    {"dur": "3 Months", "sub": "of full access", "was": "$219", "now": "129", "permo": "$43/mo",
     "save": "Save $90", "rec": "", "feat": False, "guar": True,
     "blurb": "Working full-time or rebuilding your foundation? This fits."},
    {"dur": "6 Months", "sub": "of full access", "was": "$349", "now": "199", "permo": "$33/mo",
     "save": "Save $150", "rec": "Best value", "feat": False, "guar": True,
     "blurb": "The lowest price per month &mdash; go at your own pace, stress-free."},
]
TIER_FEATURES = [
    "2,600+ original NCLEX questions &mdash; RN &amp; PN",
    "50 Next Gen case studies with walkthroughs",
    "4 full-length CAT readiness exams",
    "Next Gen strategy video course",
    "Personalized study schedule &amp; calendar",
    "Mastered / Reviewing / Learning tagging",
    "Performance by subject area",
    "140+ cheat sheets &amp; the Nurses Index",
]

def pricing_tiers(cta="join.html"):
    li = "".join(f"<li>{I['check']}{f}</li>" for f in TIER_FEATURES)
    cards = []
    for t in TIERS:
        rec = ""
        if t["rec"]:
            rec = f'<span class="rec-tab{"" if t["feat"] else " alt"}">{t["rec"]}</span>'
        guar = (f'<li>{I["shield"]}<b style="color:var(--teal-600);">Pass Guarantee</b> '
                "&mdash; full refund if you don't pass</li>") if t["guar"] else ""
        btncls = "btn-coral" if t["feat"] else "btn-line"
        cls = " feat" if t["feat"] else (" best" if t["rec"] else "")
        cards.append(f"""<div class="tier{cls} fade-up">
          {rec}
          <div class="dur">{t['dur']}<small>{t['sub']}</small></div>
          <div class="cost"><span class="was">{t['was']}</span><span class="now">${t['now']}</span><span class="usd">USD</span></div>
          <div class="permo">{t['permo']} &middot; Esi included</div>
          <span class="save">{t['save']} instantly</span>
          <p class="blurb">{t['blurb']}</p>
          <a class="btn {btncls} tier-cta" href="{cta}">Get {t['dur']}</a>
          <div class="esi-in"><span class="orb"></span> Esi AI tutor included &mdash; free</div>
          <ul>{li}{guar}</ul>
        </div>""")
    return '<div class="tiers">' + "".join(cards) + '</div>'

PRODUCTS = [
    ("Scrub Life Tote Bag", "$24", "linear-gradient(140deg,#a78bff,#14b8a8)", "M❤S"),
    ("Coffee &amp; Compassion Mug", "$18", "linear-gradient(140deg,#8b5cff,#7a45f0)", "MLS"),
    ("Must Love Scrubs Tee", "$28", "linear-gradient(140deg,#2b1055,#4d2b9e)", "M❤S"),
    ("Shift Survival Tumbler", "$26", "linear-gradient(140deg,#ffc23d,#d99a1f)", "MLS"),
    ("Night Shift Hoodie", "$44", "linear-gradient(140deg,#4d2b9e,#1a0942)", "M❤S"),
    ("Badge Buddy Sticker Pack", "$9", "linear-gradient(140deg,#a78bff,#4d2b9e)", "MLS"),
    ("Nurse Era Crewneck", "$38", "linear-gradient(140deg,#7a45f0,#ffc23d)", "M❤S"),
    ("Clipboard Confidence Notebook", "$14", "linear-gradient(140deg,#14b8a8,#2b1055)", "MLS"),
]

def product_grid(limit=None):
    items = PRODUCTS[:limit] if limit else PRODUCTS
    out = []
    for name, price, grad, logo in items:
        out.append(f"""<a class="product fade-up" href="store.html">
          <div class="shot" style="background:{grad};"><span class="logo-print">{logo}</span></div>
          <div class="body"><b>{name}</b><span class="p">{price}</span></div>
        </a>""")
    return '<div class="product-grid">' + "".join(out) + '</div>'

DIGITAL = [
    "Study Guides &amp; Cheat Sheets", "Report / Brain Sheets", "Badge Reference Cards",
    "Nursing School Planners", "Drug Cards", "Care Plan Templates",
    "Resume &amp; New-Grad Kits", "Nurse Wall Art &amp; Printables",
]

TESTIMONIALS = [
    ("The videos plus the quizzes right underneath — that combo made things finally stick for me.", "J.M.", "RN, Med-Surg", "#7a45f0"),
    ("I passed on my first try. The way this course teaches you to THINK through questions changed everything.", "A.T.", "New Grad RN", "#14b8a8"),
    ("Esi feels like having a tutor in my pocket. She catches my weak areas before I do.", "S.K.", "Nursing Student", "#4d2b9e"),
    ("Finally a nursing site that doesn't look and feel like it was built in 2009.", "D.R.", "Travel Nurse", "#d99a1f"),
]

def testi_track():
    out = []
    for quote, name, role, color in TESTIMONIALS:
        out.append(f"""<figure class="testi">
          <span class="sample-tag">Sample &middot; real reviews coming</span>
          <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
          <p>“{quote}”</p>
          <figcaption class="who"><span class="av" style="background:{color};">{name[0]}</span><span><b>{name}</b><span>{role}</span></span></figcaption>
        </figure>""")
    return '<div class="testi-track">' + "".join(out) + '</div>'

FAQS = [
    ("What is NCLEX Complete?", "Our flagship NCLEX prep: 50 Next Gen case studies with walkthroughs, 2,600+ original questions, a strategy video course, and four full-length readiness exams that predict your pass chance — plus a study schedule and Esi, your AI tutor. Everything's included in one plan."),
    ("How is this different from other NCLEX question banks?", "Most banks hand you thousands of questions and wish you luck. We teach you to <b>think like a nurse</b> — every question has a rationale for every option, case studies show the reasoning, and Esi drills exactly what you keep missing. It's built on how memory actually works."),
    ("Is there a pass guarantee?", "Yes. On the 2- and 3-month plans, finish the program and if you don't pass, you get a full refund. We built it to work and we stand behind it."),
    ("Is it updated for the Next Gen NCLEX (NGN)?", "Completely. Every item type on the current test plan is here — case studies, bow-tie, trend, matrix, select-all, and more — and our practice exams run on a real computer-adaptive engine, so test day feels familiar."),
    ("Can I use it for the NCLEX-PN (LPN)?", "Yes — the question bank has both an RN and a PN track. Pick your exam and the questions adapt to your scope of practice."),
    ("Is Esi, the AI tutor, included?", "Yes — Esi comes with every plan at no extra cost. She tracks your weak areas, builds your study plan, and turns every miss into a targeted drill. There's no separate add-on."),
    ("What's free versus paid?", "Free forever: NCLEX practice with every item type, four Scrub TV lessons a month, the Nurses Index, and daily points. Paid unlocks the full question bank, case studies, readiness exams, schedules, the workbook, and Esi."),
    ("Can I study on my phone?", "Absolutely — the entire experience is mobile-first with app-style navigation. Study on the bus, in the break room, or on the couch."),
]

ESI_FAQS = [
    ("What exactly is Esi?", "Esi is your AI nursing tutor. She explains what you missed, drills your weak areas, builds your study plan, and helps you find anything on the site — like a preceptor and a guide in one."),
    ("Is Esi included in my plan?", "Yes. Esi comes with every NCLEX Complete plan at no extra charge. There's nothing separate to buy."),
    ("Can Esi diagnose or give medical advice?", "No. Esi is an educational tutor only. She never diagnoses, prescribes, or replaces clinical judgment, faculty, or professional medical care. In an emergency, call 911."),
    ("How does Esi know my weak areas?", "She watches your quiz and question results, spots the topics you keep missing, and schedules focused reviews at the moment you're about to forget — spaced repetition, automated."),
    ("Can I chat with Esi for free?", "Esi lives inside your subscription, so there's no free open chat. You can preview exactly what she does on this page, then unlock her with any plan."),
    ("Does Esi work on my phone?", "Yes — Esi is right there in the app-style experience on any device, whenever you sit down to study."),
]

def faq_list(faqs=FAQS):
    out = []
    chev = '<svg class="chev" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="m6 9 6 6 6-6"/></svg>'
    for q, a in faqs:
        out.append(f"""<div class="faq-item">
          <button class="faq-q">{q} {chev}</button>
          <div class="faq-a"><p>{a}</p></div>
        </div>""")
    return '<div class="faq-list">' + "".join(out) + '</div>'

# ---------------------------------------------------------------- HOMEPAGE
def _student(x, top, skin, hair, scrub):
    # a seated student at a desk taking a test
    return f"""<g transform="translate({x},{top})">
      <rect x="-34" y="96" width="108" height="14" rx="4" fill="#3a1f7a"/>
      <rect x="-20" y="86" width="80" height="14" rx="3" fill="#f6f3ff"/>
      <path d="M-2 40 q22 -30 44 0 l6 54 h-56z" fill="{scrub}"/>
      <circle cx="20" cy="20" r="18" fill="{skin}"/>
      <path d="M4 16a18 18 0 0 1 32-4l3-8a24 24 0 0 0-40 6z" fill="{hair}"/>
      <path d="M2 60 q-16 14 -22 26l9 8q16 -12 24 -24z" fill="{scrub}"/>
    </g>"""

HERO_SCENE = f"""<svg viewBox="0 0 560 420" role="img" aria-label="Nursing students taking a test in a classroom">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4d2b9e"/><stop offset="1" stop-color="#2b1055"/></linearGradient>
    <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a1f7a"/><stop offset="1" stop-color="#1a0942"/></linearGradient>
  </defs>
  <rect width="560" height="420" fill="url(#sky)"/>
  <rect y="312" width="560" height="108" fill="url(#floor)"/>
  <!-- whiteboard -->
  <rect x="60" y="40" width="200" height="118" rx="10" fill="#f6f3ff"/>
  <path d="M78 70h150M78 92h150M78 114h96" stroke="#8b5cff" stroke-width="6" stroke-linecap="round" opacity="0.6"/>
  <path d="M78 136 h24 l8-14 10 26 9-12h55" stroke="#14b8a8" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- clock -->
  <circle cx="330" cy="70" r="24" fill="#2b1055" stroke="#a78bff" stroke-width="3"/>
  <path d="M330 70 L330 55 M330 70 L342 74" stroke="#ffc23d" stroke-width="3" stroke-linecap="round"/>
  <!-- three students at desks taking the test -->
  {_student(70, 210, '#e8b088', '#2a1a12', '#14b8a8')}
  {_student(240, 210, '#f4c39a', '#3b2a20', '#8b5cff')}
  {_student(410, 210, '#c98d63', '#161616', '#a78bff')}
  <circle cx="500" cy="52" r="3" fill="#ffc23d"/><circle cx="524" cy="120" r="2" fill="#a78bff" opacity="0.8"/>
  <circle cx="40" cy="188" r="2.5" fill="#14b8a8" opacity="0.8"/>
</svg>"""

HOME_LESSONS = [
    ("01", "Critical Lab Values", "course-lab-values.html", "linear-gradient(135deg,#4d2b9e,#14b8a8)"),
    ("02", "Prioritization &amp; Delegation", "course-prioritization.html", "linear-gradient(135deg,#2b1055,#8b5cff)"),
    ("03", "Medication Safety", "course-med-safety.html", "linear-gradient(135deg,#4d2b9e,#ffb038)"),
    ("04", "Spot the Deterioration", "course-deterioration.html", "linear-gradient(135deg,#2b1055,#e5484d)"),
]
def home_lessons():
    out = []
    for num, name, slug, grad in HOME_LESSONS:
        out.append(f'<a class="course-card fade-up" href="{slug}"><div class="cover" style="background:{grad};">{num}</div><div class="body"><b>{name}</b><small>Audio scene + 4 tests &middot; Free</small><div class="foot"><span class="p" style="color:var(--teal-600);">Free</span><span style="font-size:0.82rem;font-weight:700;color:var(--coral-500);">Start &rarr;</span></div></div></a>')
    return '<div class="course-shelf">' + "".join(out) + '</div>'

# Homepage RN-specialties carousel (a curated few; full list on specialties.html)
HOME_SPECS = [
    ("emergency", "Emergency / ER", "er", "linear-gradient(140deg,#e5484d,#7a45f0)", "$69"),
    ("critical-care", "Critical Care / ICU", "icu", "linear-gradient(140deg,#2ad4c4,#1a0942)", "$79"),
    ("pediatrics", "Pediatrics", "peds", "linear-gradient(140deg,#ffc23d,#8b5cff)", "$59"),
    ("med-surg", "Medical-Surgical", "medsurg", "linear-gradient(140deg,#8b5cff,#4d2b9e)", "$59"),
    ("labor-delivery", "Labor &amp; Delivery / OB", "prenatal", "linear-gradient(140deg,#8b5cff,#14b8a8)", "$69"),
    ("oncology", "Oncology", "shield", "linear-gradient(140deg,#7a45f0,#d99a1f)", "$69"),
    ("cardiac", "Cardiac / Telemetry", "icu", "linear-gradient(140deg,#e5484d,#2b1055)", "$69"),
]
def home_spec_carousel():
    out = []
    for slug, name, icon, grad, price in HOME_SPECS:
        out.append(f"""<a class="spec-card fade-up" href="specialty-{slug}.html">
          <span class="spec-lock">{I['lock']} Soon</span>
          <span class="ic" style="background:{grad};">{I[icon]}</span>
          <h3>{name}</h3>
          <div class="foot"><span class="price">{price}</span><span class="go">Preview &rarr;</span></div>
        </a>""")
    return '<div class="spec-rail">' + "".join(out) + '</div>'

INDEX_BODY = f"""  <main>
    <section class="hero">
      <div class="hero-layer" data-parallax="0.22" aria-hidden="true">
        <div class="glow glow-coral"></div><div class="glow glow-teal"></div><div class="glow glow-gold"></div>
      </div>
      <div class="wrap hero-grid">
        <div>
          <span class="flag">{I['star']} FREE NCLEX PRACTICE &mdash; NO CARD NEEDED</span>
          <h1>Train for the nurse you're <span class="hl on-dark">becoming</span>.</h1>
          <p class="lede">Free NCLEX practice, audio scenes that teach like a great preceptor, and Esi &mdash; the AI tutor that makes it stick. This is the ecosystem of nursing.</p>
          <div class="hero-cta">
            <a class="btn btn-coral" href="course-lab-values.html">Try a free lesson</a>
            <a class="btn btn-ghost" href="courses.html">See all courses</a>
          </div>
          <p class="hero-note">Free practice &middot; 10 points a day &middot; no card required</p>
        </div>
        <div class="hero-visual fade-up">
          <div class="scene">{HERO_SCENE}</div>
          <div class="float-chip tl"><span class="ico" style="background:var(--teal-100);color:var(--teal-600);">{I['check']}</span> Clinical-judgment focused</div>
          <div class="float-chip br"><span class="ico" style="background:var(--gold-100);color:var(--gold-600);">{I['star']}</span> Earn points as you learn</div>
          <span class="scene-tag">Swap-ready: students-in-class photo goes here</span>
        </div>
      </div>
    </section>

    <section class="scrubtv" id="scrubtv">
      <div class="wrap">
        <div class="section-head fade-up">
          <div class="row">
            <div>
              <span class="eyebrow">Scrub TV &middot; Free</span>
              <h2>Four free lessons. <span class="hl">Every month.</span></h2>
              <p>Each is a curated audio scene plus a full workout — memory game, matrix, chart test, and a clinical quick check.</p>
            </div>
            <a class="tv-btn" href="scrubtv.html" aria-label="Browse free Scrub TV lessons">
              <span class="tv-antenna"></span>
              <span class="tv-screen"><span class="tv-scan"></span><span class="tv-label">Scrub<b>T.V.</b></span></span>
              <span class="tv-stand"></span>
              <span class="tv-cta">Browse free lessons</span>
            </a>
          </div>
        </div>
        {home_lessons()}
      </div>
    </section>

    <section class="welcome">
      <div class="hero-layer" data-parallax="0.14" aria-hidden="true"><div class="glow glow-coral" style="opacity:0.5;"></div></div>
      <div class="wrap fade-up" style="position:relative;z-index:2;">
        <p class="kicker">A home built by nurses, for nurses</p>
        <h2>WELCOME <span class="heart">HOME</span>.</h2>
        <p class="sub">A home built by nurses, for nurses &mdash; because we remember exactly how the NCLEX felt, and how clunky the tools were. Must Love Scrubs is prep as excellent as the care you give, from people who've stood where you're standing.</p>
        {photo('nurses-group.jpg', 'linear-gradient(135deg,#4d2b9e,#14b8a8)', 'margin-top:2rem;min-height:300px;max-width:900px;margin-left:auto;margin-right:auto;')}
        <p style="margin-top:1.2rem;font-size:0.9rem;"><a href="nclex-guide.html" style="color:var(--gold-400);font-weight:800;">Read our free NCLEX study guide &rarr;</a></p>
      </div>
    </section>

    <section class="courses" id="courses">
      <div class="wrap">
        <div class="section-head fade-up">
          <span class="eyebrow teal">Featured Courses</span>
          <h2>Prep that teaches you to <span class="hl">think</span>, not memorize.</h2>
        </div>
        <div class="course-hero fade-up">
          <div class="art"><span class="big">NCLEX</span></div>
          <div class="body">
            <div class="chip-row"><span class="chip gold">FLAGSHIP</span><span class="chip teal">NGN READY</span><span class="chip">Esi compatible</span></div>
            <h3>NCLEX Complete</h3>
            <p>The full journey to test day: adaptive question banks, clinical-judgment case studies, mock exams in real test format, and analytics that show exactly where you're strong and where you're not.</p>
            <div class="price-line"><span class="price">from $59</span><span class="per">Esi tutor included &middot; Pass Guarantee</span></div>
            <div class="chip-row"><span class="chip gold">4 plans &rarr; 1, 2, 3 or 6 months &middot; everything unlocked</span></div>
            <a class="btn btn-coral" href="nclex-complete.html">Explore NCLEX Complete</a>
          </div>
        </div>
      </div>
    </section>

    <section class="why">
      <div class="wrap">
        <div class="section-head fade-up">
          <span class="eyebrow">Why Must Love Scrubs</span>
          <h2>Not another <span class="hl">cookie-cutter</span> nursing site.</h2>
        </div>
        <div class="why-grid">
          <article class="why-card fade-up">
            <span class="num">01</span>
            <h3>Innovative, proven — not generic</h3>
            <p>Most nursing sites are clones of each other. Ours is built on proven systems for retaining information — spaced repetition, active recall, and clinical-judgment reasoning — woven into every course and video.</p>
          </article>
          <article class="why-card fade-up">
            <span class="num">02</span>
            <h3>Esi revolutionizes learning</h3>
            <p>An AI tutor who knows your weak areas before you do, guides your study plan, and walks you through the site like a friend who works here. No other prep platform has her.</p>
          </article>
          <article class="why-card fade-up">
            <span class="num">03</span>
            <h3>Massive prep library</h3>
            <p>NCLEX Complete leads a growing catalog — 22 specialty tracks, pharmacology, med-surg, peds, mental health, NGN drills — with new content added constantly.</p>
          </article>
          <article class="why-card fade-up">
            <span class="num">04</span>
            <h3>Free that beats their paid</h3>
            <p>Your free account already includes NCLEX practice with every NGN item type, four full lessons a month, and the Nurses Index — deeper than what most sites put behind a paywall.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="courses">
      <div class="wrap">
        <div class="section-head fade-up">
          <div class="row">
            <div>
              <span class="eyebrow teal">RN Specialties</span>
              <h2>Prep for <span class="hl">where you're going.</span></h2>
              <p>Passed the NCLEX? Keep going. Focused prep for the specialty you're headed into &mdash; rolling out now.</p>
            </div>
            <a class="btn btn-coral" href="specialties.html">See all 22 specialties</a>
          </div>
        </div>
        {home_spec_carousel()}
      </div>
    </section>

    <section style="background:linear-gradient(150deg,var(--teal-600),var(--indigo-700));color:#fff;">
      <div class="wrap fade-up">
        <span class="eyebrow" style="color:var(--gold-400);">Points &amp; rewards</span>
        <h2 style="font-size:clamp(2rem,6vw,3rem);max-width:18ch;">Get <span class="hl">points</span> for learning.</h2>
        <p style="margin-top:1rem;max-width:54ch;color:rgba(255,255,255,0.82);">Every lesson you finish and every practice test you pass earns points &mdash; then redeem them for course discounts, downloads, and the Nurses Index. Your prep literally pays you back.</p>
        <div style="display:grid;gap:1rem;margin-top:2.4rem;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));">
          <div style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.16);border-radius:var(--radius);padding:1.4rem;"><div style="font-family:var(--font-display);font-size:1.6rem;color:var(--gold-400);font-weight:800;">01</div><b style="display:block;margin-top:0.4rem;">Learn &amp; prep</b><span style="font-size:0.85rem;color:rgba(255,255,255,0.7);">Any Scrub TV lesson or free NCLEX practice earns points.</span></div>
          <div style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.16);border-radius:var(--radius);padding:1.4rem;"><div style="font-family:var(--font-display);font-size:1.6rem;color:var(--gold-400);font-weight:800;">02</div><b style="display:block;margin-top:0.4rem;">Pass a test</b><span style="font-size:0.85rem;color:rgba(255,255,255,0.7);">Quizzes and practice tests pay out more the better you score.</span></div>
          <div style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.16);border-radius:var(--radius);padding:1.4rem;"><div style="font-family:var(--font-display);font-size:1.6rem;color:var(--gold-400);font-weight:800;">03</div><b style="display:block;margin-top:0.4rem;">Bank points + streak</b><span style="font-size:0.85rem;color:rgba(255,255,255,0.7);">10 free a day, plus quiz, test &amp; streak bonuses.</span></div>
          <div style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.16);border-radius:var(--radius);padding:1.4rem;"><div style="font-family:var(--font-display);font-size:1.6rem;color:var(--gold-400);font-weight:800;">04</div><b style="display:block;margin-top:0.4rem;">Redeem the reward</b><span style="font-size:0.85rem;color:rgba(255,255,255,0.7);">Course discounts, store downloads &amp; the Nurses Index.</span></div>
        </div>
      </div>
    </section>

    <section class="store">
      <div class="wrap">
        <div class="course-hero fade-up" style="box-shadow:var(--shadow-2);">
          <div class="art" style="background:url(images/dictionary.jpg) center/cover no-repeat, radial-gradient(circle at 70% 25%, rgba(255,201,77,0.4), transparent 50%), radial-gradient(circle at 20% 80%, rgba(139,92,255,0.5), transparent 55%), linear-gradient(150deg,#2b1055,#4d2b9e);"></div>
          <div class="body">
            <div class="chip-row"><span class="chip gold">NEW TOOL</span><span class="chip teal">217+ terms</span></div>
            <h3>The Nurses Index</h3>
            <p>Every term, abbreviation, and bit of nurse-speak &mdash; in plain language. <b>Free to search online.</b> Or get the full download: every word with a <b>real clinical example + rationale</b>, so it actually sticks.</p>
            <div class="price-line"><span class="price">$4.99</span><span class="per">download &middot; or unlock with points &middot; free with any course</span></div>
            <div class="hero-cta" style="margin-top:0.4rem;"><a class="btn btn-coral" href="dictionary.html">Open the Nurses Index</a><a class="btn btn-line" href="dictionary.html#download">Get the download</a></div>
          </div>
        </div>
      </div>
    </section>

    <section class="proof">
      <div class="wrap">
        <div class="stat-row">
          <div class="stat-big lead fade-up"><b><span data-count="1400">0</span><span class="plus">+</span></b><span>Course users already in</span></div>
          <div class="stat-big fade-up"><b><span data-count="48">0</span></b><span>Free lessons a year &mdash; 4 every month</span></div>
          <div class="stat-big fade-up"><b><span data-count="22">0</span></b><span>Specialty tracks rolling out</span></div>
        </div>
        <div class="trust-row fade-up">
          <span class="trust">{I['lock']} Secure checkout</span>
          <span class="trust">{I['shield']} SSL encrypted</span>
          <span class="trust">{I['card']} Powered by Stripe &amp; Shopify</span>
          <span class="trust">{I['check']} 7-day money-back guarantee</span>
        </div>
      </div>
    </section>

    <section class="testis">
      <div class="wrap">
        <div class="section-head fade-up">
          <span class="eyebrow">Nurses talking</span>
          <h2>Loved by the people who <span class="hl">do the work</span>.</h2>
        </div>
        {testi_track()}
      </div>
    </section>

    <section class="faq">
      <div class="wrap">
        <div class="section-head fade-up" style="text-align:center;margin-inline:auto;">
          <span class="eyebrow teal">NCLEX FAQ</span>
          <h2>Everything you're wondering about <span class="hl">NCLEX prep</span>.</h2>
        </div>
        {faq_list()}
      </div>
    </section>

    <section class="join">
      <div class="wrap">
        <div class="join-card fade-up">
          <span class="eyebrow" style="color:var(--gold-400);">Join the community</span>
          <h2>Your journey starts with a free account.</h2>
          <p>Daily points, progress tracking, saved content, and a front-row seat as the ecosystem grows.</p>
          <a class="btn btn-coral" href="join.html">Create my free account</a>
          <div class="perks">
            <span>{I['check']} Free forever</span>
            <span>{I['check']} 10 points daily</span>
            <span>{I['check']} No card required</span>
          </div>
        </div>
      </div>
    </section>
  </main>
"""

# ---------------------------------------------------------------- SUBPAGES
def simple_prose(title, sub, blocks, draft=False, active=""):
    note = '<div class="draft-note">DRAFT — sample language for review by your attorney. Not yet legally binding.</div>' if draft else ""
    return page_hero(title, sub) + f"""  <main class="content-block">
    <div class="wrap prose">
      {note}{blocks}
    </div>
  </main>
"""

PAGES = {}

PAGES["index.html"] = ("Must Love Scrubs — The Ecosystem of Nursing",
    "Premium nursing education: NCLEX prep, Scrub TV learning videos, Esi the AI tutor, and a curated nurse lifestyle store.",
    INDEX_BODY, "home")

PAGES["courses.html"] = ("Courses — Must Love Scrubs",
    "NCLEX prep and specialty nursing courses built on proven retention science.",
    page_hero('Prep that teaches you to <span class="hl on-dark">think</span>.',
              "Adaptive question banks, real test-format mocks, and analytics that show your exact weak areas &mdash; with Esi, a tutor who never sleeps, included in every plan.",
              '<div class="hero-cta" style="margin-top:1.8rem;"><a class="btn btn-coral" href="nclex-complete.html">Explore NCLEX Complete</a><a class="btn btn-ghost" href="join.html">Start free</a></div>')
    + f"""  <main class="content-block">
    <div class="wrap">
      <div class="section-head fade-up"><span class="eyebrow gold">The flagship</span><h2>Start with <span class="hl">NCLEX Complete.</span></h2><p>One subscription, everything included &mdash; the fastest path to test day.</p></div>
      <div class="course-hero fade-up">
        <div class="art" style="background:url(images/dictionary.jpg) center/cover no-repeat, radial-gradient(circle at 70% 25%, rgba(255,201,77,0.35), transparent 50%), linear-gradient(150deg,#2b1055,#4d2b9e);"><span class="big">NCLEX</span></div>
        <div class="body">
          <div class="chip-row"><span class="chip gold">FLAGSHIP</span><span class="chip teal">NGN READY</span><span class="chip">Esi included</span></div>
          <h3>NCLEX Complete</h3>
          <p>Everything to test day: 50 case studies, 2,600+ questions, 4 readiness exams, timed mocks in real format, score analytics, and a visual progress map. Built on how memory actually works &mdash; spaced repetition and active recall, not cramming.</p>
          <div class="price-line"><span class="price">from $59</span><span class="per">Esi tutor included &middot; Pass Guarantee</span></div>
          <div class="chip-row"><span class="chip gold">4 plans &rarr; 1, 2, 3 or 6 months &middot; everything unlocked</span></div>
          <a class="btn btn-coral" href="nclex-complete.html">Explore NCLEX Complete</a>
        </div>
      </div>

      <div class="section-head fade-up" style="margin-top:3.5rem;"><span class="eyebrow teal">Focused courses</span><h2>Drill a single <span class="hl">weak area.</span></h2><p>Targeted mini-courses when you just need to shore up one topic fast.</p></div>
      {course_shelf()}

      <div class="section-head fade-up" style="margin-top:3.5rem;">
        <div class="row">
          <div><span class="eyebrow">Specialty prep</span><h2>Prep for your <span class="hl">specialty.</span></h2><p>The clinical specialty you're headed into &mdash; 22 tracks rolling out.</p></div>
          <a class="btn btn-coral" href="specialties.html">See all 22 specialties</a>
        </div>
      </div>
      {home_spec_carousel()}

      <div class="section-head fade-up" style="margin-top:3.5rem;"><span class="eyebrow gold">Free to start</span><h2>Free that beats their <span class="hl">paid.</span></h2><p>Four full lessons a month, free NCLEX practice, and the Nurses Index &mdash; no card required.</p></div>
      {home_lessons()}
      <div class="two-up fade-up" style="margin-top:1.2rem;">
        <a class="wide-card" href="nclex.html">
          <span class="wc-ic" style="background:linear-gradient(140deg,#8b5cff,#4d2b9e);">{I['book']}</span>
          <div><b>Free NCLEX practice</b><p>Try every Next Gen item type &mdash; timed recall, trends, matrix, SBAR, select-all.</p></div>
          <span class="wc-go">{I['check']}</span>
        </a>
        <a class="wide-card" href="dictionary.html">
          <span class="wc-ic" style="background:linear-gradient(140deg,#2ad4c4,#1a0942);">{I['dict']}</span>
          <div><b>Nurses Index</b><p>Every term in plain language, free to search. Own the download for the bonus scenarios.</p></div>
          <span class="wc-go">{I['check']}</span>
        </a>
      </div>

      <div class="section-head fade-up" style="margin-top:3.5rem;">
        <span class="eyebrow teal">How it works</span>
        <h2>Learn it once. <span class="hl">Keep it forever.</span></h2>
      </div>
      <div class="tile-grid cols-3">
        <div class="tile fade-up"><span class="tag">Step 1</span><h3>Watch &amp; learn</h3><p>Short, sharp lessons and Scrub TV videos teach the concept the way a great preceptor would.</p></div>
        <div class="tile fade-up"><span class="tag">Step 2</span><h3>Quiz &amp; earn</h3><p>Every lesson ends in active recall — quizzes and puzzles that earn points and cement the knowledge.</p></div>
        <div class="tile fade-up"><span class="tag">Step 3</span><h3>Review with Esi</h3><p>Esi tracks your misses, schedules smart reviews, and drills your weak areas until they're strengths.</p></div>
      </div>
    </div>
  </main>
""", "courses")

PAGES["scrubtv.html"] = ("Scrub TV — Must Love Scrubs",
    "Eight specialty channels of nursing education videos with quizzes and point-earning activities. New drops every two weeks.",
    page_hero('Scrub TV: nursing school meets <span class="hl on-dark">your feed</span>.',
              "Eight channels. Fresh videos every two weeks. Watch the video, take the quiz, earn the points — and actually remember it on the floor.")
    + f"""  <main class="content-block">
    <div class="wrap">
      <div class="section-head fade-up"><span class="eyebrow">Channels</span><h2>Pick your specialty.</h2></div>
      {cat_grid()}
      <div class="section-head fade-up" style="margin-top:3rem;">
        <div class="row">
          <div><span class="eyebrow teal">This fortnight</span><h2>Fresh drops.</h2><p>New videos rotate in every two weeks — catch them here and on TikTok &amp; Facebook.</p></div>
        </div>
      </div>
      {video_row()}
      <div class="points-strip fade-up" style="margin-top:2rem;">
        <div class="txt"><b>Every video is a lesson in disguise.</b><p>Watch, then take the attached quiz and activities — each one adds points to your balance and progress to your dashboard.</p></div>
        <a class="btn btn-dark" href="profile.html">See my progress</a>
      </div>
    </div>
  </main>
""", "scrubtv")

PAGES["esi.html"] = ("Meet Esi — Your AI Tutor | Must Love Scrubs",
    "Esi is the premium AI tutor inside Must Love Scrubs: 1-on-1 tutoring, weak-area tracking, and site guidance.",
    page_hero('Meet <span class="hl on-dark">Esi</span>. The tutor who never sleeps.',
              "Esi lives inside your courses: she explains what you missed, drills your weak areas, builds your study plan, and helps you find anything on the site. She's why our students remember what others forget.")
    + f"""  <main class="content-block">
    <div class="wrap">
      <div class="tile-grid cols-3">
        <div class="tile fade-up"><span class="tag">Tutoring</span><h3>She knows your weak spots</h3><p>Esi watches your quiz results and targets exactly what you keep missing — then re-tests you at the moment you're about to forget.</p></div>
        <div class="tile fade-up"><span class="tag">Guidance</span><h3>She knows the way</h3><p>Ask her where anything is — a course, a video, your certificates — and she takes you straight there. Like a friend who works here.</p></div>
        <div class="tile fade-up"><span class="tag">Method</span><h3>She teaches thinking</h3><p>NGN-style clinical judgment, walked through step by step. Not what to memorize — how to reason.</p></div>
      </div>
      <div class="join-card fade-up" style="margin-top:2.5rem;">
        <span class="eyebrow" style="color:var(--gold-400);">Included with every plan</span>
        <h2>Esi comes with your subscription.</h2>
        <p><b style="font-size:1.6rem;">$0 extra</b> &nbsp;&middot;&nbsp; included in every NCLEX Complete plan &middot; nothing to add on</p>
        <p style="margin-top:0.6rem;color:var(--gold-400);font-weight:700;">Every plan &mdash; 1, 2, 3, or 6 months &mdash; unlocks Esi in full. Plans start at $59.</p>
        <a class="btn btn-coral" href="nclex-complete.html">See the plans &mdash; from $59</a>
        <a class="btn btn-line" href="#" data-esi-subscribe style="margin-top:0.6rem;">Preview Esi unlocked (demo)</a>
        <div class="perks">
          <span>{I['check']} Unlimited tutoring sessions</span>
          <span>{I['check']} Weak-area tracking</span>
          <span>{I['check']} Smart study plans</span>
        </div>
      </div>
      <p style="margin-top:1.6rem;font-size:0.78rem;color:var(--ink-60);max-width:70ch;">Esi is an educational tutor only. She does not provide medical advice, diagnose, or prescribe, and she is not a substitute for clinical judgment, faculty guidance, or professional medical care. In an emergency, call 911.</p>

      <div class="faq" style="margin-top:3rem;">
        <div class="section-head fade-up" style="text-align:center;margin-inline:auto;">
          <span class="eyebrow teal">Esi FAQ</span>
          <h2>Questions about <span class="hl">Esi</span>.</h2>
        </div>
        {faq_list(ESI_FAQS)}
      </div>
    </div>
  </main>
""", "esi")

PAGES["store.html"] = ("Store — Must Love Scrubs",
    "Curated nurse lifestyle goods with the MLS mark, plus digital downloads redeemable with points.",
    page_hero('Small store. <span class="hl on-dark">Great stuff</span>.',
              "Curated lifestyle pieces for nurse life — every item carries the MLS mark. Print-on-demand via Shopify (connecting soon), plus digital downloads you can buy or redeem with points.")
    + f"""  <main class="content-block">
    <div class="wrap">
      <div class="section-head fade-up"><span class="eyebrow">Lifestyle</span><h2>The collection.</h2></div>
      {product_grid()}
      <div class="section-head fade-up" id="digital" style="margin-top:3.5rem;">
        <span class="eyebrow gold">Digital downloads</span>
        <h2>Buy them — or <span class="hl">earn them</span>.</h2>
        <p>Instant-download tools made for nurses. Every item can also be redeemed with points.</p>
      </div>
      <div class="tile-grid cols-4">
        {"".join(f'<div class="tile fade-up"><span class="tag">Digital</span><h3>{d}</h3><p>Instant download &middot; buy or redeem with points.</p></div>' for d in DIGITAL)}
      </div>
      <div class="points-strip fade-up" style="margin-top:2rem;">
        <div class="txt"><b>10 free points every day.</b><p>Claim daily on your dashboard, stack them up, and cash them in right here.</p></div>
        <a class="btn btn-dark" href="profile.html">Go to my dashboard</a>
      </div>
    </div>
  </main>
""", "store")

PAGES["spotlight.html"] = ("Nurse Spotlight — Must Love Scrubs",
    "Beautifully told stories of real nurses.",
    page_hero('Real nurses. <span class="hl on-dark">Wonderful stories</span>.',
              "Editorial features on the people who hold healthcare together — curated and published by Must Love Scrubs.")
    + """  <main class="content-block">
    <div class="wrap">
      <div class="course-hero fade-up">
        <div class="art" style="background:radial-gradient(circle at 30% 30%, rgba(255,201,77,0.4), transparent 55%), linear-gradient(150deg,#7a45f0,#4d2b9e);"><span class="big">&#10084;</span></div>
        <div class="body">
          <div class="chip-row"><span class="chip gold">FEATURED STORY</span></div>
          <h3>“Twelve-hour shifts taught me everything about people.”</h3>
          <p>Our first featured nurse story is being written right now. Every Spotlight includes a portrait, the full story, and the moment that made them stay in nursing. Your story could be next.</p>
          <a class="btn btn-coral" href="contact.html">Share your story</a>
        </div>
      </div>
      <div class="tile-grid cols-3" style="margin-top:1.2rem;">
        <div class="tile fade-up"><span class="tag">Coming soon</span><h3>The night-shift lifer</h3><p>Twenty-two years of nights, and she wouldn't trade one of them.</p></div>
        <div class="tile fade-up"><span class="tag">Coming soon</span><h3>The second-career nurse</h3><p>From kitchen manager to L&amp;D at 41 — the leap that changed everything.</p></div>
        <div class="tile fade-up"><span class="tag">Coming soon</span><h3>The traveler</h3><p>Nine states, thirty contracts, one rule: never stop learning.</p></div>
      </div>
    </div>
  </main>
""", "")

PAGES["jobs.html"] = ("Job Search — Must Love Scrubs",
    "A small Indeed, just for nurses — search tools and trusted public job resources.",
    page_hero('Find your next <span class="hl on-dark">contract</span>.',
              "A focused job hunt for nurses — search below and use the best public boards in nursing, all in one place.",
              """<form class="hero-cta" style="margin-top:1.8rem;gap:0.6rem;max-width:560px;" onsubmit="return false;">
                <input type="text" placeholder="Specialty, e.g. ICU" aria-label="Specialty" style="flex:1;min-width:150px;padding:0.85rem 1.2rem;border-radius:999px;border:none;font:inherit;font-size:0.92rem;">
                <input type="text" placeholder="City or state" aria-label="Location" style="flex:1;min-width:150px;padding:0.85rem 1.2rem;border-radius:999px;border:none;font:inherit;font-size:0.92rem;">
                <button class="btn btn-coral" type="submit">Search</button>
              </form>""")
    + """  <main class="content-block">
    <div class="wrap">
      <div class="section-head fade-up"><span class="eyebrow">Trusted boards</span><h2>The best public resources, one click away.</h2><p>Live listings integration is coming — until then, these are the boards working nurses actually use.</p></div>
      <div class="tile-grid cols-3">
        <a class="tile fade-up" href="https://www.vivian.com" target="_blank" rel="noopener"><span class="tag">Travel + Perm</span><h3>Vivian Health &rarr;</h3><p>Transparent pay data and thousands of travel contracts.</p></a>
        <a class="tile fade-up" href="https://www.indeed.com/q-nurse-jobs.html" target="_blank" rel="noopener"><span class="tag">Everything</span><h3>Indeed Nursing &rarr;</h3><p>The biggest general board, filtered for nursing.</p></a>
        <a class="tile fade-up" href="https://www.ziprecruiter.com/Jobs/Nurse" target="_blank" rel="noopener"><span class="tag">Fast apply</span><h3>ZipRecruiter &rarr;</h3><p>One-click applications and salary insights.</p></a>
        <a class="tile fade-up" href="https://www.travelnursesource.com" target="_blank" rel="noopener"><span class="tag">Travel</span><h3>Travel Nurse Source &rarr;</h3><p>Travel-only listings across all 50 states.</p></a>
        <a class="tile fade-up" href="https://www.linkedin.com/jobs/nurse-jobs" target="_blank" rel="noopener"><span class="tag">Network</span><h3>LinkedIn &rarr;</h3><p>Roles plus the recruiters behind them.</p></a>
        <a class="tile fade-up" href="https://www.usajobs.gov/Search/Results?k=nurse" target="_blank" rel="noopener"><span class="tag">Federal</span><h3>USAJobs &rarr;</h3><p>VA, military and federal nursing positions.</p></a>
      </div>
    </div>
  </main>
""", "")

PAGES["blog.html"] = ("Blog — Must Love Scrubs",
    "News, study tips, and nurse life from Must Love Scrubs.",
    page_hero('The <span class="hl on-dark">MLS</span> Blog.', "Study science, nurse life, and ecosystem news — written for people who chart for a living.")
    + """  <main class="content-block">
    <div class="wrap tile-grid cols-3">
      <article class="tile fade-up"><span class="tag">Study science</span><h3>Why cramming fails nurses (and what works instead)</h3><p>Spaced repetition, active recall, and the 2-week rule — the memory science behind our courses. Coming soon.</p></article>
      <article class="tile fade-up"><span class="tag">NCLEX</span><h3>NGN questions, decoded</h3><p>How Next-Gen NCLEX actually measures clinical judgment — and how to practice for it. Coming soon.</p></article>
      <article class="tile fade-up"><span class="tag">Nurse life</span><h3>Night shift survival, from nurses who've done decades</h3><p>Sleep, food, sanity — real strategies from the veterans. Coming soon.</p></article>
      <article class="tile fade-up"><span class="tag">Career</span><h3>Travel nursing in 2026: what's really out there</h3><p>Pay honesty, contract red flags, and where demand is heading. Coming soon.</p></article>
      <article class="tile fade-up"><span class="tag">Esi</span><h3>Building an AI tutor nurses can trust</h3><p>The guardrails, the method, and why Esi teaches instead of answers. Coming soon.</p></article>
      <article class="tile fade-up"><span class="tag">Community</span><h3>Introducing Nurse Spotlight</h3><p>Why we're telling nurses' stories — and how to share yours. Coming soon.</p></article>
    </div>
  </main>
""", "")

PAGES["about.html"] = ("About — Must Love Scrubs",
    "Why Must Love Scrubs exists.",
    simple_prose('Built because nurses deserve <span class="hl on-dark">better</span>.',
        "Most nursing sites are cookie-cutter clones of each other. We set out to build something else entirely.",
        """<h2>The idea</h2>
        <p>Must Love Scrubs is a premium nursing education ecosystem — prep courses built on proven retention science, learning videos with real engagement, an AI tutor named Esi, and a small curated store — all in one seamless, mobile-first home.</p>
        <h2>The method</h2>
        <p>Everything we teach follows one principle: teach nurses how to <em>think</em>, not what to memorize. Spaced repetition, active recall, and clinical-judgment reasoning are woven into every course, quiz, and video.</p>
        <h2>The promise</h2>
        <p>1,400+ nurses have already trained with our courses. This site is the next chapter — the ecosystem of nursing, growing every two weeks.</p>"""))

PAGES["careers.html"] = ("Careers — Must Love Scrubs",
    "Work with Must Love Scrubs.",
    simple_prose('Come build the <span class="hl on-dark">ecosystem</span>.',
        "We're a small team with a big mission.",
        """<h2>Open roles</h2>
        <p>No openings right now — but this page is where they'll appear as we grow. Content writers, nurse educators, and video creators: we'd especially love to hear from you when the time comes.</p>
        <p>Want to be first in line? Say hello at <a href="mailto:hello@mustlovescrubs.com" style="color:var(--coral-500);font-weight:700;">hello@mustlovescrubs.com</a>.</p>"""))

PAGES["help.html"] = ("Help Center — Must Love Scrubs",
    "Answers and help for Must Love Scrubs.",
    simple_prose('How can we <span class="hl on-dark">help</span>?',
        "Quick answers to the most common questions — and humans behind them when you need more.",
        """<h2>Getting started</h2>
        <ul><li>Create a free account on the <a href="join.html" style="color:var(--coral-500);">Join page</a> — no card required.</li>
        <li>Claim your 5 daily points on your <a href="profile.html" style="color:var(--coral-500);">Profile Dashboard</a>.</li>
        <li>Browse <a href="courses.html" style="color:var(--coral-500);">Courses</a> or watch <a href="scrubtv.html" style="color:var(--coral-500);">Scrub TV</a>.</li></ul>
        <h2>Billing &amp; subscriptions</h2>
        <p>Courses are one-time or monthly; Esi is a monthly add-on you can cancel anytime from Settings. Refunds within 7 days of purchase, no questions asked.</p>
        <h2>Still stuck?</h2>
        <p>Visit <a href="support.html" style="color:var(--coral-500);">Support</a> or <a href="contact.html" style="color:var(--coral-500);">Contact us</a> — we answer within one business day.</p>"""))

PAGES["contact.html"] = ("Contact — Must Love Scrubs",
    "Get in touch with Must Love Scrubs.",
    page_hero('Say <span class="hl on-dark">hello</span>.', "Questions, stories, partnerships — we read everything.")
    + """  <main class="content-block">
    <div class="wrap">
      <form class="form-card" onsubmit="alert('Demo only — messaging goes live at launch.');return false;">
        <div class="field"><label for="cname">Name</label><input id="cname" type="text" placeholder="Your name"></div>
        <div class="field"><label for="cemail">Email</label><input id="cemail" type="email" placeholder="you@example.com"></div>
        <div class="field"><label for="cmsg">Message</label><textarea id="cmsg" rows="5" placeholder="What's on your mind?"></textarea></div>
        <button class="btn btn-coral" type="submit">Send message</button>
        <p style="margin-top:1rem;font-size:0.8rem;color:var(--ink-60);">Or email us directly: hello@mustlovescrubs.com</p>
      </form>
    </div>
  </main>
""", "")

PAGES["support.html"] = ("Support — Must Love Scrubs",
    "Support for Must Love Scrubs members.",
    simple_prose('We’ve got your <span class="hl on-dark">back</span>.',
        "Account trouble, billing questions, or something not working right — start here.",
        """<h2>Fastest routes</h2>
        <ul><li><b>Account &amp; login</b> — reset from the sign-in screen, or write us.</li>
        <li><b>Billing</b> — manage subscriptions in <a href="settings.html" style="color:var(--coral-500);">Settings</a>; refunds within 7 days.</li>
        <li><b>Bugs</b> — tell us what happened and on what device; screenshots help.</li></ul>
        <p>Email <a href="mailto:hello@mustlovescrubs.com" style="color:var(--coral-500);font-weight:700;">hello@mustlovescrubs.com</a> — we reply within one business day.</p>"""))

PAGES["settings.html"] = ("Settings — Must Love Scrubs",
    "Manage your Must Love Scrubs account.",
    page_hero('Your <span class="hl on-dark">settings</span>.', "Account, notifications, and subscription management. (Demo — live at launch.)")
    + """  <main class="content-block">
    <div class="wrap tile-grid">
      <div class="tile fade-up"><span class="tag">Account</span><h3>Profile &amp; password</h3><p>Name, email, password, and profile photo. Editable once real accounts launch.</p></div>
      <div class="tile fade-up"><span class="tag">Subscription</span><h3>Courses &amp; Esi</h3><p>View your plan, add or cancel Esi tutoring, and see billing history.</p></div>
      <div class="tile fade-up"><span class="tag">Notifications</span><h3>What we send you</h3><p>New video drops, points reminders, and course updates — all opt-in, all controllable.</p></div>
      <div class="tile fade-up"><span class="tag">Privacy</span><h3>Your data</h3><p>Download or delete your data anytime. See our <a href="privacy.html" style="color:var(--coral-500);">Privacy Policy</a>.</p></div>
    </div>
  </main>
""", "")

PAGES["search.html"] = ("Search — Must Love Scrubs",
    "Search Must Love Scrubs.",
    page_hero('Find <span class="hl on-dark">anything</span>.', "Courses, videos, downloads, stories — one search box for the whole ecosystem.",
        """<form class="hero-cta" style="margin-top:1.8rem;gap:0.6rem;max-width:520px;" onsubmit="return false;">
          <input type="search" placeholder="Try &quot;pharmacology&quot; or &quot;brain sheet&quot;" aria-label="Search" style="flex:1;min-width:200px;padding:0.9rem 1.3rem;border-radius:999px;border:none;font:inherit;font-size:0.95rem;">
          <button class="btn btn-coral" type="submit">Search</button>
        </form>""")
    + """  <main class="content-block">
    <div class="wrap prose"><p>Search goes live with real content at launch. Meanwhile, jump straight to <a href="courses.html" style="color:var(--coral-500);font-weight:700;">Courses</a>, <a href="scrubtv.html" style="color:var(--coral-500);font-weight:700;">Scrub TV</a>, or the <a href="store.html" style="color:var(--coral-500);font-weight:700;">Store</a>.</p></div>
  </main>
""", "")

PAGES["notifications.html"] = ("Notifications — Must Love Scrubs",
    "Your Must Love Scrubs notifications.",
    page_hero('Your <span class="hl on-dark">notifications</span>.', "Everything new since your last visit. (Sample items until launch.)")
    + """  <main class="content-block">
    <div class="wrap tile-grid">
      <div class="tile fade-up"><span class="tag">Scrub TV</span><h3>New drop: Triage in 90 seconds</h3><p>A fresh ER/Trauma video just landed — quiz attached, 25 points on the table.</p></div>
      <div class="tile fade-up"><span class="tag">Points</span><h3>Your daily 5 are waiting</h3><p>Claim today's points on your dashboard before midnight.</p></div>
      <div class="tile fade-up"><span class="tag">Courses</span><h3>NCLEX Complete: new NGN case set</h3><p>Twelve new clinical-judgment cases were added this week.</p></div>
    </div>
  </main>
""", "")

PAGES["join.html"] = ("Create your free account — Must Love Scrubs",
    "Join Must Love Scrubs free: daily points, progress tracking, and more.",
    page_hero('Join the <span class="hl on-dark">community</span>.', "Free forever. Daily points. No card required.")
    + """  <main class="content-block">
    <div class="wrap">
      <form class="form-card" onsubmit="alert('Demo only — real accounts arrive with our backend launch.');return false;">
        <div class="field"><label for="jname">Name</label><input id="jname" type="text" placeholder="Your name"></div>
        <div class="field"><label for="jemail">Email</label><input id="jemail" type="email" placeholder="you@example.com"></div>
        <div class="field"><label for="jpass">Password</label><input id="jpass" type="password" placeholder="Create a password"></div>
        <button class="btn btn-coral" type="submit" style="width:100%;">Create my free account</button>
        <p style="margin-top:1rem;font-size:0.78rem;color:var(--ink-60);">By joining you agree to our <a href="terms.html" style="color:var(--coral-500);">Terms</a> and <a href="privacy.html" style="color:var(--coral-500);">Privacy Policy</a>.</p>
      </form>
    </div>
  </main>
""", "")

PAGES["profile.html"] = ("Profile Dashboard — Must Love Scrubs",
    "Your progress, points, quiz history, and certificates.",
    page_hero('Your <span class="hl on-dark">dashboard</span>.', "Progress, points, history, certificates — the whole journey in one place. (Demo data until real accounts launch.)")
    + f"""  <main class="content-block">
    <div class="wrap dash-grid">
      <div class="tile points-card fade-up">
        <span class="tag" style="color:var(--indigo-950);opacity:0.7;">Points balance</span>
        <div class="balance"><span data-points-balance>0</span> pts</div>
        <p style="margin:0.3rem 0 1rem;font-size:0.85rem;">Claim 10 free points every day you visit.</p>
        <button class="btn btn-dark" data-claim-daily>Claim today's 10 points</button>
      </div>
      <div class="tile span2 fade-up">
        <span class="tag">Course progress</span>
        <h3>NCLEX Complete</h3>
        <p style="margin-top:0.8rem;">Unit 4 of 12 · Pharmacology</p>
        <div class="progress-bar"><i style="width:34%;"></i></div>
        <p style="margin-top:1.2rem;">Med-Surg Essentials</p>
        <div class="progress-bar"><i style="width:12%;"></i></div>
      </div>
      <div class="tile fade-up"><span class="tag">Quiz history</span><h3>Latest scores</h3><p>Beta blockers quiz — 8/10<br>Triage priorities — 9/10<br>Decels decoded — 7/10</p></div>
      <div class="tile fade-up"><span class="tag">Certificates</span><h3>Earned</h3><p>Your completion certificates will collect here — downloadable and shareable.</p></div>
      <div class="tile fade-up" style="background:linear-gradient(150deg,var(--indigo-950),var(--indigo-700));color:#fff;">
        <span class="tag" style="color:var(--gold-400);">Question of the Day</span>
        <h3 style="color:#fff;">🔥 12-day streak</h3>
        <p style="color:rgba(255,255,255,0.82);">A fresh NGN question every morning, on your phone or email. Keep the streak alive.</p>
        <a class="btn btn-coral" href="nclex-complete.html#pricing" style="margin-top:0.9rem;">Today's question &rarr;</a>
      </div>
      <div class="tile span2 fade-up" data-downloads>
        <div style="display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap;"><span class="tag">My downloads</span><span class="badge-new" data-dl-badge hidden><span class="spark"></span> Updated &middot; free</span></div>
        <h3>Nurses Index</h3>
        <div data-dl-owned hidden>
          <div class="update-card" style="margin-top:0.8rem;">
            <div class="uc-body">
              <b>Nurses Index <span data-dl-ver>Core Release 2</span></b>
              <p data-dl-msg>You own this. It's yours for life — every future expansion lands here free, automatically.</p>
              <span class="uc-ver" data-dl-note></span>
            </div>
            <a class="btn btn-glow" href="dictionary.html#download" data-dl-get>Open latest version</a>
          </div>
        </div>
        <div data-dl-unowned>
          <p style="margin-top:0.6rem;">You don't own the download yet. Buy it once for $4.99 (or unlock with points) — then every future expansion is <b>free forever</b>, with the new words waiting right here.</p>
          <div class="hero-cta" style="margin-top:1rem;"><a class="btn btn-coral" href="dictionary.html#download">Get the Nurses Index</a><button class="btn btn-line" data-dl-demo>Unlock (demo)</button></div>
        </div>
      </div>
      <div class="tile fade-up"><span class="tag">Saved</span><h3>Your library</h3><p>Saved videos, courses, and downloads live here for quick return.</p></div>
      <div class="tile span2 fade-up"><span class="tag">Esi recommends</span><h3>Tonight's 20 minutes</h3><p>“Your cardiac pharm misses cluster around beta blockers vs. calcium channel blockers. Watch the 6-minute refresher, then take the 10-question drill — I'll re-test you Thursday.” — Esi</p></div>
      <div class="tile fade-up"><span class="tag">Settings</span><h3>Manage account</h3><p><a href="settings.html" style="color:var(--coral-500);font-weight:700;">Account, billing &amp; notifications &rarr;</a></p></div>
    </div>
  </main>
""", "profile")

PAGES["privacy.html"] = ("Privacy Policy (Draft) — Must Love Scrubs",
    "Draft privacy policy for Must Love Scrubs.",
    simple_prose('Privacy <span class="hl on-dark">Policy</span>.', "How we collect, use, and protect your information.",
        """<h2>1. What we collect</h2>
        <p>Account details you give us (name, email), learning activity (course progress, quiz results, points), and standard technical data (device, browser, usage analytics).</p>
        <h2>2. How we use it</h2>
        <p>To run your account, track your progress, personalize study recommendations (including Esi's tutoring), process purchases, and improve the service. We do not sell your personal information.</p>
        <h2>3. Payments</h2>
        <p>Payments are processed by Stripe and Shopify; we never store full card numbers.</p>
        <h2>4. Your choices</h2>
        <p>You may access, download, or delete your data at any time by contacting hello@mustlovescrubs.com. You can opt out of marketing emails with one click.</p>
        <h2>5. Security &amp; retention</h2>
        <p>Data is encrypted in transit (SSL/TLS) and stored with reputable cloud providers. We keep data only as long as your account is active or as required by law.</p>
        <h2>6. Children</h2>
        <p>Must Love Scrubs is intended for users 16 and older.</p>
        <h2>7. Contact</h2>
        <p>Questions: hello@mustlovescrubs.com.</p>""", draft=True))

PAGES["terms.html"] = ("Terms of Use (Draft) — Must Love Scrubs",
    "Draft terms of use for Must Love Scrubs.",
    simple_prose('Terms of <span class="hl on-dark">Use</span>.', "The agreement between you and Must Love Scrubs.",
        """<h2>1. The service</h2>
        <p>Must Love Scrubs provides nursing education content: courses, videos, quizzes, digital downloads, and the Esi AI tutor. Content is educational only — it is not medical advice and does not replace clinical training, institutional policy, or professional judgment.</p>
        <h2>2. Accounts &amp; points</h2>
        <p>You are responsible for your account credentials. Points have no cash value, may be modified at any time, and are redeemable only for eligible digital items.</p>
        <h2>3. Purchases &amp; refunds</h2>
        <p>Course purchases are refundable within 7 days. Subscriptions (including Esi) renew monthly and can be cancelled anytime, effective at period end.</p>
        <h2>4. Intellectual property</h2>
        <p>All content, including questions, videos, and downloads, belongs to Must Love Scrubs. Personal, non-commercial use only; no redistribution or scraping.</p>
        <h2>5. Esi</h2>
        <p>Esi is an AI tutor. Her responses are educational, may contain errors, and must not be relied on for patient care decisions. In an emergency, call 911.</p>
        <h2>6. Liability</h2>
        <p>The service is provided “as is.” To the maximum extent permitted by law, our liability is limited to the amount you paid in the previous 12 months.</p>
        <h2>7. Changes</h2>
        <p>We may update these terms; continued use after notice constitutes acceptance. Contact: hello@mustlovescrubs.com.</p>""", draft=True))

# ---------------------------------------------------------------- FREE AUDIO-SCENE COURSE
SCENE_LINES = [
    ("other", "Lab", "Night shift, this is the lab — critical value on your Room 4."),
    ("nurse", "You", "Go ahead, I'm listening."),
    ("other", "Lab", "Potassium is 6.8. Repeat, six-point-eight. Read back, please."),
    ("nurse", "You", "Critical potassium 6.8 on Room 4 — read back confirmed."),
    ("nurse", "You", "<em>Mr. Alvarez, 68, post-op day two. Last round he said his legs felt heavy.</em>"),
    ("nurse", "You", "Mr. Alvarez? Tell me how you're feeling right now."),
    ("other", "Pt", "My heart's... doing a funny flutter. And I'm so weak."),
    ("nurse", "You", "<em>Weakness. Palpitations. A potassium of 6.8. My mind goes straight to his heart.</em>"),
    ("nurse", "You", "I'm getting you on the monitor and grabbing a 12-lead right now. Stay with me."),
    ("nurse", "You", "<em>Don't chase the number. Protect the heart. Then escalate.</em>"),
]

def scene_transcript():
    out = []
    for who, spk, text in SCENE_LINES:
        out.append(f'<div class="line {who}"><span class="spk">{spk}</span><p>{text}</p></div>')
    return "".join(out)

def waveform_bars(n=48):
    return "".join('<i></i>' for _ in range(n))

QUIZ = [
    ("Your patient has a potassium of 6.8, new palpitations, and sudden weakness. What is your priority?",
     [("Document the value and reassess in 30 minutes", 0),
      ("Place him on a cardiac monitor and get a 12-lead ECG", 1),
      ("Encourage potassium-rich foods so he feels stronger", 0),
      ("Ask the family whether the weakness is baseline", 0)],
     "Hyperkalemia is dangerous because of its effect on the <b>heart</b>. Monitoring and an ECG come first &mdash; peaked T waves and lethal arrhythmias can develop fast, long before documentation matters."),
    ("The provider orders IV calcium gluconate. What is its role in hyperkalemia?",
     [("It lowers the potassium level directly", 0),
      ("It stabilizes the cardiac membrane to protect the heart", 1),
      ("It shifts potassium into the cells", 0),
      ("It removes potassium from the body", 0)],
     "Calcium gluconate doesn't lower potassium &mdash; it <b>protects the heart</b> by stabilizing the cardiac membrane, buying time while insulin + D50 shift it and kayexalate or dialysis remove it."),
    ("Which finding would you expect on the ECG of a patient with a potassium of 6.8?",
     [("Peaked T waves", 1),
      ("A prominent U wave", 0),
      ("ST-elevation in two leads", 0),
      ("A shortened PR interval", 0)],
     "Peaked, tented T waves are the classic early sign of <b>high</b> potassium. U waves point the other way &mdash; toward <b>low</b> potassium. Build the pattern: high K&#8314; &rarr; peaked T's."),
    ("What is the normal reference range for serum potassium?",
     [("1.5&ndash;2.5 mEq/L", 0),
      ("3.5&ndash;5.0 mEq/L", 1),
      ("8.5&ndash;10.5 mg/dL", 0),
      ("135&ndash;145 mEq/L", 0)],
     "Normal potassium is <b>3.5&ndash;5.0 mEq/L</b> &mdash; the banana that costs $3.50 to $5.00. 8.5&ndash;10.5 is calcium; 135&ndash;145 is sodium. Knowing the anchors is how you spot a critical value instantly."),
    ("Your patient is started on furosemide (a loop diuretic). Which electrolyte will you watch most closely for a drop?",
     [("Sodium", 0),
      ("Calcium", 0),
      ("Potassium", 1),
      ("Magnesium only", 0)],
     "Loop diuretics waste <b>potassium</b> &mdash; hypokalemia is the classic risk. Watch for muscle weakness, cramps, and U waves on the ECG, and expect the provider to order a potassium supplement."),
    ("A patient's sodium is 118 mEq/L. What are you most concerned about?",
     [("Seizures and altered mental status", 1),
      ("Peaked T waves", 0),
      ("Positive Chvostek sign", 0),
      ("Kussmaul respirations", 0)],
     "Severe hyponatremia (&lt;120) pulls water <b>into brain cells</b> &mdash; cerebral edema causes headache, confusion, and <b>seizures</b>. Neuro checks and safety are the priority; correct sodium slowly to avoid harm."),
    ("A patient's magnesium is 1.2 mg/dL. Which complication are you monitoring for?",
     [("Depressed reflexes and drowsiness", 0),
      ("Cardiac arrhythmias, including torsades de pointes", 1),
      ("Constipation and thirst", 0),
      ("Bradycardia and warm, flushed skin", 0)],
     "<b>Low</b> magnesium destabilizes the heart &mdash; watch for arrhythmias, especially <b>torsades de pointes</b>. (Depressed reflexes and flushing point the other way, toward <b>high</b> magnesium.)"),
    ("A patient with a glucose of 45 mg/dL is confused and diaphoretic. What do you do first?",
     [("Draw a repeat glucose and wait for the result", 0),
      ("Give 15 g of fast-acting carbohydrate", 1),
      ("Administer the next scheduled insulin dose", 0),
      ("Encourage a high-protein snack", 0)],
     "Symptomatic hypoglycemia is an emergency &mdash; <b>treat first</b> with 15 g of fast-acting carb (juice, glucose gel/tabs), then recheck in 15 minutes. Never give insulin or wait when the brain is starving for glucose."),
]

def quiz_cards():
    out = []
    letters = "ABCD"
    for qi, (q, opts, rat) in enumerate(QUIZ, 1):
        obtns = []
        for oi, (text, correct) in enumerate(opts):
            obtns.append(f'<button class="opt" data-correct="{correct}"><span class="k">{letters[oi]}</span><span>{text}</span></button>')
        out.append(f"""<div class="quiz-card" style="margin-bottom:2.5rem;">
          <div class="quiz-head"><span>Clinical quick check</span><span>Question {qi} of {len(QUIZ)}</span></div>
          <p class="quiz-q">{q}</p>
          <div class="opts">{"".join(obtns)}</div>
          <div class="quiz-actions"><button class="btn btn-coral check-btn">Check answer</button><span style="font-size:0.8rem;color:rgba(255,255,255,0.6);">Choose the safest next step.</span></div>
          <div class="rationale"><b>Why:</b><p>{rat}</p></div>
        </div>""")
    return "".join(out)

LAB_REF = [
    ("Potassium", "K&#8314;", "3.5&ndash;5.0 mEq/L", "&lt;2.5 or &gt;6.5", "Banana costs $3.50&ndash;$5.00. High &rarr; peaked T's; low &rarr; U waves.", "c1"),
    ("Sodium", "Na&#8314;", "135&ndash;145 mEq/L", "&lt;120 or &gt;160", "Low &rarr; seizures &amp; confusion (water into the brain).", "c2"),
    ("Calcium", "Ca", "9.0&ndash;10.5 mg/dL", "&lt;7.0 or &gt;12", "Low &rarr; positive Chvostek &amp; Trousseau, tetany.", "c3"),
    ("Magnesium", "Mg", "1.5&ndash;2.5 mg/dL", "&lt;1.0 or &gt;4.0", "Low &rarr; torsades. High &rarr; depressed reflexes.", "c4"),
    ("Glucose", "&#9679;", "70&ndash;110 mg/dL", "&lt;70 or &gt;400", "Symptomatic low? Treat first with 15 g fast carbs.", "c1"),
    ("Creatinine", "Cr", "0.6&ndash;1.2 mg/dL", "&gt;4.0", "Rising Cr = failing kidneys. Hold nephrotoxic meds.", "c2"),
]

def lab_ref_cards():
    out = []
    for name, sym, rng, crit, trick, color in LAB_REF:
        out.append(f"""<div class="ref-card fade-up">
          <div class="ref-top"><span class="ref-sym {color}">{sym}</span><div><b>{name}</b><span class="ref-range">{rng}</span></div></div>
          <div class="ref-crit"><span>Critical</span><b>{crit}</b></div>
          <p class="ref-trick">{trick}</p>
        </div>""")
    return '<div class="ref-grid">' + "".join(out) + '</div>'

SORT = [
    ("K&#8314; 6.8 mEq/L", "Potassium", "high"),
    ("Na&#8314; 118 mEq/L", "Sodium", "low"),
    ("Glucose 45 mg/dL", "Glucose", "low"),
    ("Ca 10.2 mg/dL", "Calcium", "normal"),
    ("Mg 1.2 mg/dL", "Magnesium", "low"),
    ("K&#8314; 3.9 mEq/L", "Potassium", "normal"),
]

def sort_rows():
    out = []
    for val, sub, ans in SORT:
        out.append(f"""<div class="sort-row" data-answer="{ans}">
          <span class="val">{val}<small>{sub}</small></span>
          <span class="sort-btns">
            <button class="sort-btn" data-zone="low">Low</button>
            <button class="sort-btn" data-zone="normal">Normal</button>
            <button class="sort-btn" data-zone="high">High</button>
          </span>
        </div>""")
    return '<div class="sort-list">' + "".join(out) + '</div>'

SATA_CARD = """<div class="quiz-card sata" style="margin-bottom:2.5rem;">
          <div class="quiz-head"><span>Clinical quick check</span><span>Select all that apply</span></div>
          <span class="sata-tag">Next Gen NCLEX &middot; SATA</span>
          <p class="quiz-q">Your patient's potassium is 6.8 mEq/L. Which actions are appropriate right now? Select all that apply.</p>
          <div class="opts">
            <button class="opt" data-correct="1"><span class="box"></span><span>Place the patient on a cardiac monitor</span></button>
            <button class="opt" data-correct="1"><span class="box"></span><span>Hold all oral and IV potassium</span></button>
            <button class="opt" data-correct="1"><span class="box"></span><span>Notify the provider</span></button>
            <button class="opt" data-correct="0"><span class="box"></span><span>Offer a banana for a quick energy boost</span></button>
            <button class="opt" data-correct="1"><span class="box"></span><span>Prepare to give IV calcium gluconate</span></button>
          </div>
          <div class="quiz-actions"><button class="btn btn-coral check-btn">Check answer</button><span style="font-size:0.8rem;color:rgba(255,255,255,0.6);">Pick every correct action.</span></div>
          <div class="rationale"><b>Why:</b><p>Four are right &mdash; monitor the heart, stop all potassium, tell the provider, and anticipate calcium to protect the heart. Offering a banana <b>adds</b> potassium, exactly the wrong move. SATA items are all-or-nothing, so every box counts.</p></div>
        </div>"""

COURSE_BODY = f"""  <div class="page-hero">
    <div class="wrap inner">
      <a href="scrubtv.html" style="color:rgba(255,255,255,0.7);font-size:0.85rem;font-weight:700;">&larr; Back to Scrub TV</a>
      <p class="lesson-kicker" style="margin-top:1.4rem;">ER / Night shift &middot; ~14 min &middot; sorting drill + 9 questions &middot; Free</p>
      <span class="lesson-label" style="color:var(--gold-400);">Scrub TV &middot; Audio Scene &middot; Ep. 01</span>
      <h1 style="margin-top:0.6rem;">When the lab calls at <span class="em">3 a.m.</span></h1>
      <p>A full free lesson on critical lab values. Listen to the scene, learn the six that save lives, then prove it on 8 NCLEX-style questions. This is how the floor really sounds &mdash; and how you learn to think before you touch a textbook.</p>
    </div>
  </div>

  <div class="pattern-strip" aria-hidden="true">
    <div class="run"><span>Don't memorize a list. <em>Build a pattern.</em></span><span>Don't memorize a list. <em>Build a pattern.</em></span><span>Don't memorize a list. <em>Build a pattern.</em></span><span>Don't memorize a list. <em>Build a pattern.</em></span></div>
  </div>

  <section class="scene-band">
    <div class="wrap">
      <div class="section-head fade-up" style="margin-bottom:1.6rem;"><span class="lesson-label">The scene</span><h2 style="color:#fff;">Room 4. Post-op day two.</h2></div>
      <div class="player">
        <div class="player-main fade-up">
          <div class="scene-context"><span class="c">ER &middot; Night shift</span><span class="c">68-year-old male</span><span class="c">Post-op day 2</span></div>
          <div class="play-row">
            <button class="play-btn" aria-label="Play the scene">
              <span class="play-ico">{I['play']}</span>
              <span class="pause-ico"><svg viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg></span>
            </button>
            <div class="waveform" aria-hidden="true">{waveform_bars()}</div>
          </div>
          <div class="time-row"><span class="cur-time">0:00</span><span>6:12</span></div>
          <p class="audio-note">Audio is swap-ready &mdash; real recorded / AI-voiced scene drops in here. Press play to preview the synced experience.</p>
          <div class="unlock-note">{I['check']} Scene complete &middot; quick check unlocked below</div>
        </div>
        <div class="transcript fade-up" aria-label="Transcript">
          {scene_transcript()}
        </div>
      </div>
    </div>
  </section>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="lesson-label">The quick recall</span><h2>Three things to <span class="em">carry with you</span>.</h2><p>Tap a card when you're ready to test what stuck. No passive scrolling here.</p></div>
      <div class="carry-grid">
        <div class="flip fade-up" tabindex="0" role="button" aria-label="Reveal card 1">
          <div class="flip-inner">
            <div class="flip-face flip-front f1"><span class="idx">01</span><span class="tag">Recognize</span><h3>A number is a story.</h3><span class="cue">Tap to reveal &rarr;</span></div>
            <div class="flip-face flip-back"><span class="bk-tag">Recognize</span><p>K&#8314; 6.8 is <b>hyperkalemia</b> (normal 3.5&ndash;5.0). The body's warnings: muscle weakness, palpitations, and on the monitor &mdash; peaked T waves.</p></div>
          </div>
        </div>
        <div class="flip fade-up" tabindex="0" role="button" aria-label="Reveal card 2">
          <div class="flip-inner">
            <div class="flip-face flip-front f2"><span class="idx">02</span><span class="tag">Prioritize</span><h3>Protect the heart first.</h3><span class="cue">Tap to reveal &rarr;</span></div>
            <div class="flip-face flip-back"><span class="bk-tag">Prioritize</span><p>Cardiac stability beats everything. <b>Monitor + 12-lead ECG now.</b> High potassium kills through the heart, not the lab slip.</p></div>
          </div>
        </div>
        <div class="flip fade-up" tabindex="0" role="button" aria-label="Reveal card 3">
          <div class="flip-inner">
            <div class="flip-face flip-front f3"><span class="idx">03</span><span class="tag">Act</span><h3>Stop, check, escalate.</h3><span class="cue">Tap to reveal &rarr;</span></div>
            <div class="flip-face flip-back"><span class="bk-tag">Act</span><p>Hold potassium sources, notify the provider (SBAR), and anticipate: <b>calcium</b> to protect, <b>insulin + D50</b> to shift, <b>kayexalate/dialysis</b> to remove.</p></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="lesson-label">Know your criticals</span><h2>The six that <span class="em">save lives</span>.</h2><p>These are the values you'll act on at 3 a.m. Learn the anchor, spot the danger, know the move.</p></div>
      {lab_ref_cards()}
      <p class="ref-foot fade-up">Ranges vary slightly by lab. Learn the pattern, then confirm against your facility's reference values.</p>
    </div>
  </section>

  <section style="background:var(--card);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="lesson-label" style="color:var(--teal-600);">Sort it &middot; quick drill</span><h2>Low, normal, or <span class="em">high</span>?</h2><p>Tap the zone for each value. Instant feedback &mdash; this is active recall, not a cheat sheet.</p></div>
      {sort_rows()}
    </div>
  </section>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="confidence fade-up">
        <span class="lesson-label" style="color:var(--teal-600);">Confidence check</span>
        <h3 style="margin-top:0.5rem;">How sure are you on the critical potassium value?</h3>
        <input type="range" min="0" max="100" value="50" aria-label="Confidence">
        <div class="conf-scale"><span>Not sure</span><span>Locked in</span></div>
        <button class="btn btn-line conf-btn" style="margin-top:1.2rem;">Reveal the answer</button>
        <div class="conf-reveal">
          <p style="color:var(--ink-60);"><b style="color:var(--ink);">Normal K&#8314; is 3.5&ndash;5.0 mEq/L</b> &mdash; a banana costs $3.50 to $5.00. Above 6.0 is critical: peaked T's, weakness, &ldquo;protect the heart.&rdquo; Below 2.5 is critical too &mdash; cramps and arrhythmias. Rating your own certainty <em>before</em> the reveal is what makes it stick.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="quiz-band" hidden>
    <div class="wrap">
      <div class="section-head fade-up"><span class="lesson-label" style="color:var(--gold-400);">Clinical quick check</span><h2 style="color:#fff;">Now &mdash; <span class="em" style="color:var(--gold-400);">make the call</span>.</h2></div>
      {quiz_cards()}
      {SATA_CARD}

      <div class="result-reveal" hidden>
        <div class="result-card">
          <span class="lesson-label" style="color:var(--teal-600);">Scene complete</span>
          <div class="score"><span data-quiz-score>0/3</span></div>
          <span class="pts-won">{I['star']} <span data-pts-won>points earned</span></span>
          <p class="review">Esi: &ldquo;<b>I'll re-test you in 3 days</b> &mdash; that's right when this starts to fade. Build the pattern, don't cram the list.&rdquo;</p>
          <a class="btn btn-coral" href="join.html" style="margin-top:1.6rem;">Save my progress (free account)</a>
        </div>
        <div style="height:1.2rem;"></div>
        <div class="next-up">
          <span class="ic">{I['er']}</span>
          <div><small>Next scene &middot; ER / Trauma</small><b>Chest pain: what can't wait?</b></div>
          <a class="btn btn-line go" href="scrubtv.html">Listen &rarr;</a>
        </div>
      </div>
    </div>
  </section>

  <section style="background:var(--bg);">
    <div class="wrap" style="text-align:center;">
      <div class="section-head fade-up" style="margin-inline:auto;"><span class="lesson-label">Keep the momentum</span><h2>Small sessions. <span class="em">Serious growth.</span></h2><p style="margin-inline:auto;">This scene is free forever. When you're ready to pass, the full NCLEX bank, mock exams, and Esi drilling your weak spots are one step away.</p></div>
      <a class="btn btn-coral" href="courses.html">See NCLEX Complete</a>
    </div>
  </section>

  <script src="js/course.js"></script>
"""

PAGES["course-lab-values.html"] = ("Free Audio Scene: Critical Lab Values | Must Love Scrubs",
    "A free audio-scene NCLEX lesson: recognize and act on a critical potassium value. Listen, learn the pattern, and test yourself.",
    COURSE_BODY, "scrubtv")

# ---------------------------------------------------------------- NCLEX PREP PAGE
import json as _json
TMR_PROMPTS = [
    {"q": "Normal potassium (K+)?", "a": [{"t": "3.5-5.0", "c": 1}, {"t": "135-145", "c": 0}, {"t": "1.5-2.5", "c": 0}, {"t": "9-10.5", "c": 0}]},
    {"q": "Normal sodium (Na+)?", "a": [{"t": "135-145", "c": 1}, {"t": "3.5-5.0", "c": 0}, {"t": "70-110", "c": 0}, {"t": "12-16", "c": 0}]},
    {"q": "Treat hypoglycemia below?", "a": [{"t": "70 mg/dL", "c": 1}, {"t": "110 mg/dL", "c": 0}, {"t": "140 mg/dL", "c": 0}, {"t": "200 mg/dL", "c": 0}]},
    {"q": "Low magnesium risks...", "a": [{"t": "Torsades", "c": 1}, {"t": "Constipation", "c": 0}, {"t": "Flushing", "c": 0}, {"t": "Bradycardia", "c": 0}]},
    {"q": "Peaked T waves mean...", "a": [{"t": "High K+", "c": 1}, {"t": "Low K+", "c": 0}, {"t": "High Ca", "c": 0}, {"t": "Low Na", "c": 0}]},
    {"q": "Normal calcium (Ca)?", "a": [{"t": "9.0-10.5", "c": 1}, {"t": "3.5-5.0", "c": 0}, {"t": "1.5-2.5", "c": 0}, {"t": "135-145", "c": 0}]},
]
TMR_JSON = _json.dumps(TMR_PROMPTS)

PREP_BODY = f"""  <div class="page-hero">
    <div class="wrap inner">
      <span class="lesson-label" style="color:var(--gold-400);">NCLEX Prep</span>
      <h1 style="margin-top:0.6rem;">Prep that feels like the <span class="em">real test</span>.</h1>
      <p>Every Next Gen NCLEX item type &mdash; timed recall, trends, matrix grids, SBAR, select-all. Choose your exam, start free, unlock the full bank when you're ready.</p>
      <div style="margin-top:1.6rem;display:flex;flex-wrap:wrap;gap:1rem;align-items:center;">
        <div class="segment" role="tablist" aria-label="Choose exam track">
          <button class="on" data-track="rn">NCLEX-RN</button>
          <button data-track="lpn">NCLEX-PN (LPN)</button>
        </div>
        <span class="track-note">You're prepping for the <b class="track-word">RN</b>. Questions adapt to your scope.</span>
      </div>
    </div>
  </div>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="lesson-label">Free to start</span><h2>Two ways in.</h2><p>Sample every item type free. Unlock the full <span class="track-word">RN</span> bank, timed mocks, and analytics when it's crunch time.</p></div>
      <div class="tier-compare">
        <div class="tier-col fade-up">
          <div class="tname">Free practice</div>
          <div class="tprice">$0 forever</div>
          <ul>
            <li>{I['check']} Every NGN item type to try</li>
            <li>{I['check']} A live sample from the <span class="track-word">RN</span> bank</li>
            <li>{I['check']} Daily points &amp; streaks</li>
            <li>{I['check']} Scrub TV audio scenes</li>
          </ul>
          <a class="btn btn-line" href="course-lab-values.html">Try a free scene</a>
        </div>
        <div class="tier-col paid fade-up">
          <div class="tname">NCLEX Complete</div>
          <div class="tprice">Plans from $59 &middot; Esi included</div>
          <ul>
            <li>{I['check']} 2,600+ questions, <span class="track-word">RN</span> &amp; LPN tracks</li>
            <li>{I['check']} 50 case studies + 4 readiness exams</li>
            <li>{I['check']} Study schedule, tagging &amp; the workbook</li>
            <li>{I['check']} Weak-area analytics + Esi tutoring</li>
          </ul>
          <a class="btn btn-coral" href="nclex-complete.html">See NCLEX Complete &rarr;</a>
          <a class="relock" href="#unlock" data-unlock style="display:block;margin-top:0.6rem;">Or feel the paid side right here &rarr;</a>
        </div>
      </div>
    </div>
  </section>

  <section style="background:var(--card);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="lesson-label">Item type 1</span><h2>Timed memory round.</h2><p>Rapid recall against the clock &mdash; speed is how you know it's automatic.</p></div>
      <div class="widget timed-round fade-up" data-prompts='{TMR_JSON}'>
        <div class="tmr-intro">
          <span class="widget-tag">{I['star']} Beat your streak</span>
          <p class="prompt" style="margin-bottom:1.4rem;">Six lab-value prompts. ~8 seconds each. Answer fast, keep the streak alive.</p>
          <button class="btn btn-coral tmr-start">Start the round</button>
        </div>
        <div class="tmr-body" hidden>
          <div class="tmr-meta"><span class="tmr-idx">1 / 6</span><span class="streak">Streak: <span class="tmr-streak">0</span></span></div>
          <div class="timer-bar"><i></i></div>
          <p class="prompt"></p>
          <div class="choice-grid"></div>
        </div>
      </div>
    </div>
  </section>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="lesson-label">Item type 2</span><h2>Chart &amp; trend.</h2><p>Read the story across the vitals. NGN wants to know you can see it coming.</p></div>
      <div class="widget mc-item fade-up">
        <span class="widget-tag">Trend item</span>
        <p class="prompt">Your post-op patient's vitals over 8 hours. What is your priority interpretation?</p>
        <div class="trend-scroll">
          <table class="trend-table">
            <thead><tr><th>Time</th><th>HR</th><th>BP</th><th>Temp &deg;C</th><th>RR</th><th>SpO&#8322;</th></tr></thead>
            <tbody>
              <tr><td>08:00</td><td>88</td><td>122/78</td><td>37.0</td><td>16</td><td>98%</td></tr>
              <tr><td>12:00</td><td>104</td><td>108/66</td><td>38.4</td><td>22</td><td>95%</td></tr>
              <tr><td>16:00</td><td class="flag">122</td><td class="flag">94/54</td><td class="flag">39.1</td><td class="flag">28</td><td class="flag">91%</td></tr>
            </tbody>
          </table>
        </div>
        <div class="choice-grid" style="grid-template-columns:1fr;">
          <button class="choice" data-correct="1">Rising HR/RR/temp with falling BP &amp; SpO&#8322; &mdash; early sepsis. Escalate now.</button>
          <button class="choice" data-correct="0">Expected post-op recovery &mdash; continue routine monitoring.</button>
          <button class="choice" data-correct="0">Anxiety &mdash; offer reassurance and reassess in an hour.</button>
          <button class="choice" data-correct="0">Mild dehydration &mdash; encourage oral fluids.</button>
        </div>
        <div class="quiz-actions" style="margin-top:1.2rem;"><button class="btn btn-coral mc-check">Check answer</button></div>
        <div class="rationale" style="background:var(--bg);border-left:3px solid var(--teal-600);color:var(--ink);"><b style="color:var(--teal-600);">Why:</b><p style="color:var(--ink-60);">Trending up in HR, RR, and temp while BP and SpO&#8322; fall is the classic <b>deterioration / sepsis</b> pattern (SIRS). The individual numbers matter less than the direction &mdash; recognize it early and escalate.</p></div>
      </div>
    </div>
  </section>

  <section style="background:var(--card);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="lesson-label">Item type 3</span><h2>Matrix / grid.</h2><p><span data-rn="For each finding, decide: expected, or does it need you to act?" data-lpn="For each finding, decide: expected, or report to the RN?">For each finding, decide: expected, or does it need you to act?</span></p></div>
      <div class="widget matrix-item fade-up">
        <span class="widget-tag">Matrix item</span>
        <div class="matrix-scroll">
          <table class="matrix">
            <thead><tr><th>Post-op finding</th><th>Expected</th><th data-rn="Act / notify" data-lpn="Report to RN">Act / notify</th></tr></thead>
            <tbody>
              <tr data-answer="exp"><td>Temp 38.0&deg;C at 12 hours</td><td class="mcell"><button data-col="exp" aria-label="expected"></button></td><td class="mcell"><button data-col="rep" aria-label="act"></button></td></tr>
              <tr data-answer="rep"><td>Urine output 20 mL/hr for 2 hours</td><td class="mcell"><button data-col="exp"></button></td><td class="mcell"><button data-col="rep"></button></td></tr>
              <tr data-answer="exp"><td>Pain 4/10, steadily improving</td><td class="mcell"><button data-col="exp"></button></td><td class="mcell"><button data-col="rep"></button></td></tr>
              <tr data-answer="rep"><td>New confusion with HR 122</td><td class="mcell"><button data-col="exp"></button></td><td class="mcell"><button data-col="rep"></button></td></tr>
              <tr data-answer="exp"><td>Incision pink, edges approximated</td><td class="mcell"><button data-col="exp"></button></td><td class="mcell"><button data-col="rep"></button></td></tr>
            </tbody>
          </table>
        </div>
        <div class="quiz-actions" style="margin-top:1.2rem;"><button class="btn btn-coral matrix-check">Check the grid</button><span class="matrix-result" hidden style="font-weight:800;color:var(--teal-600);"><b></b></span></div>
      </div>
    </div>
  </section>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="lesson-label">Item type 4</span><h2>Build the SBAR.</h2><p>You're calling the provider about the potassium patient. Put each line where it belongs.</p></div>
      <div class="widget sbar fade-up">
        <span class="widget-tag">SBAR builder</span>
        <div class="sbar-grid">
          <div class="sbar-slot" data-answer="s"><span class="lab">S<b>Situation</b></span></div>
          <div class="sbar-slot" data-answer="b"><span class="lab">B<b>Background</b></span></div>
          <div class="sbar-slot" data-answer="a"><span class="lab">A<b>Assessment</b></span></div>
          <div class="sbar-slot" data-answer="r"><span class="lab">R<b>Recommendation</b></span></div>
        </div>
        <p style="font-size:0.8rem;color:var(--ink-60);margin-bottom:0.7rem;">Tap a line, then tap its slot.</p>
        <div class="chip-pool">
          <button class="sbar-chip" data-id="a">I'm concerned about a cardiac arrhythmia from hyperkalemia.</button>
          <button class="sbar-chip" data-id="r">Please come assess and consider IV calcium gluconate.</button>
          <button class="sbar-chip" data-id="s">Mr. Alvarez in Room 4 has new palpitations and weakness.</button>
          <button class="sbar-chip" data-id="b">He's post-op day 2; his potassium just resulted at 6.8.</button>
        </div>
        <div class="quiz-actions" style="margin-top:1.3rem;"><button class="btn btn-coral sbar-check">Check my SBAR</button><span class="sbar-result" hidden style="font-weight:800;color:var(--teal-600);"><b></b></span></div>
      </div>
    </div>
  </section>

  <section id="unlock" style="background:var(--card);">
    <div class="wrap">
      <div class="gate fade-up">
        <div class="lock-ic">{I['lock']}</div>
        <h3>That's the free sample.</h3>
        <p>You've tried every item type. The full <span class="track-word">RN</span> bank has <b>2,600+ questions</b>, 50 case studies, 4 readiness exams, timed mocks, weak-area analytics, and Esi drilling exactly what you miss.</p>
        <a class="btn btn-coral" href="#" data-unlock>Unlock NCLEX Complete &mdash; from $59 (demo)</a>
        <a class="relock" href="#" data-unlock>Just let me feel the paid side &rarr;</a>
      </div>

      <div class="paid-only">
        <div class="pro-band fade-up">
          <span class="pro-badge">{I['star']} NCLEX Complete &middot; Unlocked</span>
          <h2>Welcome to the full <span class="track-word">RN</span> bank.</h2>
          <p class="sub">This is the paid side &mdash; and it should feel like it. Deeper than anything out there: thousands of questions, real mocks, live analytics, and Esi drilling your exact weak spots.</p>
          <div class="pro-grid">
            <div class="pro-tile">
              <span class="pi">{I['book']}</span>
              <div class="big-n">2,140</div>
              <b><span class="track-word">RN</span> questions</b>
              <p>Every NGN type, filterable by clinical area, full rationales on every option.</p>
            </div>
            <div class="pro-tile">
              <span class="pi">{I['play']}</span>
              <div class="big-n">CAT</div>
              <b>Real-format mocks</b>
              <p>75&ndash;145 item computer-adaptive mock exams that end when you're ready.</p>
            </div>
            <div class="pro-tile">
              <span class="pi">{I['shield']}</span>
              <b>Weak-area analytics</b>
              <div class="pro-bars">
                <div class="pro-bar"><span>Pharm</span><span class="track"><i style="width:58%"></i></span><span>58%</span></div>
                <div class="pro-bar"><span>Cardiac</span><span class="track"><i style="width:82%"></i></span><span>82%</span></div>
                <div class="pro-bar"><span>Peds</span><span class="track"><i style="width:41%"></i></span><span>41%</span></div>
                <div class="pro-bar"><span>Safety</span><span class="track"><i style="width:74%"></i></span><span>74%</span></div>
              </div>
            </div>
            <div class="pro-tile">
              <span class="pi"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M9 10a3 3 0 1 1 4 2.8V15"/><circle cx="12" cy="18" r="0.6" fill="currentColor"/></svg></span>
              <b>Esi tutoring</b>
              <p>Your AI tutor turns every miss into a targeted drill and a spaced-review plan. Nobody else has her.</p>
            </div>
          </div>
          <div class="pro-launch">
            <div class="pass-ring"><b>87%</b></div>
            <div class="txt"><b>Your pass probability: 87%</b><p>Take a full timed mock and watch it climb. 75 questions, real format, scored instantly. (Demo &mdash; runner lands in Phase 2.)</p></div>
            <a class="btn btn-coral" href="#">Start a 75-question mock</a>
          </div>
          <p style="text-align:center;margin-top:1.6rem;"><a class="relock" href="#" data-relock style="color:rgba(255,255,255,0.55);text-decoration:underline;font-size:0.8rem;">Relock to feel the free side again</a></p>
        </div>
      </div>
    </div>
  </section>

  <script src="js/prep.js"></script>
"""

PAGES["nclex.html"] = ("NCLEX Prep (RN &amp; LPN) — Must Love Scrubs",
    "Free NCLEX practice with every Next Gen item type: timed recall, chart-trend, matrix grid, SBAR builder, and select-all. RN and LPN tracks.",
    PREP_BODY, "courses")

# ---------------------------------------------------------------- NCLEX COMPLETE (flagship product page)

# Custom inline icons (sized by CSS) for this page
IC_STACK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 3 8l9 5 9-5-9-5z"/><path d="M3 13l9 5 9-5"/></svg>'
IC_CASE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="5" width="16" height="15" rx="2.5"/><path d="M8 3v4M16 3v4M4 10h16M8 14h5M8 17h8"/></svg>'
IC_ROUTE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="6" r="2.5"/><path d="M8.5 17.5 15 8m1 8h1a3 3 0 0 0 0-6h-6a3 3 0 0 1 0-6H8"/></svg>'
IC_GAUGE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 18a8 8 0 1 1 16 0"/><path d="m12 14 4-4"/><circle cx="12" cy="14" r="1.4" fill="currentColor"/></svg>'
IC_USERS = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.5"/><path d="M3 20c0-3.3 2.7-5.5 6-5.5s6 2.2 6 5.5"/><path d="M16 5.2a3.5 3.5 0 0 1 0 5.6M18 20c0-2.4-1-4.3-2.6-5.2"/></svg>'
IC_CAL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3.5" y="5" width="17" height="16" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg>'

COMPLETE_BODY = f"""  <div class="page-hero">
    <div class="wrap inner">
      <span class="lesson-label" style="color:var(--gold-400);">The flagship &middot; NCLEX Complete</span>
      <h1 style="margin-top:0.6rem;">Everything you need to pass. <span class="em">Nothing you don't.</span></h1>
      <p>Four ways to master the Next Gen NCLEX &mdash; case studies, a deep question bank, a strategy course, and full-length readiness exams that predict your pass chance &mdash; wrapped in a plan built around your test date. Esi, your AI tutor, comes with every plan.</p>
      <div class="hero-cta" style="margin-top:1.8rem;">
        <a class="btn btn-coral" href="#pricing">See plans &mdash; from $59</a>
        <a class="btn btn-ghost" href="nclex.html">Try the free practice</a>
      </div>
      <div class="chip-row" style="margin-top:1.4rem;justify-content:center;">
        <span class="chip gold">Esi AI tutor included</span>
        <span class="chip teal">Pass Guarantee</span>
        <span class="chip">100% original content</span>
      </div>
    </div>
  </div>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="eyebrow teal">Four ways to prep</span><h2>The complete system, <span class="hl">not a pile of questions.</span></h2><p>Most sites hand you a giant question bank and wish you luck. NCLEX Complete teaches you to <b>think like a nurse</b> from four angles &mdash; then proves you're ready.</p></div>
      <div class="pillar-grid">
        <div class="pillar fade-up">
          <div class="illo" style="background:linear-gradient(140deg,#8b5cff,#4d2b9e);">{IC_CASE}</div>
          <span class="kick">Learn the reasoning</span>
          <div class="stat">50</div>
          <h3>Next Gen case studies</h3>
          <p>Full unfolding cases with a step-by-step expert walkthrough for each &mdash; exactly how the new NCLEX tests clinical judgment. Watch how an expert reasons through the bow-tie, then try it yourself.</p>
        </div>
        <div class="pillar fade-up">
          <div class="illo" style="background:linear-gradient(140deg,#2ad4c4,#1a0942);">{IC_STACK}</div>
          <span class="kick">Build the reps</span>
          <div class="stat">2,600+</div>
          <h3>Standalone questions</h3>
          <p>Original NCLEX-style questions across every clinical area &mdash; MC, select-all, matrix, trend, ordered response and more. Every option carries a full rationale, not just a right answer. <a href="qbank.html" style="color:var(--coral-500);font-weight:700;">Try the bank free &rarr;</a></p>
        </div>
        <div class="pillar fade-up">
          <div class="illo" style="background:linear-gradient(140deg,#ffc23d,#8b5cff);">{I['play']}</div>
          <span class="kick">Learn the strategy</span>
          <div class="stat">NGN</div>
          <h3>Strategy video course</h3>
          <p>A short, sharp course on how to <i>approach</i> Next Gen items &mdash; how to read a case, spot the answer type, and avoid the traps the test is built on. Strategy is the difference between knowing and passing.</p>
        </div>
        <div class="pillar fade-up">
          <div class="illo" style="background:linear-gradient(140deg,#e5484d,#7a45f0);">{IC_GAUGE}</div>
          <span class="kick">Prove you're ready</span>
          <div class="stat">4</div>
          <h3>Full-length readiness exams</h3>
          <p>Four computer-adaptive practice exams in real test format. Each one predicts your pass chance &mdash; Low, Borderline, High, or Very High &mdash; and shows the exact subjects holding you back.</p>
        </div>
      </div>
    </div>
  </section>

  <section style="background:var(--card);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="eyebrow">Readiness</span><h2>Know your pass chance <span class="hl">before test day.</span></h2><p>After each readiness exam, you get a single honest read on where you stand &mdash; and what to fix next.</p></div>
      <div class="cat-explain fade-up">
        <h3 style="margin-bottom:0.4rem;">Your readiness after Exam 2</h3>
        <p style="margin-bottom:1.4rem;">Based on 145 adaptive items across every category.</p>
        <div class="readiness" data-readiness="3">
          <div class="rd-track"><div class="rd-seg s1"></div><div class="rd-seg s2"></div><div class="rd-seg s3"></div><div class="rd-seg s4"></div></div>
          <div class="rd-labels"><span data-rd="1">Low</span><span data-rd="2">Borderline</span><span data-rd="3" class="cur">High</span><span data-rd="4">Very High</span></div>
        </div>
        <p style="margin-top:1.3rem;"><b style="color:var(--teal-400);">You're tracking High.</b> Two more focused sessions on your weakest areas and you'll be Very High. Esi has already queued them.</p>
      </div>
    </div>
  </section>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="eyebrow teal">What's a CAT?</span><h2>The real NCLEX <span class="hl">adapts to you.</span></h2><p>The NCLEX is a Computer Adaptive Test &mdash; it changes difficulty based on how you answer. Our readiness exams work the same way, so test day feels familiar.</p></div>
      <div class="cat-explain fade-up">
        <div class="cat-steps">
          <div class="cat-step"><b>1 &middot; It reacts</b><p>Answer correctly and the next question gets harder. Miss one and it eases off &mdash; constantly zeroing in on your true ability.</p></div>
          <div class="cat-step"><b>2 &middot; It's not fixed-length</b><p>The exam can end anywhere from 75 to 145 questions &mdash; it stops the moment it's confident you're above (or below) the passing line.</p></div>
          <div class="cat-step"><b>3 &middot; We mirror it</b><p>Practicing on a real adaptive engine means no surprises. You'll have already felt the format four times before it counts.</p></div>
        </div>
      </div>
    </div>
  </section>

  <section style="background:var(--card);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="eyebrow gold">Study schedule</span><h2>A day-by-day plan, <span class="hl">built around your test date.</span></h2><p>Tell us when you test and how much time you have &mdash; we build the calendar, complete with review days and readiness checkpoints baked in.</p></div>
      <div class="sched-grid">
        <div class="sched fade-up">
          <span class="rec">Fast track</span>
          <div class="len">1 Month</div>
          <div class="hrs">3&ndash;4 hrs/day &middot; 6 days/week</div>
          <ul>
            <li>{I['check']} Great if you have a solid foundation and just need practice</li>
            <li>{I['check']} Daily case study + standalone set</li>
            <li>{I['check']} Readiness Exam at weeks 2 and 4</li>
            <li>{I['check']} Built-in review days so nothing slips</li>
          </ul>
        </div>
        <div class="sched hot fade-up">
          <span class="rec">Most students</span>
          <div class="len">2 Months</div>
          <div class="hrs">~2 hrs/day &middot; 5 days/week</div>
          <ul>
            <li>{I['check']} The ideal timeline for most test-takers</li>
            <li>{I['check']} Concept days, practice days, and review days</li>
            <li>{I['check']} All 4 readiness exams spaced across the plan</li>
            <li>{I['check']} Weak-area drills auto-scheduled by Esi</li>
          </ul>
        </div>
        <div class="sched fade-up">
          <span class="rec">Full-time workers</span>
          <div class="len">3 Months</div>
          <div class="hrs">1&ndash;2 hrs/day &middot; 5 days/week</div>
          <ul>
            <li>{I['check']} Right if you work full-time or need to rebuild basics</li>
            <li>{I['check']} Gentler daily load, same total coverage</li>
            <li>{I['check']} Extra concept teaching before practice</li>
            <li>{I['check']} Readiness checkpoints every few weeks</li>
          </ul>
        </div>
      </div>

      <div class="section-head fade-up" style="margin-top:3rem;"><span class="eyebrow">Not sure?</span><h2>Which plan is <span class="hl">right for you?</span></h2><p>Answer three quick questions and we'll point you to the 1-, 2-, or 3-month plan.</p></div>
      <div class="squiz fade-up" data-squiz>
        <div class="sq-progress"><i style="width:33%;"></i></div>
        <div class="q" data-step="1">
          <span class="qnum">Question 1 of 3</span>
          <h4>When is your NCLEX test date?</h4>
          <div class="opts">
            <button class="opt" data-score="1">In about a month or less</button>
            <button class="opt" data-score="2">Roughly two months out</button>
            <button class="opt" data-score="3">Three months or more &mdash; or not booked yet</button>
          </div>
        </div>
        <div class="q" data-step="2">
          <span class="qnum">Question 2 of 3</span>
          <h4>How much can you realistically study each day?</h4>
          <div class="opts">
            <button class="opt" data-score="1">3&ndash;4 focused hours</button>
            <button class="opt" data-score="2">About 2 hours</button>
            <button class="opt" data-score="3">An hour or so &mdash; I work or have family</button>
          </div>
        </div>
        <div class="q" data-step="3">
          <span class="qnum">Question 3 of 3</span>
          <h4>How solid do your fundamentals feel right now?</h4>
          <div class="opts">
            <button class="opt" data-score="1">Strong &mdash; I mostly need reps and timing</button>
            <button class="opt" data-score="2">Okay &mdash; some shaky areas to firm up</button>
            <button class="opt" data-score="3">Rusty &mdash; I want to rebuild from the ground up</button>
          </div>
        </div>
        <div class="sq-result">
          <span class="qnum">Your match</span>
          <div class="big" data-sq-plan>2-Month Plan</div>
          <p data-sq-note>Enough runway to fix weak areas without cramming &mdash; the sweet spot for most students.</p>
          <a class="btn btn-coral" href="#pricing">See the matching plan</a>
          <div><button class="btn btn-line" data-sq-restart style="margin-top:0.8rem;">Retake the quiz</button></div>
        </div>
      </div>
    </div>
  </section>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="eyebrow teal">Track every item</span><h2>Tag it. Master it. <span class="hl">Watch it move.</span></h2><p>Flag any question as Mastered, Reviewing, or Learning &mdash; then see your whole exam roll up by subject area, so you always know where to spend the next hour.</p></div>
      <div class="widget fade-up" style="max-width:720px;margin:0 auto;">
        <span class="widget-tag">{I['star']} Tag this question</span>
        <p class="prompt" style="margin-bottom:0.4rem;">A client with heart failure gains 3 lb in two days. What is the nurse's priority action?</p>
        <div class="tag-chips" data-tagset>
          <button class="tagc mastered" data-tag="mastered">Mastered</button>
          <button class="tagc reviewing" data-tag="reviewing">Reviewing</button>
          <button class="tagc learning" data-tag="learning">Learning</button>
        </div>
        <p data-tag-note style="font-size:0.82rem;color:var(--ink-60);margin-top:0.7rem;">Tap a tag &mdash; it files the question into your dashboard for smart review.</p>
      </div>

      <div class="section-head fade-up" style="margin-top:3rem;"><span class="eyebrow">Performance by subject area</span><h2>Your weak spots, <span class="hl">in plain sight.</span></h2></div>
      <div class="subj-grid fade-up" style="margin-left:auto;margin-right:auto;">
        <div class="subj"><span class="lab">Adult Health</span><span class="track"><i class="hi" style="width:82%;"></i></span><span class="pct">82%</span></div>
        <div class="subj"><span class="lab">Pharmacology</span><span class="track"><i class="lo" style="width:44%;"></i></span><span class="pct">44%</span></div>
        <div class="subj"><span class="lab">Mental Health</span><span class="track"><i class="hi" style="width:78%;"></i></span><span class="pct">78%</span></div>
        <div class="subj"><span class="lab">Maternal / Newborn</span><span class="track"><i class="mid" style="width:63%;"></i></span><span class="pct">63%</span></div>
        <div class="subj"><span class="lab">Safety &amp; Infection</span><span class="track"><i class="hi" style="width:88%;"></i></span><span class="pct">88%</span></div>
        <div class="subj"><span class="lab">Pediatrics</span><span class="track"><i class="mid" style="width:57%;"></i></span><span class="pct">57%</span></div>
      </div>
    </div>
  </section>

  <section style="background:var(--card);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="eyebrow gold">Question of the Day</span><h2>One question, <span class="hl">every morning.</span></h2><p>A fresh NGN-style question lands on your phone or in your inbox daily &mdash; keep the streak, keep it sharp.</p></div>
      <div class="qotd fade-up" data-qotd style="max-width:640px;margin:0 auto;">
        <span class="qk">Today's question</span>
        <h3>Clinical Judgment</h3>
        <p class="stem">A nurse is caring for a client receiving IV heparin. Which laboratory value is the <b>priority</b> to monitor?</p>
        <div class="qopts">
          <button class="qo" data-correct="0">Serum potassium</button>
          <button class="qo" data-correct="1">Activated partial thromboplastin time (aPTT)</button>
          <button class="qo" data-correct="0">Blood urea nitrogen (BUN)</button>
          <button class="qo" data-correct="0">Serum glucose</button>
        </div>
        <div class="qrat"><b style="color:var(--teal-400);">Correct: aPTT.</b> Heparin's effect is monitored with the aPTT (therapeutic range ~1.5&ndash;2.5&times; the control). Antidote to remember: <b>protamine sulfate</b>. (INR/PT tracks <i>warfarin</i>, not heparin &mdash; a classic NCLEX trap.)</div>
        <div class="qotd-signup">
          <span style="font-size:0.82rem;color:rgba(255,255,255,0.8);align-self:center;">Send it to my:</span>
          <div class="seg" data-qotd-channel>
            <button class="on" data-ch="phone">Phone</button>
            <button data-ch="email">Email</button>
          </div>
          <button class="btn btn-coral" data-qotd-sub style="padding:0.5rem 1.1rem;font-size:0.82rem;">Send me the daily question</button>
        </div>
        <p data-qotd-done hidden style="margin-top:0.8rem;font-size:0.82rem;color:var(--teal-400);font-weight:700;"></p>
      </div>
    </div>
  </section>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="eyebrow teal">You're not alone</span><h2>A community <span class="hl">in your corner.</span></h2></div>
      <div class="community">
        <div class="comm-card fade-up">
          <span class="ci" style="background:linear-gradient(140deg,#8b5cff,#4d2b9e);">{IC_USERS}</span>
          <div><h4>Private study group</h4><p>Join thousands of nurses-to-be trading tips, wins, and last-minute pep talks. Post a question at 2 a.m. and someone's awake.</p></div>
        </div>
        <div class="comm-card fade-up">
          <span class="ci" style="background:linear-gradient(140deg,#2ad4c4,#1a0942);">{I['play']}</span>
          <div><h4>Weekly live webinars</h4><p>A real instructor walks through the hardest topics live every week &mdash; ask questions, get answers, and catch the replay if you miss it.</p></div>
        </div>
      </div>
    </div>
  </section>

  <section style="background:var(--card);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="eyebrow gold">Take it with you</span><h2>The <span class="hl">50-question workbook.</span></h2><p>Every plan includes our downloadable NGN workbook &mdash; 50 original questions, each with a described illustration, a rationale for <b>every</b> option, an NCLEX tip, and a memory trick. Print it, mark it up, study offline.</p></div>
      <div class="points-strip fade-up">
        <div class="txt"><b>50 original Next Gen questions &middot; ~100 pages.</b><p>Written from scratch by our team &mdash; not scraped from anywhere. Yours to download and keep with any plan.</p></div>
        <a class="btn btn-dark" href="#pricing">Included with every plan</a>
      </div>
    </div>
  </section>

  <section id="pricing" style="background:var(--bg);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="eyebrow">Pricing</span><h2>One price. <span class="hl">Everything included.</span></h2><p>No add-ons, no upsells. Every plan unlocks the full system &mdash; questions, cases, readiness exams, schedules, the workbook, and Esi. Pick the runway that fits your test date.</p></div>
      {pricing_tiers("join.html")}
      <div class="guarantee fade-up">
        {I['shield']}
        <div><b>NCLEX Pass Guarantee</b><p>On the 2-, 3-, and 6-month plans, finish the program and if you don't pass, you get a full refund. We built it to work &mdash; and we stand behind it.</p></div>
      </div>
      <p style="text-align:center;margin-top:1.6rem;font-size:0.78rem;color:var(--ink-60);max-width:70ch;margin-left:auto;margin-right:auto;">NCLEX&reg; is a registered trademark of the National Council of State Boards of Nursing, Inc. Must Love Scrubs is not affiliated with or endorsed by NCSBN. All questions and materials are 100% original and created by our team. Educational content only &mdash; not medical advice.</p>
    </div>
  </section>

  <script src="js/complete.js"></script>
"""

PAGES["nclex-complete.html"] = ("NCLEX Complete — The Flagship NCLEX Prep | Must Love Scrubs",
    "NCLEX Complete: 50 Next Gen case studies, 2,600+ original questions, a strategy course, and 4 full-length readiness exams that predict your pass chance. Esi AI tutor included. Plans from $59.",
    COMPLETE_BODY, "courses")

# ---------------------------------------------------------------- QUESTION BANK (interactive, original content)

# Each: cat, stem, opts[{t,r}], correct index, tip, pct (answer-stats, sums ~100)
QBANK = [
    {"cat": "Pharmacology", "stem": "A client with atrial fibrillation is being discharged on warfarin. Which statement indicates the teaching was effective?",
     "opts": [
        {"t": "“I’ll double my dose if I ever miss a day.”", "r": "Doubling risks a dangerously high INR and bleeding — a missed dose is reported to the provider, not doubled."},
        {"t": "“I’ll keep my leafy-green vegetables about the same each week.”", "r": "Correct. Warfarin antagonizes vitamin K, so the goal is consistency (not avoidance) to keep the INR stable."},
        {"t": "“I can take ibuprofen for aches whenever I need it.”", "r": "NSAIDs raise bleeding risk and should not be taken freely with warfarin."},
        {"t": "“I’ll stop it once my heartbeat feels regular.”", "r": "Warfarin prevents clots in AFib regardless of how the rhythm feels; stopping abruptly raises stroke risk."}],
     "correct": 1, "tip": "When an option says “avoid all vitamin K foods,” it’s a trap — the answer is consistency.", "pct": [6, 71, 9, 14]},
    {"cat": "Pharmacology", "stem": "An older adult on digoxin and furosemide reports nausea, no appetite, and “yellow-green halos” around lights. What is the nurse’s priority action?",
     "opts": [
        {"t": "Give the next scheduled digoxin dose.", "r": "Giving more digoxin to a client showing toxicity could be fatal."},
        {"t": "Hold the digoxin and obtain digoxin and potassium levels.", "r": "Correct. Nausea, anorexia, and yellow-green vision are classic digoxin toxicity; low potassium (from furosemide) worsens it."},
        {"t": "Encourage a high-potassium breakfast and reassess later.", "r": "Diet alone won’t fix active toxicity, and delaying risks a lethal dysrhythmia."},
        {"t": "Document as expected heart-failure findings.", "r": "These are a medication emergency, not expected findings."}],
     "correct": 1, "tip": "Digoxin + a potassium-wasting diuretic = connect low K⁺ to higher toxicity risk.", "pct": [4, 79, 8, 9]},
    {"cat": "Med-Surg", "stem": "A client is started on IV furosemide for pulmonary edema. Which lab value is most important to monitor?",
     "opts": [
        {"t": "Serum sodium", "r": "Furosemide can lower sodium, but the potassium loss is the higher priority."},
        {"t": "Serum potassium", "r": "Correct. Furosemide is potassium-wasting; hypokalemia can cause life-threatening dysrhythmias."},
        {"t": "Serum calcium", "r": "Loop diuretics affect calcium slightly, but it isn’t the priority."},
        {"t": "Serum magnesium", "r": "Magnesium can drop, but potassium is the classic priority answer."}],
     "correct": 1, "tip": "Loop & thiazide → lose potassium; spironolactone → keeps it. Normal K⁺ = 3.5–5.0.", "pct": [10, 74, 7, 9]},
    {"cat": "Med-Surg", "stem": "A client with a traumatic brain injury is monitored for increased ICP. Which finding is the earliest sign to report?",
     "opts": [
        {"t": "Restlessness and a decreasing level of consciousness", "r": "Correct. A change in level of consciousness is the earliest, most sensitive sign of rising ICP."},
        {"t": "Bradycardia, widening pulse pressure, irregular respirations", "r": "That’s Cushing’s triad — a late, ominous sign, not early."},
        {"t": "Hypotension and tachycardia", "r": "This points to shock/hypovolemia, not classic ICP changes."},
        {"t": "Constricted, briskly reactive pupils", "r": "Rising ICP causes a dilated, sluggish pupil, not constricted/brisk."}],
     "correct": 0, "tip": "Read for “early” vs “late.” Early ICP = LOC change; late ICP = Cushing’s triad.", "pct": [63, 21, 7, 9]},
    {"cat": "Maternal / Newborn", "stem": "A laboring client on IV oxytocin shows late decelerations. What is the nurse’s first action?",
     "opts": [
        {"t": "Increase the oxytocin to strengthen contractions.", "r": "This worsens uteroplacental insufficiency — exactly wrong."},
        {"t": "Stop the oxytocin, reposition to the side, and give oxygen.", "r": "Correct. Late decels signal uteroplacental insufficiency; intrauterine resuscitation is the priority."},
        {"t": "Have the client hold her breath and push.", "r": "Pushing doesn’t correct the underlying oxygen problem."},
        {"t": "Document the reassuring tracing and continue.", "r": "Late decels are non-reassuring — they require action."}],
     "correct": 1, "tip": "VEAL CHOP: Late → Placental insufficiency → act. Turn, O₂, IV, stop the Pit.", "pct": [7, 76, 6, 11]},
    {"cat": "Pediatrics", "stem": "A 4-year-old presents drooling, in a tripod position, with high fever and a muffled voice. Epiglottitis is suspected. Which action should the nurse AVOID?",
     "opts": [
        {"t": "Keeping the child calm on the parent’s lap", "r": "This is appropriate — calm and upright prevents airway spasm."},
        {"t": "Examining the throat with a tongue depressor", "r": "Correct (this is what to AVOID). It can trigger laryngospasm and total airway obstruction."},
        {"t": "Preparing emergency airway equipment", "r": "Appropriate — have airway equipment ready."},
        {"t": "Notifying the provider and staying with the child", "r": "Appropriate — stay and escalate."}],
     "correct": 1, "tip": "Negative-style stem: the “right” answer is the wrong action. Epiglottitis = hands off the throat.", "pct": [8, 72, 11, 9]},
    {"cat": "Mental Health", "stem": "A client newly diagnosed with cancer says, “I feel like I’ve already let my kids down.” Which response is most therapeutic?",
     "opts": [
        {"t": "“Don’t worry — plenty of people beat cancer.”", "r": "False reassurance dismisses the feeling and shuts down communication."},
        {"t": "“It sounds like you’re feeling overwhelmed about facing your children.”", "r": "Correct. Reflecting the feeling shows empathy and invites the client to say more."},
        {"t": "“Why would you feel like you’ve let them down?”", "r": "“Why” questions can feel challenging and put the client on the defensive."},
        {"t": "“You should stay positive for your family.”", "r": "Telling them how to feel minimizes real distress."}],
     "correct": 1, "tip": "Therapeutic answers reflect feelings and keep the focus on the client — not advice or reassurance.", "pct": [5, 78, 8, 9]},
    {"cat": "Safety", "stem": "At the start of the shift, which client should the nurse assess first?",
     "opts": [
        {"t": "A client awaiting discharge paperwork", "r": "Stable — lowest priority."},
        {"t": "A client with new shortness of breath and SpO₂ 86%", "r": "Correct. Airway/Breathing comes first — an acute oxygenation emergency."},
        {"t": "A client requesting pain medication for chronic back pain (5/10)", "r": "Important but not immediately life-threatening."},
        {"t": "A post-op client with a small amount of dried drainage", "r": "Expected and stable."}],
     "correct": 1, "tip": "ABCs first, then acute-over-chronic, unstable-over-stable. Air goes first.", "pct": [4, 81, 8, 7]},
]
QBANK_JSON = _json.dumps(QBANK)
# --- assemble the bank from data/qbank/*.json (batch pipeline) ---
def _load_qbank():
    import glob as _glob, hashlib as _hl
    qs, seen = [], set()
    for path in sorted(_glob.glob(os.path.join(ROOT, 'data', 'qbank', '*.json'))):
        data = _json.load(open(path, encoding='utf-8'))
        for q in data.get('questions', []):
            t = q.get('type', 'mc')
            if q.get('id') in seen: continue
            if t == 'mc':
                if len(q.get('opts', [])) != 4: continue
                if not (0 <= q.get('correct', -1) <= 3): continue
                if 'pct' not in q:  # synthesize answer-stats
                    base = {'Easy': 78, 'Moderate': 68, 'Hard': 55}.get(q.get('difficulty', 'Moderate'), 68)
                    h = int(_hl.md5(q['id'].encode()).hexdigest(), 16)
                    c = q['correct']; pct = [0, 0, 0, 0]; pct[c] = base + (h % 7) - 3
                    rem = 100 - pct[c]; others = [i for i in range(4) if i != c]
                    splits = [rem // 2, rem // 3, rem - rem // 2 - rem // 3]
                    for k, i in enumerate(others): pct[i] = splits[k]
                    q['pct'] = pct
            elif t == 'sata':
                if len(q.get('opts', [])) < 3: continue
                if not isinstance(q.get('correct'), list) or not q['correct']: continue
            elif t == 'matrix':
                if not q.get('cols') or not q.get('rows'): continue
            elif t == 'bowtie':
                if not (q.get('condition') and q.get('actions') and q.get('parameters')): continue
            else:
                continue  # unknown type
            # numeric difficulty level for the CAT engine (1=very easy … 5=very hard).
            # Easy/Moderate/Hard map to 2/3/4; 1 and 5 reserved for finer calibration.
            q['level'] = {'Easy': 2, 'Moderate': 3, 'Hard': 4}.get(q.get('difficulty', 'Moderate'), 3)
            seen.add(q['id'])
            qs.append(q)
    return qs

_loaded = _load_qbank()
if _loaded:
    QBANK = _loaded
QB_FREE = [q for q in QBANK if q.get('free')] or QBANK
QB_TOTAL = len(QBANK)
QBANK_JSON = _json.dumps(QB_FREE, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
QB_CATS = ['All']
for _q in QB_FREE:
    if _q['cat'] not in QB_CATS:
        QB_CATS.append(_q['cat'])

def qb_chips():
    out = []
    for i, c in enumerate(QB_CATS):
        on = " on" if i == 0 else ""
        out.append(f'<button class="qb-chip{on}" data-cat="{c}">{c}</button>')
    return "".join(out)

QBANK_BODY = f"""  <div class="page-hero">
    <div class="wrap inner">
      <span class="lesson-label" style="color:var(--gold-400);">Question Bank &middot; Sample</span>
      <h1 style="margin-top:0.6rem;">Practice like it’s the <span class="em">real thing</span>.</h1>
      <p>Every question has a rationale for <b>every</b> option, answer stats, and one-tap tagging &mdash; the same engine that powers the full bank. This is a free taste; unlock the rest with any plan.</p>
    </div>
  </div>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="qbank" data-qb-total="{QB_TOTAL}">
        <script type="application/json" data-qbank>{QBANK_JSON}</script>
        <div class="qb-bar fade-up">
          <div class="qb-chips">{qb_chips()}</div>
          <div class="qb-meta">
            <span class="qb-stat">Score <b data-qb-score>0/0</b></span>
            <span class="qb-stat">Timer <b data-qb-timer>0:00</b></span>
            <span class="qb-stat">Q <b data-qb-prog>1/{len(QB_FREE)}</b></span>
          </div>
        </div>
        <div class="qb-stage fade-up" data-qb-stage></div>
        <div class="qb-gate" data-qb-gate hidden>
          <div class="lock-ic">{I['lock']}</div>
          <h3>That’s the free sample.</h3>
          <p>You’ve seen how the bank works. The full <b>{QB_TOTAL}-question</b> bank &mdash; growing toward 2,600+, every NGN type, all clinical areas, with Esi drilling your misses &mdash; comes with any plan.</p>
          <a class="btn btn-coral" href="nclex-complete.html#pricing">Unlock the full bank &mdash; from $59</a>
        </div>
      </div>
    </div>
  </section>

  <script src="js/qbank.js"></script>
"""

PAGES["qbank.html"] = ("NCLEX Question Bank (Free Sample) | Must Love Scrubs",
    "Practice original NCLEX-style questions with a rationale for every option, answer stats, and Mastered/Reviewing/Learning tagging. A free sample of the 2,600+ question bank.",
    QBANK_BODY, "courses")

# ---------------------------------------------------------------- TESTS & EXAMS (pop quiz / basic / NCLEX mock CAT / specialty mock)
# The engine draws from the whole loaded bank; content scales as batches are added.
TESTS_JSON = _json.dumps(QBANK, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')

def test_specialty_options():
    out = ['<option value="All">All clinical areas</option>']
    for c in QB_CATS[1:]:
        out.append(f'<option value="{c}">{c}</option>')
    return "".join(out)

TEST_MODES = [
    ("quiz", I['bolt'], "Pop Quiz", "8 questions", "A fast daily gut-check with instant rationale after every question. Perfect between study blocks or straight off your calendar.", "Start pop quiz", "coral"),
    ("basic", I['list'], "Basic Test", "20 questions", "A focused 20-question test across mixed topics. Answer straight through, then get your score, weak areas, and a full review.", "Start basic test", "line"),
    ("nclex", I['target'], "NCLEX Mock Test", "85–150 · adaptive", "The real deal. A full computer-adaptive simulation that gets harder or easier as you go and stops the moment it knows where you stand — exactly like test day.", "Start NCLEX mock", "coral"),
    ("specialty", I['heart'], "Specialty Mock Test", "100 questions", "A 100-question deep dive in one clinical area — build mastery and confidence in your specialty before the floor or a certification.", "Start specialty mock", "line"),
]

def test_cards():
    out = []
    for slug, icon, title, meta, desc, cta, tone in TEST_MODES:
        pick = ""
        if slug == "specialty":
            pick = f'<select class="ex-select" data-test-specialty aria-label="Choose a specialty">{test_specialty_options()}</select>'
        out.append(f"""        <div class="ex-card fade-up">
          <div class="ex-card-ic">{icon}</div>
          <span class="ex-card-len">{meta}</span>
          <h3>{title}</h3>
          <p>{desc}</p>
          {pick}
          <button class="btn btn-{tone} ex-card-go" data-test-start="{slug}">{cta} &rarr;</button>
        </div>""")
    return "\n".join(out)

TESTS_BODY = f"""  <div class="page-hero">
    <div class="wrap inner">
      <span class="lesson-label" style="color:var(--gold-400);">Tests &amp; Exams</span>
      <h1 style="margin-top:0.6rem;">Test yourself like it’s <span class="em">test day</span>.</h1>
      <p>Four ways to prove you’re ready &mdash; a quick pop quiz, a basic test, a full computer-adaptive NCLEX mock, or a 100-question specialty deep dive. Every one ends with your score, your weak areas, and a rationale on every question.</p>
    </div>
  </div>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="exam" data-exam>
        <script type="application/json" data-tests>{TESTS_JSON}</script>

        <div data-exam-setup>
          <div class="ex-grid">
{test_cards()}
          </div>
          <div class="ex-history" data-exam-history hidden></div>
          <div class="ex-how fade-up">
            <h3 class="ex-h">How the adaptive NCLEX mock works</h3>
            <div class="ex-how-grid">
              <div><span class="ex-step">1</span><b>Everyone starts at the passing line.</b><p>Your first question sits right at the standard the NCLEX uses to decide pass or fail.</p></div>
              <div><span class="ex-step">2</span><b>It adapts to you.</b><p>Get one right and the next is harder; miss one and it eases off &mdash; zeroing in on your true ability with each answer.</p></div>
              <div><span class="ex-step">3</span><b>It stops when it’s sure.</b><p>After 85 items it ends the moment it’s 95% confident you’re clearly above or below the line &mdash; up to a 150-item ceiling. Same rules as the real exam.</p></div>
            </div>
          </div>
        </div>

        <div data-exam-run hidden>
          <div class="ex-bar" data-exam-bar></div>
          <div class="ex-stage" data-exam-stage></div>
          <div class="ex-runfoot"><button class="ex-quit" data-exam-quit>End test</button></div>
        </div>

        <div class="ex-results" data-exam-results hidden></div>
      </div>
    </div>
  </section>

  <script src="js/tests.js"></script>
"""

PAGES["tests.html"] = ("NCLEX Practice Tests &amp; Adaptive Mock Exams | Must Love Scrubs",
    "Take a pop quiz, a basic test, a full adaptive NCLEX mock exam (85–150 questions), or a 100-question specialty mock. Score, weak-area breakdown, and a rationale on every question.",
    TESTS_BODY, "courses")

# ---------------------------------------------------------------- FLASHCARDS + GAMES (adaptive, same difficulty model as CAT)

def _load_flashcards():
    import glob as _glob
    cards, seen = [], set()
    for path in sorted(_glob.glob(os.path.join(ROOT, 'data', 'flashcards', '*.json'))):
        data = _json.load(open(path, encoding='utf-8'))
        for c in data.get('cards', []):
            if not c.get('front'): continue
            kind = c.get('kind', 'qa')
            if kind == 'qa' and not c.get('back'): continue   # flip cards need a back
            if c.get('id') in seen: continue
            seen.add(c['id'])
            c.setdefault('kind', 'qa')
            c.setdefault('difficulty', 3)   # 1..5, same scale as the CAT engine
            cards.append(c)
    return cards

FLASH = _load_flashcards()
FLASH_JSON = _json.dumps(FLASH, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
FLASH_DECKS = []
for _c in FLASH:
    if _c['deck'] not in FLASH_DECKS:
        FLASH_DECKS.append(_c['deck'])

def flash_deck_chips():
    out = ['<button class="fc-chip on" data-deck="All">All</button>']
    for d in FLASH_DECKS:
        out.append(f'<button class="fc-chip" data-deck="{d}">{d}</button>')
    return "".join(out)

FLASH_BODY = f"""  <div class="page-hero">
    <div class="wrap inner">
      <span class="lesson-label" style="color:var(--gold-400);">Flashcards &amp; Games</span>
      <h1 style="margin-top:0.6rem;">Flip it. Play it. <span class="em">Remember it.</span></h1>
      <p>Animated flashcards with a rationale on the back &mdash; then turn the same cards into quizzes, a match game, and a speed round. Adaptive levels (1&ndash;5) rise as you improve, exactly like the CAT engine. Works for NCLEX <b>and</b> specialty prep.</p>
    </div>
  </div>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="flash" data-flash-total="{len(FLASH)}">
        <script type="application/json" data-flash>{FLASH_JSON}</script>
        <div class="fc-bar fade-up"><div class="fc-decks">{flash_deck_chips()}</div></div>
        <div class="fc-modes fade-up">
          <button class="fc-mode on" data-mode="study">Study</button>
          <button class="fc-mode" data-mode="challenge">Challenge</button>
          <button class="fc-mode" data-mode="quiz">Quiz</button>
          <button class="fc-mode" data-mode="match">Match game</button>
          <button class="fc-mode" data-mode="speed">Speed round</button>
        </div>
        <div class="fc-meta fade-up">
          <span class="fc-stat">Level <b data-fc-level>1</b></span>
          <span class="fc-stat">Mastered <b data-fc-mastered>0</b></span>
          <span class="fc-stat">Streak <b data-fc-streak>0</b></span>
          <span class="fc-stat">Deck <b data-fc-count>0</b></span>
        </div>
        <div class="fc-stage fade-up" data-fc-stage></div>
      </div>
    </div>
  </section>

  <script src="js/flashcards.js"></script>
"""

PAGES["flashcards.html"] = ("Nursing Flashcards & Games (Adaptive) | Must Love Scrubs",
    "Animated nursing flashcards with rationales, plus quizzes, a match game, and a speed round. Adaptive difficulty levels for NCLEX and specialty prep.",
    FLASH_BODY, "courses")

# ---------------------------------------------------------------- DRUG CARDS (structured medication library + drill)

def _load_drugs():
    import glob as _glob
    drugs, seen = [], set()
    for path in sorted(_glob.glob(os.path.join(ROOT, 'data', 'drugs', '*.json'))):
        data = _json.load(open(path, encoding='utf-8'))
        for x in data.get('drugs', []):
            if not x.get('generic') or not x.get('class'): continue
            if x.get('id') in seen: continue
            seen.add(x['id'])
            drugs.append(x)
    drugs.sort(key=lambda x: x['generic'].lower())
    return drugs

DRUGS = _load_drugs()
DRUGS_JSON = _json.dumps(DRUGS, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
DRUG_SYSTEMS = []
for _x in DRUGS:
    if _x['system'] not in DRUG_SYSTEMS:
        DRUG_SYSTEMS.append(_x['system'])
DRUG_SYSTEMS.sort()

def drug_sys_chips():
    out = ['<button class="dc-chip on" data-sys="All">All systems</button>']
    for s in DRUG_SYSTEMS:
        out.append(f'<button class="dc-chip" data-sys="{s}">{s}</button>')
    return "".join(out)

DRUGS_BODY = f"""  <div class="page-hero">
    <div class="wrap inner">
      <span class="lesson-label" style="color:var(--gold-400);">Drug Cards</span>
      <h1 style="margin-top:0.6rem;">Every drug, the <span class="em">same way</span>.</h1>
      <p>Pharmacology is the #1 place NCLEX trips nurses up. Each card gives you one medication in the exact same shape &mdash; class, how it works, uses, side effects, the nursing considerations that matter, and the antidote &mdash; so your brain can pattern-match on test day. Search it, filter by body system, then <b>drill</b> it like flashcards.</p>
    </div>
  </div>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="drugcards" data-drugs-total="{len(DRUGS)}">
        <script type="application/json" data-drugs>{DRUGS_JSON}</script>
        <div class="dc-tools fade-up">
          <div class="dc-search">
            {I['search']}
            <input type="search" placeholder="Search a drug, brand, or class&hellip;" aria-label="Search drug cards" data-dc-search>
          </div>
          <div class="dc-modes">
            <button class="dc-mode on" data-dc-mode="browse">Browse</button>
            <button class="dc-mode" data-dc-mode="drill">Drill</button>
          </div>
        </div>
        <div class="dc-chips fade-up" data-dc-chips>{drug_sys_chips()}</div>
        <p class="dc-count fade-up"><b data-dc-count>{len(DRUGS)}</b> drug cards &middot; growing every week</p>
        <div class="dc-grid fade-up" data-dc-grid></div>
        <div class="dc-drill fade-up" data-dc-drill hidden></div>
        <div class="dc-empty" data-dc-empty hidden><p><b>No match yet.</b> This library grows every week &mdash; tell us what to add at hello@mustlovescrubs.com.</p></div>
      </div>
    </div>
  </section>

  <section style="background:var(--card);">
    <div class="wrap" style="text-align:center;">
      <div class="section-head fade-up" style="margin-inline:auto;"><span class="lesson-label" style="color:var(--teal-600);">Go deeper</span><h2>Turn these into a <span class="em">quiz</span>.</h2><p style="margin-inline:auto;">Drug cards feed the same adaptive engine as the question bank &mdash; drill them here, then test yourself in the question bank and mock exams.</p></div>
      <div class="hero-cta" style="justify-content:center;"><a class="btn btn-coral" href="qbank.html">Practice questions</a><a class="btn btn-line" href="tests.html">Take a test</a></div>
    </div>
  </section>

  <script src="js/drugs.js"></script>
"""

PAGES["drugs.html"] = ("NCLEX Drug Cards &mdash; Nursing Pharmacology Library | Must Love Scrubs",
    "A searchable library of nursing drug cards: class, mechanism, uses, side effects, nursing considerations, and antidotes for the highest-yield NCLEX medications. Drill them like flashcards.",
    DRUGS_BODY, "courses")

# ---------------------------------------------------------------- CHEAT SHEETS (searchable clinical reference)

def _load_cheatsheets():
    import glob as _glob
    sheets, seen = [], set()
    for path in sorted(_glob.glob(os.path.join(ROOT, 'data', 'cheatsheets', '*.json'))):
        data = _json.load(open(path, encoding='utf-8'))
        for s in data.get('sheets', []):
            if not s.get('title') or not s.get('sections'): continue
            if s.get('id') in seen: continue
            seen.add(s['id']); sheets.append(s)
    return sheets

CHEATS = _load_cheatsheets()
CHEATS_JSON = _json.dumps(CHEATS, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
CHEAT_CATS = []
for _s in CHEATS:
    if _s['category'] not in CHEAT_CATS:
        CHEAT_CATS.append(_s['category'])
CHEAT_CATS.sort()

def cheat_cat_chips():
    out = ['<button class="cs-chip on" data-cat="All">All</button>']
    for c in CHEAT_CATS:
        out.append(f'<button class="cs-chip" data-cat="{c}">{c}</button>')
    return "".join(out)

CHEATS_BODY = f"""  <div class="page-hero">
    <div class="wrap inner">
      <span class="lesson-label" style="color:var(--gold-400);">Cheat Sheets</span>
      <h1 style="margin-top:0.6rem;">Every high-yield fact, <span class="em">one tap away</span>.</h1>
      <p>Pocket-sized clinical reference sheets &mdash; lab values, ABGs, fluids &amp; electrolytes, antidotes, isolation precautions &mdash; searchable, filterable, and printable. The stuff you want the night before an exam and on the floor.</p>
    </div>
  </div>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="cheats" data-cheats-total="{len(CHEATS)}">
        <script type="application/json" data-cheats>{CHEATS_JSON}</script>
        <div class="cs-tools fade-up">
          <div class="cs-search">
            {I['search']}
            <input type="search" placeholder="Search a sheet or a value&hellip;" aria-label="Search cheat sheets" data-cs-search>
          </div>
        </div>
        <div class="cs-chips fade-up" data-cs-chips>{cheat_cat_chips()}</div>
        <p class="cs-count fade-up"><b data-cs-count>{len(CHEATS)}</b> cheat sheets &middot; growing every week</p>
        <div class="cs-grid fade-up" data-cs-grid></div>
        <div class="cs-empty" data-cs-empty hidden><p><b>No match yet.</b> Tell us what to add at hello@mustlovescrubs.com.</p></div>
      </div>
    </div>
  </section>

  <script src="js/cheatsheets.js"></script>
"""

PAGES["cheatsheets.html"] = ("NCLEX Nursing Cheat Sheets &mdash; Lab Values, ABGs, Antidotes | Must Love Scrubs",
    "Free searchable nursing cheat sheets: lab values, ABGs, fluid & electrolytes, medication antidotes, isolation precautions, and vital signs by age. Printable clinical reference for students and nurses.",
    CHEATS_BODY, "courses")

# ---------------------------------------------------------------- CARE PLANS (ADPIE library)

def _load_careplans():
    import glob as _glob
    plans, seen = [], set()
    for path in sorted(_glob.glob(os.path.join(ROOT, 'data', 'careplans', '*.json'))):
        data = _json.load(open(path, encoding='utf-8'))
        for p in data.get('plans', []):
            if not p.get('title') or not p.get('diagnoses'): continue
            if p.get('id') in seen: continue
            seen.add(p['id']); plans.append(p)
    return plans

CAREPLANS = _load_careplans()
CAREPLANS_JSON = _json.dumps(CAREPLANS, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
CP_DX_TOTAL = sum(len(p['diagnoses']) for p in CAREPLANS)
CP_CATS = []
for _p in CAREPLANS:
    if _p['category'] not in CP_CATS:
        CP_CATS.append(_p['category'])
CP_CATS.sort()

def cp_cat_chips():
    out = ['<button class="cp-chip on" data-cat="All">All</button>']
    for c in CP_CATS:
        out.append(f'<button class="cp-chip" data-cat="{c}">{c}</button>')
    return "".join(out)

CAREPLANS_BODY = f"""  <div class="page-hero">
    <div class="wrap inner">
      <span class="lesson-label" style="color:var(--gold-400);">Care Plans</span>
      <h1 style="margin-top:0.6rem;">Care plans, <span class="em">done right</span>.</h1>
      <p>Full nursing care plans in the format your instructor wants &mdash; nursing diagnosis, assessment data, measurable outcomes, and interventions with the <b>rationale</b> behind each one. Searchable, filterable, and built to teach the clinical judgment, not just fill a template.</p>
    </div>
  </div>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="careplans" data-cp-total="{len(CAREPLANS)}">
        <script type="application/json" data-careplans>{CAREPLANS_JSON}</script>
        <div class="cp-tools fade-up">
          <div class="cp-search">
            {I['search']}
            <input type="search" placeholder="Search a condition or diagnosis&hellip;" aria-label="Search care plans" data-cp-search>
          </div>
        </div>
        <div class="cp-chips fade-up" data-cp-chips>{cp_cat_chips()}</div>
        <p class="cp-count fade-up"><b data-cp-count>{len(CAREPLANS)}</b> care plans &middot; {CP_DX_TOTAL} nursing diagnoses &middot; growing weekly</p>
        <div class="cp-grid fade-up" data-cp-grid></div>
        <div class="cp-empty" data-cp-empty hidden><p><b>No match yet.</b> Tell us what to add at hello@mustlovescrubs.com.</p></div>
      </div>
    </div>
  </section>

  <script src="js/careplans.js"></script>
"""

PAGES["care-plans.html"] = ("Nursing Care Plans &mdash; Diagnoses, Interventions &amp; Rationales | Must Love Scrubs",
    "Free nursing care plans in full ADPIE format: nursing diagnosis, assessment, measurable outcomes, and interventions with rationales — heart failure, pneumonia, diabetes, COPD, pain, falls, skin integrity, and infection.",
    CAREPLANS_BODY, "courses")

# ---------------------------------------------------------------- LAB VALUES (comprehensive reference — range + high + low)

def _load_labvalues():
    import glob as _glob
    labs, seen = [], set()
    for path in sorted(_glob.glob(os.path.join(ROOT, 'data', 'labvalues', '*.json'))):
        data = _json.load(open(path, encoding='utf-8'))
        for x in data.get('labs', []):
            if not x.get('name') or not x.get('range'): continue
            if x.get('id') in seen: continue
            seen.add(x['id']); labs.append(x)
    return labs

LABS = _load_labvalues()
LABS_JSON = _json.dumps(LABS, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
LAB_CATS = []
for _x in LABS:
    if _x['category'] not in LAB_CATS:
        LAB_CATS.append(_x['category'])

def lab_cat_chips():
    out = ['<button class="lv-chip on" data-cat="All">All</button>']
    for c in LAB_CATS:
        out.append(f'<button class="lv-chip" data-cat="{c}">{c}</button>')
    return "".join(out)

LABS_BODY = f"""  <div class="page-hero">
    <div class="wrap inner">
      <span class="lesson-label" style="color:var(--gold-400);">Lab Values</span>
      <h1 style="margin-top:0.6rem;">Every lab, and what it <span class="em">means</span>.</h1>
      <p>All {len(LABS)} high-yield NCLEX lab values &mdash; not just the number, but what a <b>high</b> result means and what a <b>low</b> result means, plus the critical values that mean call the provider now. Search any lab, filter by panel.</p>
    </div>
  </div>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="labvalues" data-lv-total="{len(LABS)}">
        <script type="application/json" data-labs>{LABS_JSON}</script>
        <div class="lv-tools fade-up">
          <div class="lv-search">
            {I['search']}
            <input type="search" placeholder="Search a lab (e.g. potassium, INR)&hellip;" aria-label="Search lab values" data-lv-search>
          </div>
        </div>
        <div class="lv-chips fade-up" data-lv-chips>{lab_cat_chips()}</div>
        <p class="lv-count fade-up"><b data-lv-count>{len(LABS)}</b> lab values &middot; {len(LAB_CATS)} panels</p>
        <div class="lv-list fade-up" data-lv-list></div>
        <div class="lv-empty" data-lv-empty hidden><p><b>No match yet.</b> Tell us what to add at hello@mustlovescrubs.com.</p></div>
      </div>
    </div>
  </section>

  <script src="js/labvalues.js"></script>
"""

PAGES["lab-values.html"] = ("NCLEX Lab Values (All 65) &mdash; Normal Ranges, High &amp; Low Meaning | Must Love Scrubs",
    "Every high-yield NCLEX lab value with its normal range, what a high result means, what a low result means, and critical values. Searchable, filterable nursing lab reference.",
    LABS_BODY, "courses")

# ---------------------------------------------------------------- MNEMONICS (+ emoji picmonic visuals)

def _load_mnemonics():
    import glob as _glob
    out, seen = [], set()
    for path in sorted(_glob.glob(os.path.join(ROOT, 'data', 'mnemonics', '*.json'))):
        data = _json.load(open(path, encoding='utf-8'))
        for m in data.get('mnemonics', []):
            if not m.get('title') or not m.get('letters'): continue
            if m.get('id') in seen: continue
            seen.add(m['id']); out.append(m)
    return out

MNEMS = _load_mnemonics()
MNEMS_JSON = _json.dumps(MNEMS, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
MNEM_CATS = []
for _m in MNEMS:
    if _m['category'] not in MNEM_CATS:
        MNEM_CATS.append(_m['category'])
MNEM_CATS.sort()

def mnem_cat_chips():
    out = ['<button class="mn-chip on" data-cat="All">All</button>']
    for c in MNEM_CATS:
        out.append(f'<button class="mn-chip" data-cat="{c}">{c}</button>')
    return "".join(out)

MNEMS_BODY = f"""  <div class="page-hero">
    <div class="wrap inner">
      <span class="lesson-label" style="color:var(--gold-400);">Mnemonics</span>
      <h1 style="margin-top:0.6rem;">Make it <span class="em">stick</span>.</h1>
      <p>The memory tricks nurses swear by &mdash; MONA, VEAL CHOP, SLUDGE, FAST and more &mdash; each broken down letter by letter with a visual cue. Your brain remembers stories and pictures, not lists. Search any topic, filter by system.</p>
    </div>
  </div>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="mnemonics" data-mn-total="{len(MNEMS)}">
        <script type="application/json" data-mnems>{MNEMS_JSON}</script>
        <div class="mn-tools fade-up">
          <div class="mn-search">
            {I['search']}
            <input type="search" placeholder="Search a mnemonic or topic&hellip;" aria-label="Search mnemonics" data-mn-search>
          </div>
        </div>
        <div class="mn-chips fade-up" data-mn-chips>{mnem_cat_chips()}</div>
        <p class="mn-count fade-up"><b data-mn-count>{len(MNEMS)}</b> mnemonics &middot; growing weekly</p>
        <div class="mn-grid fade-up" data-mn-grid></div>
        <div class="mn-empty" data-mn-empty hidden><p><b>No match yet.</b> Tell us what to add at hello@mustlovescrubs.com.</p></div>
      </div>
    </div>
  </section>

  <script src="js/mnemonics.js"></script>
"""

PAGES["mnemonics.html"] = ("Nursing Mnemonics &mdash; MONA, VEAL CHOP, SLUDGE &amp; More | Must Love Scrubs",
    "A searchable library of high-yield nursing mnemonics with letter-by-letter breakdowns and visual cues — MONA, VEAL CHOP, SLUDGE, FAST, ADPIE, SIG E CAPS, and more.",
    MNEMS_BODY, "courses")

# ---------------------------------------------------------------- PATHO (pathophysiology charts)

def _load_patho():
    import glob as _glob
    out, seen = [], set()
    for path in sorted(_glob.glob(os.path.join(ROOT, 'data', 'patho', '*.json'))):
        data = _json.load(open(path, encoding='utf-8'))
        for c in data.get('conditions', []):
            if not c.get('title') or not c.get('patho'): continue
            if c.get('id') in seen: continue
            seen.add(c['id']); out.append(c)
    return out

PATHO = _load_patho()
PATHO_JSON = _json.dumps(PATHO, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
PATHO_CATS = []
for _c in PATHO:
    if _c['category'] not in PATHO_CATS:
        PATHO_CATS.append(_c['category'])
PATHO_CATS.sort()

def patho_cat_chips():
    out = ['<button class="pt-chip on" data-cat="All">All</button>']
    for c in PATHO_CATS:
        out.append(f'<button class="pt-chip" data-cat="{c}">{c}</button>')
    return "".join(out)

PATHO_BODY = f"""  <div class="page-hero">
    <div class="wrap inner">
      <span class="lesson-label" style="color:var(--gold-400);">Patho</span>
      <h1 style="margin-top:0.6rem;">Understand the <span class="em">why</span>.</h1>
      <p>Pathophysiology made visual &mdash; each disease as a chain from cause to mechanism to the exact signs it produces (and <b>why</b>), then diagnostics, complications, and treatment. Stop memorizing lists; see how it all connects. Linked to the matching care plan.</p>
    </div>
  </div>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="patho" data-pt-total="{len(PATHO)}">
        <script type="application/json" data-patho>{PATHO_JSON}</script>
        <div class="pt-tools fade-up">
          <div class="pt-search">
            {I['search']}
            <input type="search" placeholder="Search a disease or system&hellip;" aria-label="Search pathophysiology" data-pt-search>
          </div>
        </div>
        <div class="pt-chips fade-up" data-pt-chips>{patho_cat_chips()}</div>
        <p class="pt-count fade-up"><b data-pt-count>{len(PATHO)}</b> conditions &middot; growing weekly</p>
        <div class="pt-grid fade-up" data-pt-grid></div>
        <div class="pt-empty" data-pt-empty hidden><p><b>No match yet.</b> Tell us what to add at hello@mustlovescrubs.com.</p></div>
      </div>
    </div>
  </section>

  <script src="js/patho.js"></script>
"""

PAGES["patho.html"] = ("Pathophysiology Made Visual &mdash; Disease Mechanisms for Nurses | Must Love Scrubs",
    "Nursing pathophysiology explained simply: each disease as a chain from cause to mechanism to signs (and why), plus diagnostics, complications, and treatment. Heart failure, MI, COPD, diabetes, sepsis, stroke, and more.",
    PATHO_BODY, "courses")

# ---------------------------------------------------------------- STUDY CALENDAR (the conductor)

STUDYPLAN_BODY = f"""  <div class="page-hero">
    <div class="wrap inner">
      <span class="lesson-label" style="color:var(--gold-400);">Study Plan</span>
      <h1 style="margin-top:0.6rem;">Your plan, run like a <span class="em">class</span>.</h1>
      <p>Pick your test date and we build a day-by-day calendar that runs the whole system for you &mdash; reading, flashcards, case studies, pop quizzes, mnemonic games, and weekly review tests &mdash; on the learning science that makes it stick: spaced repetition, active recall, and interleaving.</p>
    </div>
  </div>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="planner" data-planner>
        <div class="plan-controls fade-up">
          <div class="pc-row">
            <label>Plan length
              <div class="seg pc-len" data-plan-len>
                <button data-len="1">1 mo</button>
                <button class="on" data-len="2">2 mo</button>
                <button data-len="3">3 mo</button>
                <button data-len="6">6 mo</button>
              </div>
            </label>
            <label>Start date <input type="date" data-plan-start></label>
            <button class="btn btn-coral" data-plan-go>Build my plan</button>
          </div>
          <div class="pc-meta">
            <span class="fc-stat">Days done <b data-plan-done>0</b></span>
            <span class="fc-stat">Total days <b data-plan-total>0</b></span>
            <span class="fc-stat">Streak <b data-plan-streak>0</b></span>
            <div class="plan-progress"><i data-plan-bar style="width:0%"></i></div>
          </div>
          <div class="plan-legend">
            <span class="lg lg-read">Read</span><span class="lg lg-cards">Flashcards</span>
            <span class="lg lg-review">Review</span><span class="lg lg-quiz">Pop quiz</span>
            <span class="lg lg-case">Case study</span><span class="lg lg-game">Mnemonic game</span>
            <span class="lg lg-test">Review test</span><span class="lg lg-exam">Readiness exam</span>
            <span class="lg lg-rest">Rest</span>
          </div>
        </div>
        <div class="plan-cal fade-up" data-plan-cal></div>
      </div>
      <div class="plan-why fade-up">
        <h3>Why a calendar beats “just do questions”</h3>
        <p>Cramming fades; <b>spaced repetition</b> (revisiting a topic right before you'd forget it), <b>active recall</b> (retrieving instead of rereading), and <b>interleaving</b> (mixing topics) are the most evidence-backed ways to learn faster and remember longer. The calendar schedules all three automatically, then re-weights toward whatever you keep missing.</p>
      </div>
    </div>
  </section>

  <div class="plan-day-modal" data-plan-modal hidden>
    <div class="pdm-card">
      <button class="pdm-close" data-plan-close aria-label="Close">&times;</button>
      <div data-plan-modal-body></div>
    </div>
  </div>

  <script src="js/studyplan.js"></script>
"""

PAGES["study-plan.html"] = ("NCLEX Study Plan Calendar (Day-by-Day) | Must Love Scrubs",
    "Build a personalized day-by-day NCLEX study calendar that runs reading, flashcards, case studies, pop quizzes, mnemonic games, and review tests on spaced repetition and active recall.",
    STUDYPLAN_BODY, "courses")

# ---------------------------------------------------------------- FREE NCLEX STUDY GUIDE / RESOURCES HUB

# NCLEX-101 quick-jump topics (icon key, label, anchor, blurb)
GUIDE_TOPICS = [
    ("dict", "How do I register?", "register", "Sign up with your board of nursing, get your ATT, and book your date."),
    ("shield", "What's exam day like?", "examday", "What to bring, what to expect, and how the CAT actually works."),
    ("card", "How much does it cost?", "fees", "The exam fee, extra costs, and where prep fits your budget."),
    ("book", "What's on the test plan?", "testplan", "The categories every question is drawn from — and where to focus."),
    ("star", "When should I take it?", "when", "How to pick a test date that gives you enough runway."),
    ("play", "How long should I study?", "study", "1, 2, 3, or 6 months — take the quiz and get a matched plan."),
]

def guide_cards():
    out = []
    for icon, label, anchor, blurb in GUIDE_TOPICS:
        out.append(f"""<a class="spec-card fade-up" href="#{anchor}">
          <span class="ic" style="background:linear-gradient(140deg,#8b5cff,#4d2b9e);">{I[icon]}</span>
          <h3>{label}</h3>
          <p>{blurb}</p>
          <div class="foot"><span class="go">Read &rarr;</span></div>
        </a>""")
    return '<div class="spec-grid">' + "".join(out) + '</div>'

GUIDE_BODY = f"""  <div class="page-hero">
    <div class="wrap inner">
      <span class="lesson-label" style="color:var(--gold-400);">Free NCLEX Study Guide</span>
      <h1 style="margin-top:0.6rem;">Everything you need to pass &mdash; <span class="em">for nurses, by nurses.</span></h1>
      <p>Must Love Scrubs was built by a group of nurses who remember exactly how the NCLEX felt. This free guide is the advice we wish we'd had &mdash; how the test works, how to study, and how to walk in ready.</p>
      <div class="hero-cta" style="margin-top:1.8rem;">
        <a class="btn btn-coral" href="#ngn">Start reading</a>
        <a class="btn btn-ghost" href="nclex-complete.html">See the MLS Bootcamp</a>
      </div>
    </div>
  </div>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="intro-letter fade-up">
        {photo('nurses-group.jpg', 'linear-gradient(150deg,#4d2b9e,#14b8a8)', 'min-height:280px;')}
        <div class="letter-body">
          <span class="eyebrow teal">Hi, future nurse</span>
          <h2>First &mdash; breathe.</h2>
          <p>We're the nurses behind Must Love Scrubs, and we made this because the NCLEX terrified us too. Here's the good news: the Next Gen NCLEX has stopped asking you to memorize every tiny detail. It wants to know one thing &mdash; <b>can you think like a nurse?</b></p>
          <p>That's learnable. Everything in this guide (and everything in our prep) is built to grow exactly that skill: reading a situation, weighing the options, and choosing the safest action. Practice that, and test day stops being a wall and starts being a formality.</p>
          <p style="margin-top:1rem;"><b>Happy studying &mdash; you've got this.</b><br><span style="color:var(--ink-60);">&mdash; The Must Love Scrubs team, nurses who've been where you are</span></p>
          <p style="margin-top:1rem;font-size:0.82rem;color:var(--ink-60);">Want the full program? <a href="nclex-complete.html" style="color:var(--coral-500);font-weight:700;">Meet NCLEX Complete &mdash; our bootcamp &rarr;</a> &nbsp;<span style="opacity:0.7;">(placeholder: your external bootcamp link can point here too)</span></p>
        </div>
      </div>
    </div>
  </section>

  <section style="background:var(--card);">
    <div class="wrap">
      <div class="qotd fade-up" style="max-width:720px;margin:0 auto;">
        <span class="qk">Free &middot; every morning</span>
        <h3>Subscribe to the NCLEX Question of the Day</h3>
        <p class="stem">One fresh NGN-style question in your inbox or on your phone, every day &mdash; pulled from our original question bank. Free to join, and a great way to keep your mind sharp.</p>
        <div class="qotd-signup">
          <span style="font-size:0.82rem;color:rgba(255,255,255,0.8);align-self:center;">Send it to my:</span>
          <div class="seg" data-qotd-channel>
            <button class="on" data-ch="phone">Phone</button>
            <button data-ch="email">Email</button>
          </div>
          <a class="btn btn-coral" href="join.html" style="padding:0.5rem 1.1rem;font-size:0.82rem;">Subscribe free</a>
        </div>
      </div>
    </div>
  </section>

  <section id="ngn" style="background:var(--bg);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="eyebrow teal">The basics</span><h2>What is the <span class="hl">Next Gen NCLEX (NGN)?</span></h2><p>The NGN is the current version of the exam. It's a better mirror of real nursing &mdash; more clinical judgment, less rote memorization. Here's what changed:</p></div>
      <div class="guide-points fade-up">
        <ul>
          <li>{I['check']} <b>Case studies.</b> Unfolding, six-item cases test how you reason through a real patient. <a href="nclex-complete.html#pricing">See our 50 case studies &rarr;</a></li>
          <li>{I['check']} <b>New item types.</b> Drop-down, matrix, highlight, bow-tie and more. <a href="nclex.html">Try every item type free &rarr;</a></li>
          <li>{I['check']} <b>Partial credit</b> on select-all-that-apply &mdash; miss one option and you still earn most of the points. Good news for test-takers.</li>
          <li>{I['check']} <b>Lab values are given to you.</b> You can look them up, just like at the bedside &mdash; so focus on the <i>meaning</i>, not the number.</li>
          <li>{I['check']} <b>It adapts to you.</b> The exam is computer-adaptive (CAT) &mdash; it changes difficulty as you answer and can end between 75 and 145 questions. <a href="nclex-complete.html">Practice on a real CAT engine &rarr;</a></li>
        </ul>
      </div>
    </div>
  </section>

  <section style="background:var(--card);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="eyebrow">NCLEX 101</span><h2>Your questions, <span class="hl">answered.</span></h2><p>The logistics nobody explains clearly. Tap any card to jump to it.</p></div>
      {guide_cards()}
    </div>
  </section>

  <section style="background:var(--bg);">
    <div class="wrap guide-stack">
      <div class="guide-block fade-up" id="register">
        <h3>How do I register for the NCLEX?</h3>
        <p>Three steps: (1) apply for licensure with your state board of nursing, (2) register for the exam and pay the fee, and (3) wait for your <b>Authorization to Test (ATT)</b> &mdash; then schedule your date and location. Give yourself a buffer; ATTs can take a few weeks.</p>
        <p><a class="btn btn-line" href="#" data-ext>Official registration (add NCSBN link)</a></p>
      </div>
      <div class="guide-block fade-up" id="examday">
        <h3>What's exam day like?</h3>
        <p>Bring your ID and your ATT. You'll be checked in, store your belongings, and test at a computer. The NCLEX is a <b>computer-adaptive test</b> &mdash; each answer shapes the next question, and the exam ends when it's confident about your result (anywhere from 75 to 145 questions). Breathe, read carefully, and trust your preparation.</p>
        <p><a class="btn btn-line" href="nclex-complete.html">Practice in real test format &rarr;</a></p>
      </div>
      <div class="guide-block fade-up" id="fees">
        <h3>How much does the NCLEX cost?</h3>
        <p>The exam itself has a set registration fee paid to the testing service, plus possible state licensure and background-check costs that vary by board. Budget for those separately from prep. Our prep starts at <b>$49</b> &mdash; and includes everything, with Esi.</p>
        <p><a class="btn btn-line" href="nclex-complete.html#pricing">See prep plans &rarr;</a> &nbsp; <a class="btn btn-line" href="#" data-ext>Current exam fee (add link)</a></p>
      </div>
      <div class="guide-block fade-up" id="testplan">
        <h3>What's on the test plan?</h3>
        <p>Every question comes from the official <b>Client Needs</b> categories &mdash; Safe &amp; Effective Care Environment, Health Promotion, Psychosocial Integrity, and Physiological Integrity &mdash; with clinical judgment woven throughout. Our question bank is tagged to these same areas so you always know where you stand.</p>
        <p><a class="btn btn-line" href="nclex-complete.html">See performance by subject area &rarr;</a> &nbsp; <a class="btn btn-line" href="#" data-ext>Official test plan (add link)</a></p>
      </div>
      <div class="guide-block fade-up" id="when">
        <h3>When should I take the NCLEX?</h3>
        <p>Sooner than you think &mdash; most students do best testing <b>4 to 8 weeks after graduation</b>, while the content is fresh. The trick is picking a date that leaves enough runway to fix your weak areas without going stale. That's exactly what our study schedule builds around.</p>
        <p><a class="btn btn-line" href="#study">How long should I study? &rarr;</a></p>
      </div>
      <div class="guide-block fade-up" id="study">
        <h3>How long should I study?</h3>
        <p>It depends on your foundation and your test date. As a rule of thumb: a <b>1-month</b> plan for strong students who mainly need reps, a <b>2-month</b> plan for most people, and a <b>3-month</b> plan if you work full-time or are rebuilding basics. Not sure? Take the 30-second quiz.</p>
        <div class="hero-cta" style="margin-top:0.6rem;">
          <a class="btn btn-coral" href="nclex-complete.html#pricing">Take the plan quiz &rarr;</a>
        </div>
        <div class="plan-links">
          <a href="nclex-complete.html#pricing">1-Month plan</a>
          <a href="nclex-complete.html#pricing">2-Month plan</a>
          <a href="nclex-complete.html#pricing">3-Month plan</a>
          <a href="nclex-complete.html#pricing">6-Month plan</a>
        </div>
      </div>
    </div>
  </section>

  <section style="background:var(--card);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="eyebrow gold">Any advice?</span><h2>Our best <span class="hl">strategy</span> for test day.</h2><p>Reading the question right is half the battle. Two tools do the heavy lifting:</p></div>
      <div class="community">
        <div class="comm-card fade-up">
          <span class="ci" style="background:linear-gradient(140deg,#ffc23d,#8b5cff);">{I['play']}</span>
          <div><h4>Next Gen strategy course</h4><p>Short lessons on how to read a case, spot the answer type, and dodge the traps the test is built on. <a href="nclex-complete.html" style="color:var(--coral-500);font-weight:700;">Explore the course &rarr;</a></p></div>
        </div>
        <div class="comm-card fade-up">
          <span class="ci" style="background:linear-gradient(140deg,#2ad4c4,#1a0942);">{I['shield']}</span>
          <div><h4>Readiness &amp; analyzing tool</h4><p>Full-length readiness exams predict your pass chance and show your weakest subjects, so you always know what to fix next. <a href="nclex-complete.html" style="color:var(--coral-500);font-weight:700;">See the analyzer &rarr;</a></p></div>
        </div>
      </div>
      <div class="soon-band fade-up" style="margin-top:1.6rem;">
        <div>
          <h3>Ready to go all in?</h3>
          <p>NCLEX Complete has the case studies, the question bank, the readiness exams, the schedule, and Esi &mdash; from $59.</p>
        </div>
        <a class="btn btn-coral" href="nclex-complete.html">Explore NCLEX Complete</a>
      </div>
      <p style="text-align:center;margin-top:1.4rem;font-size:0.78rem;color:var(--ink-60);max-width:70ch;margin-left:auto;margin-right:auto;">NCLEX&reg; is a registered trademark of the National Council of State Boards of Nursing, Inc. Must Love Scrubs is not affiliated with or endorsed by NCSBN. This guide is original educational content, not medical or licensing advice &mdash; always confirm current requirements with your state board.</p>
    </div>
  </section>

  <script src="js/complete.js"></script>
"""

PAGES["nclex-guide.html"] = ("Free NCLEX Study Guide — How to Pass, For Nurses By Nurses | Must Love Scrubs",
    "A free NCLEX study guide from Must Love Scrubs: what the Next Gen NCLEX is, how to register, exam day, fees, the test plan, when to test, and how long to study. Question of the Day, plus strategy and readiness tools.",
    GUIDE_BODY, "courses")

# ---------------------------------------------------------------- SPECIALTY PREP (22 tracks, UI shell)

# icon = key in I{}; grad = hero/card gradient; topics = 4 module labels (UI only)
SPECIALTIES = [
    ("med-surg", "Medical-Surgical", "medsurg", "linear-gradient(140deg,#8b5cff,#4d2b9e)", "$59",
     "The broadest floor in nursing — build the systems-based judgment that carries every shift.",
     ["Fluid, electrolyte &amp; acid-base", "Perioperative care", "Multi-system assessment", "Prioritizing a full assignment"]),
    ("emergency", "Emergency / ER", "er", "linear-gradient(140deg,#e5484d,#7a45f0)", "$69",
     "Triage, trauma, and the first ten minutes — think fast and think right under pressure.",
     ["Triage &amp; rapid assessment", "Trauma &amp; resuscitation", "Chest pain &amp; stroke", "Toxicology &amp; overdose"]),
    ("critical-care", "Critical Care / ICU", "icu", "linear-gradient(140deg,#2ad4c4,#1a0942)", "$79",
     "Vents, drips, and unstable patients — the deepest end of bedside reasoning.",
     ["Hemodynamic monitoring", "Ventilator management", "Vasoactive drips", "Sepsis &amp; shock"]),
    ("pediatrics", "Pediatrics", "peds", "linear-gradient(140deg,#ffc23d,#8b5cff)", "$59",
     "Weight-based everything and growing bodies — nursing the smallest patients safely.",
     ["Growth &amp; development", "Pediatric dosing safety", "Respiratory illnesses", "Fluid &amp; dehydration"]),
    ("labor-delivery", "Labor &amp; Delivery / OB", "prenatal", "linear-gradient(140deg,#8b5cff,#14b8a8)", "$69",
     "Two patients at once — read the strip, protect the mom, deliver the baby.",
     ["Fetal monitoring", "Stages of labor", "Preeclampsia &amp; hemorrhage", "Postpartum care"]),
    ("neonatal", "Neonatal / NICU", "peds", "linear-gradient(140deg,#2ad4c4,#4d2b9e)", "$79",
     "Grams, thermoregulation, and fragile beginnings — high-acuity newborn care.",
     ["Newborn assessment", "Thermoregulation", "Preterm complications", "Neonatal resuscitation"]),
    ("oncology", "Oncology", "shield", "linear-gradient(140deg,#7a45f0,#d99a1f)", "$69",
     "Chemo safety, neutropenia, and hard conversations — precise, compassionate care.",
     ["Chemotherapy safety", "Neutropenic precautions", "Oncologic emergencies", "Symptom &amp; pain management"]),
    ("cardiac", "Cardiac / Telemetry", "icu", "linear-gradient(140deg,#e5484d,#2b1055)", "$69",
     "Rhythms, MIs, and heart failure — see the pattern before the alarm.",
     ["ECG rhythm basics", "Acute coronary syndrome", "Heart failure", "Cardiac medications"]),
    ("perioperative", "OR / Perioperative", "medsurg", "linear-gradient(140deg,#4d2b9e,#14b8a8)", "$59",
     "Sterile fields, counts, and time-outs — safety from pre-op to hand-off.",
     ["Surgical asepsis", "Pre-op preparation", "Intra-op safety &amp; counts", "Handoff to PACU"]),
    ("pacu", "PACU / Post-Anesthesia", "icu", "linear-gradient(140deg,#8b5cff,#2ad4c4)", "$59",
     "The riskiest recovery minutes — airway, arousal, and complications after anesthesia.",
     ["Airway &amp; emergence", "Anesthesia complications", "Aldrete scoring", "Pain &amp; nausea control"]),
    ("psychiatric", "Psychiatric / Mental Health", "mental", "linear-gradient(140deg,#7a45f0,#4d2b9e)", "$59",
     "Therapeutic presence and safety — the words and the watchfulness that heal.",
     ["Therapeutic communication", "Suicide &amp; safety", "Psychotropic medications", "Crisis de-escalation"]),
    ("geriatrics", "Geriatrics", "geri", "linear-gradient(140deg,#d99a1f,#7a45f0)", "$49",
     "Polypharmacy, falls, and dignity — nursing the aging adult with care.",
     ["Age-related changes", "Polypharmacy &amp; safety", "Falls &amp; mobility", "Delirium vs dementia"]),
    ("home-health", "Home Health", "home", "linear-gradient(140deg,#14b8a8,#2b1055)", "$49",
     "One nurse, one home — assessment, teaching, and safety without the call bell.",
     ["Home safety assessment", "Wound &amp; IV in the home", "Caregiver teaching", "Care coordination"]),
    ("hospice", "Hospice / Palliative", "prenatal", "linear-gradient(140deg,#8b5cff,#d99a1f)", "$49",
     "Comfort as the goal — symptom relief, presence, and honoring the end of life.",
     ["Pain &amp; symptom management", "Comfort measures", "End-of-life communication", "Family &amp; grief support"]),
    ("rehabilitation", "Rehabilitation", "medsurg", "linear-gradient(140deg,#4d2b9e,#2ad4c4)", "$49",
     "Function over cure — help patients rebuild independence step by step.",
     ["Mobility &amp; transfers", "ADL retraining", "Neuro rehab", "Skin &amp; bladder programs"]),
    ("dialysis", "Dialysis / Nephrology", "pharm", "linear-gradient(140deg,#2ad4c4,#7a45f0)", "$69",
     "Access, fluid, and electrolytes — the rhythm of kidney care.",
     ["AV access care", "Fluid &amp; electrolyte balance", "Dialysis complications", "Renal medications"]),
    ("wound-care", "Wound Care", "shield", "linear-gradient(140deg,#d99a1f,#4d2b9e)", "$59",
     "Stage it, dress it, heal it — the science of skin and tissue repair.",
     ["Pressure injury staging", "Wound assessment", "Dressing selection", "Infection &amp; healing"]),
    ("ambulatory", "Ambulatory / Clinic", "book", "linear-gradient(140deg,#8b5cff,#14b8a8)", "$49",
     "High volume, quick visits — assessment and teaching in the outpatient world.",
     ["Focused assessment", "Immunizations", "Chronic disease teaching", "Triage by phone"]),
    ("school", "School Nursing", "peds", "linear-gradient(140deg,#ffc23d,#4d2b9e)", "$49",
     "One nurse for a whole school — from asthma to emergencies to care plans.",
     ["Common school emergencies", "Chronic conditions at school", "Medication administration", "Health screening"]),
    ("occupational", "Occupational Health", "shield", "linear-gradient(140deg,#14b8a8,#4d2b9e)", "$49",
     "Workplace wellness and injury — prevention, assessment, and return-to-work.",
     ["Workplace injury care", "Exposure &amp; prevention", "Ergonomics", "Return-to-work planning"]),
    ("long-term-care", "Long-Term Care", "geri", "linear-gradient(140deg,#7a45f0,#d99a1f)", "$49",
     "Residents, not room numbers — steady, relationship-based chronic care.",
     ["Chronic condition management", "Skin &amp; wound prevention", "Behavioral care", "Regulatory &amp; documentation"]),
    ("progressive-care", "Progressive Care (PCU)", "icu", "linear-gradient(140deg,#e5484d,#14b8a8)", "$69",
     "A step below the ICU — telemetry, titration, and catching the early turn.",
     ["Telemetry monitoring", "Titratable drips", "Respiratory support", "Recognizing deterioration"]),
]

def specialties_grid():
    cards = []
    for slug, name, icon, grad, price, tag, topics in SPECIALTIES:
        cards.append(f"""<a class="spec-card fade-up" href="specialty-{slug}.html">
          <span class="spec-lock">{I['lock']} In development</span>
          <span class="ic" style="background:{grad};">{I[icon]}</span>
          <h3>{name}</h3>
          <p>{tag}</p>
          <div class="foot"><span class="price">{price}</span><span class="go">Preview &rarr;</span></div>
        </a>""")
    return '<div class="spec-grid">' + "".join(cards) + '</div>'

def build_specialty(slug, name, icon, grad, price, tag, topics):
    chips = "".join(f'<span class="chip">{t}</span>' for t in topics)
    modules = "".join(f"""<div class="pillar fade-up">
          <div class="illo" style="background:{grad};">{I[icon]}</div>
          <span class="kick">Module</span>
          <h3>{t}</h3>
          <p>Full lessons, question sets, and rationales for this area are in development for the {name} track.</p>
        </div>""" for t in topics)
    return f"""  <div class="page-hero" style="background:{grad};">
    <div class="wrap inner">
      <span class="lesson-label" style="color:var(--gold-400);">Specialty Prep &middot; In development</span>
      <h1 style="margin-top:0.6rem;">{name}</h1>
      <p>{tag}</p>
      <div class="spec-hero-tags">{chips}</div>
      <div class="hero-cta" style="margin-top:1.8rem;">
        <a class="btn btn-coral" href="#notify">Notify me when it launches</a>
        <a class="btn btn-ghost" href="specialties.html">All 22 specialties</a>
      </div>
    </div>
  </div>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="eyebrow teal">What you'll master</span><h2>The {name} <span class="hl">track.</span></h2><p>Built on the same retention science as NCLEX Complete &mdash; audio scenes, question sets, and rationales, focused on this specialty. Here's what it will cover.</p></div>
      <div class="pillar-grid">
        {modules}
      </div>
    </div>
  </section>

  <section style="background:var(--card);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="eyebrow">How this track works</span><h2>Learn it once. <span class="hl">Keep it forever.</span></h2></div>
      <div class="tile-grid cols-3">
        <div class="tile fade-up"><span class="tag">Step 1</span><h3>Watch &amp; listen</h3><p>Short specialty scenes drop you onto the unit &mdash; the way a great preceptor would show you.</p></div>
        <div class="tile fade-up"><span class="tag">Step 2</span><h3>Quiz &amp; earn</h3><p>Specialty question sets in every NGN format, with a rationale for every option &mdash; and points as you go.</p></div>
        <div class="tile fade-up"><span class="tag">Step 3</span><h3>Review with Esi</h3><p>Esi tracks your misses in this specialty and drills them until they're strengths.</p></div>
      </div>

      <div class="section-head fade-up" style="margin-top:3rem;"><span class="eyebrow gold">Sneak peek</span><h2>A taste of the <span class="hl">question bank.</span></h2></div>
      <div class="locked-preview fade-up" style="max-width:720px;margin:0 auto;">
        <div class="widget blur">
          <span class="widget-tag">{I['star']} {name} item</span>
          <p class="prompt">Sample {name} scenario &mdash; the client presents with the classic findings your specialty is built to recognize&hellip;</p>
          <div class="choice-grid" style="grid-template-columns:1fr;">
            <button class="choice">Option A &mdash; a plausible distractor</button>
            <button class="choice">Option B &mdash; the correct action</button>
            <button class="choice">Option C &mdash; a plausible distractor</button>
            <button class="choice">Option D &mdash; a plausible distractor</button>
          </div>
        </div>
        <div class="lockmsg">
          <div class="lockbox">
            <span class="lc">{I['lock']}</span>
            <b>Locked &mdash; coming soon</b>
            <p>The {name} question bank is being written now. Join the list and we'll unlock it for you first.</p>
            <a class="btn btn-coral" href="#notify">Notify me</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section id="notify" style="background:var(--bg);">
    <div class="wrap">
      <div class="soon-band fade-up">
        <div>
          <h3>Be first into {name}.</h3>
          <p>We'll email you the moment this specialty track goes live &mdash; often with early-bird pricing from {price}.</p>
        </div>
        <div>
          <form class="soon-form" data-soon onsubmit="return false;">
            <input type="email" placeholder="you@email.com" aria-label="Email">
            <button class="btn btn-coral" type="submit">Notify me</button>
          </form>
          <p class="soon-note" data-soon-done hidden>&check; You're on the list &mdash; we'll be in touch.</p>
        </div>
      </div>
      <p style="text-align:center;margin-top:1.4rem;font-size:0.8rem;color:var(--ink-60);">Prefer the full picture? <a href="specialties.html" style="color:var(--coral-500);font-weight:700;">Browse all 22 specialty tracks &rarr;</a></p>
    </div>
  </section>

  <script src="js/specialty.js"></script>
"""

for _s in SPECIALTIES:
    _slug, _name, _icon, _grad, _price, _tag, _topics = _s
    PAGES[f"specialty-{_slug}.html"] = (
        f"{_name} Specialty Prep (Coming Soon) | Must Love Scrubs",
        f"{_name} specialty nursing prep from Must Love Scrubs — audio scenes, NGN question sets, and rationales. In development; join the list for early access.",
        build_specialty(_slug, _name, _icon, _grad, _price, _tag, _topics), "courses")

PAGES["specialties.html"] = ("Specialty Prep — 22 Nursing Specialties | Must Love Scrubs",
    "Focused NCLEX-style prep for 22 nursing specialties: ER, ICU, Pediatrics, OB, Oncology, Cardiac, and more. Built on proven retention science. Rolling out now.",
    page_hero('The 22 <span class="hl on-dark">specialty tracks</span>.',
              "Passed the NCLEX? Keep going. Focused prep for the specialty you're headed into &mdash; each built on the same retention science as NCLEX Complete. Rolling out now, one specialty at a time.")
    + f"""  <main class="content-block">
    <div class="wrap">
      <div class="section-head fade-up"><span class="eyebrow teal">Any-RN specialties</span><h2>Prep for <span class="hl">where you're going.</span></h2><p>These are the clinical specialties any RN can step into. Tap any track to preview what it will cover &mdash; and get on the list for early access.</p></div>
      {specialties_grid()}
      <div class="points-strip fade-up" style="margin-top:2.4rem;">
        <div class="txt"><b>New tracks are dropping continuously.</b><p>We're building these the right way &mdash; original scenes, question sets, and rationales, one specialty at a time. Owners of NCLEX Complete get first access.</p></div>
        <a class="btn btn-dark" href="nclex-complete.html">Start with NCLEX Complete</a>
      </div>
    </div>
  </main>
""", "courses")

# ---------------------------------------------------------------- NURSE DICTIONARY
import json as _json2
DICT_DATA = _json2.load(open(os.path.join(ROOT, "data", "nurse-dictionary.json"), encoding="utf-8"))

# map the 32 fine categories to a handful of filter groups
DICT_GROUP = {
    "Cardiovascular": "Body systems", "Respiratory": "Body systems", "Neurologic": "Body systems",
    "Renal": "Body systems", "Gastrointestinal": "Body systems", "Endocrine": "Body systems",
    "Hematology": "Body systems", "Immunology": "Body systems", "Oncology": "Body systems",
    "Pharmacology": "Pharmacology", "Medication Administration": "Pharmacology", "Pain Management": "Pharmacology",
    "Labs & Diagnostics": "Labs & values", "Acid-Base": "Labs & values", "Fluids & Electrolytes": "Labs & values",
    "Infection Control": "Safety & infection", "Infection": "Safety & infection", "Safety": "Safety & infection",
    "Assessment": "Fundamentals", "Fundamentals": "Fundamentals", "NCLEX Skills": "Fundamentals",
    "Communication": "Fundamentals", "Mobility": "Fundamentals", "Nutrition": "Fundamentals",
    "Anatomy & Physiology": "Fundamentals",
    "IV Therapy": "Clinical care", "Skin & Wound": "Clinical care", "Emergency": "Clinical care",
    "Maternal-Newborn": "Clinical care", "Palliative & Hospice": "Clinical care",
    "Ethics & Legal": "Professional", "Leadership": "Professional",
}
DICT_GROUPS = ["Body systems", "Pharmacology", "Labs & values", "Safety & infection", "Fundamentals", "Clinical care", "Professional"]

def _esc(t):
    return (t or "").replace('"', '&quot;')

def dict_cards():
    out = []
    def g(e, k):
        v = e.get(k, "")
        return "" if v is None else str(v).strip()
    for e in sorted(DICT_DATA, key=lambda x: str(x["Term"]).lower()):
        term = g(e, "Term"); defn = g(e, "Plain-Language Definition")
        cat = g(e, "Category") or "Fundamentals"; grp = DICT_GROUP.get(cat, "Fundamentals")
        abbr = g(e, "Abbreviation / Expansion")
        rel = g(e, "Related Terms")
        kw = (g(e, "Search Keywords") + " " + term + " " + defn + " " + cat).lower().replace('"', "")
        example = g(e, "Real-World Example")
        abbr_html = f'<span class="term-abbr">{abbr}</span>' if abbr else ""
        rel_html = f'<span class="term-rel">Related: {rel}</span>' if rel else ""
        ex_html = f'<div class="term-ex"><b>{I["star"]} On the floor.</b> {example}</div>' if example else ""
        hi = ' data-hi="1"' if e.get("NCLEX Relevance") == "High" else ""
        out.append(f"""<div class="term-card" data-cat="{grp}" data-search="{_esc(kw)}"{hi}>
          <div class="term-top"><span class="term">{term}</span><span class="term-cat">{cat}</span></div>
          {abbr_html}
          <p>{defn}</p>
          {ex_html}
          {rel_html}
        </div>""")
    return "".join(out)

def dict_chips():
    out = ['<button class="chip-filter on" data-cat="all">All</button>']
    for c in DICT_GROUPS:
        out.append(f'<button class="chip-filter" data-cat="{c}">{c}</button>')
    return "".join(out)

DICT_BODY = f"""  <div class="page-hero">
    <div class="wrap inner">
      <span class="lesson-label" style="color:var(--gold-400);">Free tool</span>
      <h1 style="margin-top:0.6rem;">The Nurses <span class="em">Index</span>.</h1>
      <p>Every term, abbreviation, and bit of nurse-speak &mdash; in plain language. Search it, filter it, learn it. Free to search, forever, and always growing.</p>
    </div>
  </div>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="dict-tools fade-up">
        <div class="dict-search">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
          <input type="search" placeholder="Search a term or abbreviation&hellip;" aria-label="Search the dictionary">
        </div>
        <div class="dict-chips">{dict_chips()}</div>
        <p class="dict-count">{len(DICT_DATA)} terms</p>
      </div>
      <div class="dict-grid">{dict_cards()}</div>
      <div class="dict-empty">
        <p><b>No match yet.</b> This dictionary grows every week &mdash; tell us what to add at hello@mustlovescrubs.com.</p>
      </div>
    </div>
  </section>

  <section id="download" style="background:var(--card);">
    <div class="wrap">
      <div class="course-hero fade-up" style="box-shadow:var(--shadow-2);">
        <div class="art" style="background:url(images/dictionary.jpg) center/cover no-repeat, radial-gradient(circle at 70% 25%, rgba(255,201,77,0.4), transparent 50%), radial-gradient(circle at 20% 80%, rgba(20,184,168,0.5), transparent 55%), linear-gradient(150deg,#2b1055,#4d2b9e);"></div>
        <div class="body">
          <div class="chip-row"><span class="chip gold">Download</span><span class="chip teal">Example + rationale for every term</span></div>
          <h3>Take the whole dictionary with you.</h3>
          <p>The download goes deeper than the free search: every word paired with a <b>real clinical example</b> and a <b>rationale</b> &mdash; same lane as a question bank, a different way to learn and retain.</p>
          <div class="price-line"><span class="price">$4.99</span><span class="per">one-time</span></div>
          <div class="chip-row"><span class="chip">Unlock with points</span><span class="chip">Free with any course</span></div>
          <div class="hero-cta" style="margin-top:0.4rem;"><a class="btn btn-coral" href="join.html">Unlock with points</a><a class="btn btn-line" href="store.html">Buy for $4.99</a></div>
        </div>
      </div>

      <div class="section-head fade-up" style="margin-top:2.6rem;"><span class="eyebrow gold">See what you're paying for</span><h2>Same term. <span class="hl">Two depths.</span></h2><p>Here's the exact difference between the free search and the paid download &mdash; using one real term.</p></div>
      <div class="compare-grid fade-up">
        <div class="compare-col free">
          <span class="ctag">Free search</span>
          <b class="cterm">Hyperkalemia</b>
          <p class="cdef">A higher-than-normal level of potassium in the blood (above ~5.0 mEq/L). Can affect the heart's rhythm.</p>
        </div>
        <div class="compare-col paid">
          <span class="ctag paid">Paid download &middot; with bonus</span>
          <b class="cterm">Hyperkalemia</b>
          <p class="cdef">A higher-than-normal level of potassium in the blood (above ~5.0 mEq/L). Can affect the heart's rhythm.</p>
          <div class="cbonus">
            <p><b>{I['star']} Real-world nurse situation (the bonus).</b> Mr. Alvarez, post-op day 2 with kidney injury, has a potassium of 6.8 and tall, peaked T waves on the monitor. His nurse holds all potassium, places him on a cardiac monitor, and calls the provider &mdash; anticipating IV calcium to protect the heart.</p>
            <p><b>{I['check']} Built-in context clues.</b> Your brain remembers stories, not definitions. Seeing the term <i>in a scene</i> &mdash; the patient, the monitor, the action &mdash; gives you the context clues that make it stick on test day and on the floor.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section style="background:var(--bg);">
    <div class="wrap" style="text-align:center;">
      <div class="section-head fade-up" style="margin-inline:auto;"><span class="lesson-label" style="color:var(--teal-600);">Stuck on a term?</span><h2>Esi can explain <span class="em">anything</span>.</h2><p style="margin-inline:auto;">Every definition here is free. For a term walked through your way &mdash; with examples and a quick check &mdash; Esi is one tap away.</p></div>
      <a class="btn btn-coral" href="esi.html">Meet Esi</a>
    </div>
  </section>

  <script src="js/dictionary.js"></script>
"""

PAGES["dictionary.html"] = ("Nurses Index &mdash; Must Love Scrubs",
    "A free, searchable dictionary of 217+ nursing and medical terms, abbreviations, and plain-language definitions. Download with examples and rationales.",
    DICT_BODY, "dictionary")

# ================================================================ COURSE TEMPLATE
# A course is data. Modules: audio scene (+curated video) -> memory game ->
# matrix memory test -> chart test -> quiz (+SATA). Add a dict = add a course.

def _scene(lines):
    return "".join(f'<div class="line {w}"><span class="spk">{s}</span><p>{t}</p></div>' for w, s, t in lines)

def _memory(cards):
    faces = ["f1", "f2", "f3"]
    out = []
    for i, (tag, front, back) in enumerate(cards):
        out.append(f"""<div class="flip fade-up" tabindex="0" role="button" aria-label="Reveal card {i+1}">
          <div class="flip-inner">
            <div class="flip-face flip-front {faces[i%3]}"><span class="idx">0{i+1}</span><span class="tag">{tag}</span><h3>{front}</h3><span class="cue">Tap to reveal &rarr;</span></div>
            <div class="flip-face flip-back"><span class="bk-tag">{tag}</span><p>{back}</p></div>
          </div></div>""")
    return '<div class="carry-grid">' + "".join(out) + '</div>'

def _matrix(m):
    rows = "".join(
        f'<tr data-answer="{ans}"><td>{find}</td><td class="mcell"><button data-col="exp" aria-label="{m["c1"]}"></button></td><td class="mcell"><button data-col="rep" aria-label="{m["c2"]}"></button></td></tr>'
        for find, ans in m["rows"])
    return f"""<div class="widget matrix-item fade-up"><span class="widget-tag">Matrix memory test</span>
      <p class="prompt">{m['q']}</p>
      <div class="matrix-scroll"><table class="matrix"><thead><tr><th>{m['head']}</th><th>{m['c1']}</th><th>{m['c2']}</th></tr></thead><tbody>{rows}</tbody></table></div>
      <div class="quiz-actions" style="margin-top:1.2rem;"><button class="btn btn-coral matrix-check">Check the grid</button><span class="matrix-result" hidden style="font-weight:800;color:var(--teal-600);"><b></b></span></div></div>"""

def _chart(ch):
    head = "".join(f"<th>{h}</th>" for h in ch["cols"])
    body = []
    flag_cls = ' class="flag"'
    for r_i, row in enumerate(ch["rows"]):
        cells = ""
        for c_i, v in enumerate(row):
            fc = flag_cls if (r_i in ch.get("flag_rows", []) and c_i > 0) else ""
            cells += f"<td{fc}>{v}</td>"
        body.append(f"<tr>{cells}</tr>")
    opts = "".join(f'<button class="choice" data-correct="{c}">{t}</button>' for t, c in ch["opts"])
    return f"""<div class="widget mc-item fade-up"><span class="widget-tag">Chart &amp; trend test</span>
      <p class="prompt">{ch['q']}</p>
      <div class="trend-scroll"><table class="trend-table"><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>
      <div class="choice-grid" style="grid-template-columns:1fr;">{opts}</div>
      <div class="quiz-actions" style="margin-top:1.2rem;"><button class="btn btn-coral mc-check">Check answer</button></div>
      <div class="rationale" style="background:var(--bg);border-left:3px solid var(--teal-600);color:var(--ink);"><b style="color:var(--teal-600);">Why:</b><p style="color:var(--ink-60);">{ch['rationale']}</p></div></div>"""

def _quiz(quiz):
    L = "ABCDE"
    out = []
    for qi, (q, opts, rat) in enumerate(quiz, 1):
        ob = "".join(f'<button class="opt" data-correct="{c}"><span class="k">{L[i]}</span><span>{t}</span></button>' for i, (t, c) in enumerate(opts))
        out.append(f"""<div class="quiz-card" style="margin-bottom:2.5rem;"><div class="quiz-head"><span>Clinical quick check</span><span>Question {qi} of {len(quiz)}</span></div>
          <p class="quiz-q">{q}</p><div class="opts">{ob}</div>
          <div class="quiz-actions"><button class="btn btn-coral check-btn">Check answer</button></div>
          <div class="rationale"><b>Why:</b><p>{rat}</p></div></div>""")
    return "".join(out)

def _sata(s):
    if not s:
        return ""
    ob = "".join(f'<button class="opt" data-correct="{c}"><span class="box"></span><span>{t}</span></button>' for t, c in s["opts"])
    return f"""<div class="quiz-card sata" style="margin-bottom:2.5rem;"><div class="quiz-head"><span>Clinical quick check</span><span>Select all that apply</span></div>
      <span class="sata-tag">Next Gen NCLEX &middot; SATA</span><p class="quiz-q">{s['q']}</p>
      <div class="opts">{ob}</div>
      <div class="quiz-actions"><button class="btn btn-coral check-btn">Check answer</button></div>
      <div class="rationale"><b>Why:</b><p>{s['rationale']}</p></div></div>"""

PATTERN_RUN = ("<span>Don't memorize a list. <em>Build a pattern.</em></span>") * 4

def build_course(c):
    ctx = "".join(f'<span class="c">{x}</span>' for x in c["context"])
    return f"""  <div class="page-hero">
    <div class="wrap inner">
      <a href="scrubtv.html" style="color:rgba(255,255,255,0.7);font-size:0.85rem;font-weight:700;">&larr; Back to Scrub TV</a>
      <p class="lesson-kicker" style="margin-top:1.4rem;">{c['kicker']}</p>
      <span class="lesson-label" style="color:var(--gold-400);">{c['tag']}</span>
      <h1 style="margin-top:0.6rem;">{c['title']} <span class="em">{c['title_em']}</span></h1>
      <p>{c['intro']}</p>
    </div>
  </div>

  <div class="pattern-strip" aria-hidden="true"><div class="run">{PATTERN_RUN}</div></div>

  <section class="scene-band">
    <div class="wrap">
      <div class="section-head fade-up" style="margin-bottom:1.4rem;"><span class="lesson-label">The scene</span><h2 style="color:#fff;">{c['scene_title']}</h2></div>
      <div class="scene-visual fade-up">
        <div class="sv-thumb" style="background:{c['grad']};"><span class="sv-play">{I['play']}</span></div>
        <span class="sv-note">Curated visual &mdash; sets the scene, not the exact case. (Sourced video drops in here.)</span>
      </div>
      <div class="player">
        <div class="player-main fade-up">
          <div class="scene-context">{ctx}</div>
          <div class="play-row">
            <button class="play-btn" aria-label="Play the scene"><span class="play-ico">{I['play']}</span><span class="pause-ico"><svg viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg></span></button>
            <div class="waveform" aria-hidden="true">{waveform_bars()}</div>
          </div>
          <div class="time-row"><span class="cur-time">0:00</span><span>{c['runtime']}</span></div>
          <p class="audio-note">Audio is swap-ready &mdash; real recorded / AI-voiced scene drops in here.</p>
          <div class="unlock-note">{I['check']} Scene complete</div>
        </div>
        <div class="transcript fade-up" aria-label="Transcript">{_scene(c['scene'])}</div>
      </div>
    </div>
  </section>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="lesson-label">Memory game</span><h2>{c['mem_head']}</h2><p>Tap a card when you're ready to test what stuck. No passive scrolling here.</p></div>
      {_memory(c['memory'])}
    </div>
  </section>

  <section style="background:var(--card);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="lesson-label">Matrix memory test</span><h2>{c['matrix_head']}</h2></div>
      {_matrix(c['matrix'])}
    </div>
  </section>

  <section style="background:var(--bg);">
    <div class="wrap">
      <div class="section-head fade-up"><span class="lesson-label">Chart test</span><h2>{c['chart_head']}</h2></div>
      {_chart(c['chart'])}
    </div>
  </section>

  <section class="quiz-band">
    <div class="wrap">
      <div class="section-head fade-up"><span class="lesson-label" style="color:var(--gold-400);">Clinical quick check</span><h2 style="color:#fff;">Now &mdash; <span class="em" style="color:var(--gold-400);">make the call</span>.</h2></div>
      {_quiz(c['quiz'])}{_sata(c.get('sata'))}
      <div class="result-reveal" hidden>
        <div class="result-card">
          <span class="lesson-label" style="color:var(--teal-600);">Lesson complete</span>
          <div class="score"><span data-quiz-score>0/0</span></div>
          <span class="pts-won">{I['star']} <span data-pts-won>points earned</span></span>
          <p class="review">Esi: &ldquo;<b>I'll re-test you in 3 days</b> &mdash; that's right when this starts to fade. Build the pattern, don't cram the list.&rdquo;</p>
          <a class="btn btn-coral" href="join.html" style="margin-top:1.6rem;">Save my progress (free account)</a>
        </div>
        <div style="height:1.2rem;"></div>
        <div class="next-up"><span class="ic">{I['play']}</span><div><small>Next free lesson</small><b>{c['next']}</b></div><a class="btn btn-line go" href="scrubtv.html">Browse &rarr;</a></div>
      </div>
    </div>
  </section>

  <section style="background:var(--bg);">
    <div class="wrap" style="text-align:center;">
      <div class="section-head fade-up" style="margin-inline:auto;"><span class="lesson-label">Keep the momentum</span><h2>Small sessions. <span class="em">Serious growth.</span></h2><p style="margin-inline:auto;">This lesson is free forever. Prepping a specialty? The full paid courses go deeper on {c['upsell']}.</p></div>
      <a class="btn btn-coral" href="courses.html">See specialty prep</a>
    </div>
  </section>

  <script src="js/course.js"></script>
  <script src="js/prep.js"></script>
"""

COURSES = [
  {
    "slug": "course-lab-values.html", "num": "01",
    "kicker": "Foundations &middot; ~14 min &middot; Free", "tag": "Scrub TV &middot; Lesson 01",
    "title": "When the lab calls at", "title_em": "3 a.m.",
    "intro": "A full free lesson on critical lab values. Hear the scene, lock in the six that save lives, then prove it &mdash; memory game, matrix, chart, and a clinical quick check.",
    "grad": "linear-gradient(135deg,#4d2b9e,#14b8a8)", "runtime": "6:12",
    "scene_title": "Room 4. Post-op day two.",
    "context": ["ER &middot; Night shift", "68-year-old male", "Post-op day 2"],
    "scene": [
      ("other", "Lab", "Night shift, this is the lab &mdash; critical value on your Room 4."),
      ("nurse", "You", "Go ahead, I'm listening."),
      ("other", "Lab", "Potassium is 6.8. Repeat, six-point-eight. Read back, please."),
      ("nurse", "You", "Critical potassium 6.8 on Room 4 &mdash; read back confirmed."),
      ("nurse", "You", "<em>Mr. Alvarez, 68, post-op day two. He said his legs felt heavy.</em>"),
      ("other", "Pt", "My heart's... doing a funny flutter. And I'm so weak."),
      ("nurse", "You", "<em>Weakness. Palpitations. A potassium of 6.8. My mind goes to his heart.</em>"),
      ("nurse", "You", "I'm getting you on the monitor and grabbing a 12-lead right now."),
    ],
    "mem_head": 'Three things to <span class="em">carry with you</span>.',
    "memory": [
      ("Recognize", "A number is a story.", "K&#8314; 6.8 is hyperkalemia (normal 3.5&ndash;5.0). Warnings: weakness, palpitations, peaked T waves."),
      ("Prioritize", "Protect the heart first.", "Cardiac stability beats everything. Monitor + 12-lead ECG now. High potassium kills through the heart."),
      ("Act", "Stop, check, escalate.", "Hold potassium, notify the provider (SBAR), anticipate calcium to protect, insulin+D50 to shift, kayexalate/dialysis to remove."),
    ],
    "matrix_head": 'Which results <span class="em">demand action</span> now?',
    "matrix": {"q": "For each lab, decide: expected/normal, or act now?", "head": "Lab result", "c1": "Expected", "c2": "Act now",
      "rows": [("Potassium 6.8 mEq/L", "rep"), ("Sodium 139 mEq/L", "exp"), ("Glucose 45 mg/dL", "rep"), ("Calcium 9.5 mg/dL", "exp"), ("Magnesium 1.2 mg/dL", "rep")]},
    "chart_head": 'Read the <span class="em">glucose</span> trend.',
    "chart": {"q": "A diabetic patient's glucose over the shift. What's your priority?", "cols": ["Time", "Glucose", "Alert?"], "flag_rows": [2],
      "rows": [["08:00", "142 mg/dL", "&mdash;"], ["12:00", "88 mg/dL", "&mdash;"], ["16:00", "45 mg/dL", "Confused, shaky"]],
      "opts": [("Treat now with 15 g fast-acting carbohydrate, then recheck in 15 min", 1), ("Give the next scheduled insulin dose", 0), ("Document and reassess in 30 minutes", 0), ("Encourage a high-protein snack", 0)],
      "rationale": "Symptomatic hypoglycemia is an emergency &mdash; <b>treat first</b> with 15 g fast carbs, recheck in 15. Never give insulin or wait when the brain is starving for glucose."},
    "quiz": [
      ("K&#8314; 6.8 with new palpitations and weakness. Priority?", [("Document and reassess in 30 minutes", 0), ("Cardiac monitor + 12-lead ECG", 1), ("Encourage potassium-rich foods", 0), ("Ask family if weakness is baseline", 0)], "Hyperkalemia is dangerous to the <b>heart</b> &mdash; monitor and ECG first."),
      ("IV calcium gluconate's role in hyperkalemia?", [("Lowers potassium directly", 0), ("Stabilizes the cardiac membrane to protect the heart", 1), ("Shifts potassium into cells", 0), ("Removes potassium from the body", 0)], "Calcium <b>protects the heart</b>; it doesn't lower the level."),
      ("Normal potassium range?", [("1.5&ndash;2.5", 0), ("3.5&ndash;5.0 mEq/L", 1), ("8.5&ndash;10.5", 0), ("135&ndash;145", 0)], "3.5&ndash;5.0 &mdash; the banana that costs $3.50 to $5.00."),
      ("Furosemide is started. Which electrolyte drops?", [("Sodium", 0), ("Potassium", 1), ("Calcium", 0), ("Magnesium only", 0)], "Loop diuretics waste <b>potassium</b> &mdash; watch for hypokalemia and U waves."),
      ("Sodium 118. Most concerned about?", [("Seizures and altered mental status", 1), ("Peaked T waves", 0), ("Positive Chvostek sign", 0), ("Kussmaul respirations", 0)], "Severe hyponatremia causes cerebral edema &mdash; headache, confusion, <b>seizures</b>."),
    ],
    "sata": {"q": "Potassium is 6.8. Which actions are appropriate? Select all that apply.",
      "opts": [("Place on a cardiac monitor", 1), ("Hold all oral and IV potassium", 1), ("Notify the provider", 1), ("Offer a banana for energy", 0), ("Prepare IV calcium gluconate", 1)],
      "rationale": "Four are right. Offering a banana <b>adds</b> potassium &mdash; exactly wrong. SATA is all-or-nothing."},
    "next": "Prioritization &amp; Delegation", "upsell": "renal, cardiac &amp; critical care",
  },
  {
    "slug": "course-prioritization.html", "num": "02",
    "kicker": "Foundations &middot; ~12 min &middot; Free", "tag": "Scrub TV &middot; Lesson 02",
    "title": "Four patients.", "title_em": "One of you.",
    "intro": "The heart of the NCLEX: who do you see first, and what can you hand off? Learn to think in ABCs, acuity, and safe delegation &mdash; then prove it.",
    "grad": "linear-gradient(135deg,#2b1055,#8b5cff)", "runtime": "5:40",
    "scene_title": "0700. Shift change.",
    "context": ["Med-Surg", "4-patient assignment", "Start of shift"],
    "scene": [
      ("other", "RN", "Here's your handoff &mdash; four patients, and the aide's with you till noon."),
      ("nurse", "You", "Give me the headlines. Who's least stable?"),
      ("other", "RN", "Room 1: stable, waiting on discharge. Room 2: new onset shortness of breath."),
      ("nurse", "You", "<em>Shortness of breath &mdash; that's airway and breathing. Room 2 is first.</em>"),
      ("other", "RN", "Room 3: post-op, pain 3 and improving. Room 4: fresh admit, needs assessment."),
      ("nurse", "You", "<em>Improving pain can wait. A new admit needs my eyes, not the aide's.</em>"),
      ("nurse", "You", "I'll see Room 2 now, then the new admit. Aide takes stable vitals and the discharge walk."),
      ("nurse", "You", "<em>ABCs first. Unstable before stable. Delegate the routine, keep the judgment.</em>"),
    ],
    "mem_head": 'Three rules to <span class="em">see first</span> by.',
    "memory": [
      ("Airway first", "ABCs win.", "Airway, Breathing, Circulation always outrank comfort. New shortness of breath, choking, or a failing airway is always your first stop."),
      ("Acuity", "Unstable beats stable.", "Acute, new, or unstable comes before chronic, expected, or improving. A changing patient beats a comfortable one."),
      ("Delegate", "Keep the judgment.", "Delegate stable, routine, predictable tasks (vitals, ADLs, ambulating stable patients). Assessment, teaching, and unstable patients stay with the RN."),
    ],
    "matrix_head": 'Can you <span class="em">delegate</span> it to the aide (UAP)?',
    "matrix": {"q": "For each task, decide: delegate to the UAP, or RN only?", "head": "Task", "c1": "Delegate", "c2": "RN only",
      "rows": [("Vital signs on a stable patient", "exp"), ("Initial assessment of a new admit", "rep"), ("Ambulate a stable post-op patient", "exp"), ("Teach a new diabetic about insulin", "rep"), ("Feed a stable patient", "exp"), ("Evaluate a patient's response to a new med", "rep")]},
    "chart_head": 'Who do you see <span class="em">first</span>?',
    "chart": {"q": "Four patients at 0700. Based on this board, who is your priority?", "cols": ["Room", "Status", "Key finding"], "flag_rows": [1],
      "rows": [["1", "Stable", "Awaiting discharge"], ["2", "New", "SpO&#8322; 89%, new dyspnea"], ["3", "Post-op", "Pain 3/10, improving"], ["4", "Admit", "Vitals stable, needs H&amp;P"]],
      "opts": [("Room 2 &mdash; new dyspnea with low SpO&#8322; is an airway/breathing threat", 1), ("Room 1 &mdash; get the discharge moving", 0), ("Room 3 &mdash; treat the pain", 0), ("Room 4 &mdash; the admit paperwork is overdue", 0)],
      "rationale": "New dyspnea with SpO&#8322; 89% is an <b>ABC</b> problem &mdash; breathing beats discharge, pain, and paperwork every time."},
    "quiz": [
      ("Which patient should the nurse assess first?", [("A patient with chronic, stable COPD", 0), ("A patient with new confusion and RR 30", 1), ("A patient due for routine AM meds", 0), ("A patient asking about discharge", 0)], "New confusion + high RR is acute deterioration &mdash; <b>ABCs and change</b> come first."),
      ("Which task is appropriate to delegate to a UAP?", [("Assessing a new admission", 0), ("Bathing a stable patient", 1), ("Teaching wound care", 0), ("Evaluating a PRN pain med", 0)], "UAPs do stable, routine, predictable care. <b>Assessment, teaching, and evaluation</b> stay with the RN."),
      ("Using Maslow, which need comes first?", [("Belonging &mdash; the patient feels lonely", 0), ("Physiologic &mdash; the patient can't breathe", 1), ("Self-esteem &mdash; the patient feels embarrassed", 0), ("Safety &mdash; the bed alarm is off", 0)], "Physiologic needs (airway, breathing, circulation) sit at the base of Maslow &mdash; they come first."),
      ("Two patients need you now. Which is the priority?", [("Expected post-op incision pain", 0), ("New, sudden chest pain with diaphoresis", 1), ("A dietary complaint", 0), ("A request for a warm blanket", 0)], "New, sudden chest pain with sweating is a possible cardiac emergency &mdash; <b>acute and unstable</b> wins."),
      ("Which is the RN's non-delegable responsibility?", [("Recording intake and output", 0), ("The initial nursing assessment", 1), ("Ambulating a stable patient", 0), ("Stocking supplies", 0)], "The <b>initial assessment</b> (and care planning, teaching, evaluation) is the RN's alone."),
    ],
    "sata": {"q": "Which tasks can be delegated to a UAP? Select all that apply.",
      "opts": [("Taking vital signs on stable patients", 1), ("Assisting with feeding", 1), ("Performing the admission assessment", 0), ("Ambulating a stable patient", 1), ("Teaching about a new medication", 0)],
      "rationale": "Stable, routine tasks delegate. <b>Assessment and teaching</b> require an RN &mdash; every time."},
    "next": "Medication Safety", "upsell": "med-surg, ER &amp; leadership",
  },
  {
    "slug": "course-med-safety.html", "num": "03",
    "kicker": "Foundations &middot; ~12 min &middot; Free", "tag": "Scrub TV &middot; Lesson 03",
    "title": "The catch before", "title_em": "the harm.",
    "intro": "Most med errors are caught by a nurse who slowed down. Learn the rights, the high-alert drugs, and the stop-signs &mdash; then prove you'd catch it too.",
    "grad": "linear-gradient(135deg,#4d2b9e,#ffb038)", "runtime": "5:20",
    "scene_title": "The medication room.",
    "context": ["Med-Surg", "0900 med pass", "Two patients, same last name"],
    "scene": [
      ("nurse", "You", "<em>Two Johnsons on the unit today. That's exactly how the wrong-patient errors happen.</em>"),
      ("other", "Pt", "You can just leave the pills, honey, I know which are mine."),
      ("nurse", "You", "I hear you &mdash; but I check the band every time. Two identifiers, no exceptions."),
      ("nurse", "You", "<em>Name and date of birth. Scan the band. Now I know it's really her.</em>"),
      ("nurse", "You", "This one's insulin &mdash; high-alert. I want a second nurse to verify the dose."),
      ("other", "RN", "Verified: 6 units, matches the order."),
      ("nurse", "You", "<em>Right patient, right drug, right dose, right route, right time. Then I document.</em>"),
      ("nurse", "You", "Slowing down for ten seconds is how nobody gets hurt."),
    ],
    "mem_head": 'Three habits that <span class="em">prevent harm</span>.',
    "memory": [
      ("The Rights", "Check every one.", "Right patient, drug, dose, route, time &mdash; plus right documentation, reason, and response. Skip one and you've opened the door to harm."),
      ("High-alert", "Slow down for these.", "Insulin, heparin/anticoagulants, opioids, and concentrated electrolytes (like IV potassium) cause the most serious errors. Many need an independent double-check."),
      ("Two IDs", "Every time.", "Two identifiers (name + date of birth), and scan the band. \"I know which are mine\" is never an identifier."),
    ],
    "matrix_head": 'Safe to give, or <span class="em">stop</span>?',
    "matrix": {"q": "For each situation, decide: safe to proceed, or stop?", "head": "Situation", "c1": "Safe", "c2": "Stop",
      "rows": [("Insulin dose verified by a second nurse", "exp"), ("Heparin given without an independent double-check", "rep"), ("Med left at the bedside without checking the band", "rep"), ("Metoprolol held for a heart rate of 46", "exp"), ("An extended-release tablet crushed to give via tube", "rep")]},
    "chart_head": 'Read the <span class="em">INR</span> trend.',
    "chart": {"q": "A patient on warfarin. Their INR over three days. What's your action?", "cols": ["Day", "INR", "Note"], "flag_rows": [2],
      "rows": [["Mon", "2.1", "Therapeutic"], ["Wed", "3.4", "Rising"], ["Fri", "5.8", "Gums bleeding"]],
      "opts": [("Hold the warfarin, notify the provider, anticipate vitamin K", 1), ("Give the next warfarin dose as scheduled", 0), ("Increase the warfarin dose", 0), ("Document and reassess next week", 0)],
      "rationale": "An INR of 5.8 with bleeding is dangerously high &mdash; <b>hold the warfarin</b>, notify the provider, and anticipate vitamin K. The trend and the bleeding both scream stop."},
    "quiz": [
      ("Before giving a medication, how many patient identifiers are required?", [("One is enough if you know the patient", 0), ("Two independent identifiers", 1), ("The room number", 0), ("The patient's word", 0)], "Always <b>two identifiers</b> (name + DOB), and scan the band."),
      ("Which is considered a high-alert medication?", [("Acetaminophen", 0), ("Insulin", 1), ("A stool softener", 0), ("A saline flush", 0)], "Insulin, heparin, opioids, and concentrated electrolytes are <b>high-alert</b> &mdash; slow down and double-check."),
      ("The heart rate is 46 before a dose of metoprolol. The nurse should:", [("Give it as ordered", 0), ("Hold it and notify the provider", 1), ("Double the dose", 0), ("Give half the dose", 0)], "Beta-blockers are held for bradycardia &mdash; <b>hold and notify</b> when the HR is below the parameter."),
      ("A capsule is labeled extended-release. The patient has a feeding tube. The nurse should:", [("Open and crush it into the tube", 0), ("Call the pharmacy for a suitable form", 1), ("Give it whole and hope it passes", 0), ("Skip it entirely without telling anyone", 0)], "Crushing extended-release drugs can cause a dangerous dose dump &mdash; <b>ask pharmacy</b> for an appropriate formulation."),
      ("Two patients share a last name. The safest action is to:", [("Ask which pills are theirs", 0), ("Verify two identifiers and scan the band", 1), ("Use the room number", 0), ("Trust the assignment sheet", 0)], "Same-name patients are a classic error trap &mdash; <b>two identifiers and the band scan</b> every time."),
    ],
    "sata": {"q": "Which of these are high-alert medications? Select all that apply.",
      "opts": [("Insulin", 1), ("Heparin", 1), ("Docusate (stool softener)", 0), ("IV concentrated potassium", 1), ("Hydromorphone (an opioid)", 1)],
      "rationale": "Insulin, heparin, concentrated electrolytes, and opioids are high-alert. A stool softener is low-risk."},
    "next": "Spot the Deterioration", "upsell": "pharmacology, ICU &amp; med-surg",
  },
  {
    "slug": "course-deterioration.html", "num": "04",
    "kicker": "Foundations &middot; ~12 min &middot; Free", "tag": "Scrub TV &middot; Lesson 04",
    "title": "See it coming.", "title_em": "Before it spirals.",
    "intro": "Patients rarely crash without warning &mdash; they whisper first. Learn the subtle early signs, trust the trend, and escalate before it's an emergency.",
    "grad": "linear-gradient(135deg,#2b1055,#e5484d)", "runtime": "5:30",
    "scene_title": "Room 7. Something's off.",
    "context": ["Med-Surg", "Evening", "Post-op day 1"],
    "scene": [
      ("nurse", "You", "<em>She was chatty this morning. Now she's quiet, picking at the sheets.</em>"),
      ("other", "Pt", "I'm fine... just can't get comfortable. And I'm a little short of breath."),
      ("nurse", "You", "Let me get a set of vitals. Stay with me."),
      ("nurse", "You", "<em>Respirations 26, up from 16. Heart rate creeping. She's restless.</em>"),
      ("nurse", "You", "<em>No single number is screaming &mdash; but the trend is. That's the whisper before the crash.</em>"),
      ("nurse", "You", "I'm calling the rapid response team now. I'd rather be early than sorry."),
      ("other", "RN", "Good call. What's your SBAR?"),
      ("nurse", "You", "<em>Escalate early. Nobody was ever harmed by a nurse who called too soon.</em>"),
    ],
    "mem_head": 'Three signs to <span class="em">trust early</span>.',
    "memory": [
      ("Trend", "Direction over numbers.", "One vital sign can be noise. A trend &mdash; rising RR and HR, falling BP and SpO&#8322; over hours &mdash; is the story. Chart it and watch the direction."),
      ("Subtle", "Restlessness first.", "The earliest sign of deterioration is often a rising respiratory rate or a subtle mental-status change &mdash; restlessness, confusion, \"just not right.\" Believe it."),
      ("Escalate", "Call early.", "When the pattern points down, escalate with SBAR and call the rapid response team. Early is always better than late &mdash; you can't un-crash a patient."),
    ],
    "matrix_head": 'Escalate now, or <span class="em">keep watching</span>?',
    "matrix": {"q": "For each finding, decide: escalate now, or monitor?", "head": "Finding", "c1": "Monitor", "c2": "Escalate",
      "rows": [("RR 28, up from 16 an hour ago", "rep"), ("SpO&#8322; 91% on room air, was 98%", "rep"), ("Pain 3/10, steadily improving", "exp"), ("New confusion and restlessness", "rep"), ("Blood pressure 96/58, trending down", "rep"), ("Stable vitals, resting comfortably", "exp")]},
    "chart_head": 'Read the <span class="em">deterioration</span>.',
    "chart": {"q": "Your patient's vitals over 8 hours. What is your priority interpretation?", "cols": ["Time", "HR", "BP", "Temp", "RR", "SpO&#8322;"], "flag_rows": [2],
      "rows": [["08:00", "88", "122/78", "37.0", "16", "98%"], ["12:00", "104", "108/66", "38.4", "22", "95%"], ["16:00", "122", "94/54", "39.1", "28", "91%"]],
      "opts": [("Rising HR/RR/temp with falling BP &amp; SpO&#8322; &mdash; early sepsis. Escalate.", 1), ("Expected recovery &mdash; keep routine monitoring", 0), ("Anxiety &mdash; offer reassurance", 0), ("Dehydration &mdash; offer oral fluids", 0)],
      "rationale": "Up in HR, RR, and temp while BP and SpO&#8322; fall is the classic <b>sepsis / deterioration</b> pattern. The direction matters more than any one number &mdash; escalate early."},
    "quiz": [
      ("What is often the earliest sign of clinical deterioration?", [("A rising respiratory rate", 1), ("A drop in temperature", 0), ("Increased appetite", 0), ("Lower heart rate", 0)], "A <b>rising respiratory rate</b> (and subtle mental-status change) is often the first, earliest warning."),
      ("A patient becomes restless and confused with RR 30. The nurse should:", [("Reassure and recheck in an hour", 0), ("Assess, take vitals, and escalate", 1), ("Document only", 0), ("Give a sedative", 0)], "New confusion + high RR is deterioration &mdash; <b>assess and escalate</b>, don't wait."),
      ("Which pattern most suggests early sepsis?", [("HR and RR up, BP and SpO&#8322; down, temp up", 1), ("All vital signs stable", 0), ("Only a mild headache", 0), ("Isolated high blood pressure", 0)], "The <b>trend</b> &mdash; rising HR/RR/temp, falling BP/SpO&#8322; &mdash; is the sepsis pattern (SIRS)."),
      ("The nurse is calling the rapid response team. Which tool structures the call?", [("SOAP", 0), ("SBAR", 1), ("PERRLA", 0), ("RICE", 0)], "<b>SBAR</b> (Situation, Background, Assessment, Recommendation) structures the escalation."),
      ("A single slightly-abnormal vital sign is best interpreted by:", [("Ignoring it if the patient looks okay", 0), ("Comparing it to the trend over time", 1), ("Rechecking only at end of shift", 0), ("Charting without action", 0)], "One value is noise; the <b>trend</b> is the signal. Compare to baseline and direction."),
    ],
    "sata": {"q": "Which findings warrant escalation to the provider or rapid response? Select all that apply.",
      "opts": [("New confusion or restlessness", 1), ("RR 28 and climbing", 1), ("Improving, well-controlled pain", 0), ("SpO&#8322; falling from 98% to 90%", 1), ("Urine output 15 mL/hr for 2 hours", 1)],
      "rationale": "New confusion, rising RR, falling SpO&#8322;, and low urine output all signal deterioration &mdash; escalate. Improving pain does not."},
    "next": "Critical Lab Values", "upsell": "ICU, ER &amp; rapid response",
  },
]

for _c in COURSES:
    PAGES[_c["slug"]] = (
        f"{_c['title']} {_c['title_em']} &mdash; Free NCLEX Lesson | Must Love Scrubs",
        "A free interactive NCLEX lesson: audio scene, memory game, matrix, chart test, and a clinical quick check.",
        build_course(_c), "scrubtv")

def lesson_cards():
    out = []
    for c in COURSES:
        name = f"{c['title']} {c['title_em']}"
        out.append(f"""<a class="course-card fade-up" href="{c['slug']}">
          <div class="cover" style="background:{c['grad']};">{c['num']}</div>
          <div class="body"><b>{name}</b><small>{c['kicker'].split('&middot;')[0].strip()} &middot; audio + 4 tests</small>
            <div class="foot"><span class="p" style="color:var(--teal-600);">Free</span><a style="font-size:0.82rem;font-weight:700;color:var(--coral-500);">Start &rarr;</a></div>
          </div></a>""")
    return '<div class="course-shelf">' + "".join(out) + '</div>'

PAGES["scrubtv.html"] = ("Scrub TV — Free NCLEX Lessons | Must Love Scrubs",
    "Scrub TV: four free interactive NCLEX lessons a month. Each one is an audio scene plus a memory game, matrix, chart test, and quiz.",
    page_hero('Scrub TV: nursing school meets <span class="hl on-dark">your feed</span>.',
              "Four free lessons a month. Each is a curated audio scene plus a full workout &mdash; memory game, matrix, chart test, and a clinical quick check. Watch, listen, then prove it.")
    + f"""  <main class="content-block">
    <div class="wrap">
      <div class="section-head fade-up"><span class="eyebrow teal">This month</span><h2>Four free lessons. <span class="hl">Zero excuses.</span></h2><p>The complete free tier &mdash; as deep as anything you'd pay for elsewhere. Specialty prep lives in <a href="courses.html" style="color:var(--coral-500);font-weight:700;">paid courses</a>.</p></div>
      {lesson_cards()}
      <div class="points-strip fade-up" style="margin-top:2rem;">
        <div class="txt"><b>Every lesson earns points.</b><p>Finish the quick check to bank points toward store downloads and course discounts &mdash; all tracked on your dashboard.</p></div>
        <a class="btn btn-dark" href="profile.html">See my progress</a>
      </div>
    </div>
  </main>
""", "scrubtv")

# ---------------------------------------------------------------- write out
for fname, (title, desc, body, *rest) in PAGES.items():
    active = rest[0] if rest else ""
    path = os.path.join(ROOT, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(chrome(fname, title, desc, body, active))
    print("wrote", fname)

print(f"\n{len(PAGES)} pages generated.")
