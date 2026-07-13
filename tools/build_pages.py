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
}

TICKER_ESI = "".join(
    '<span>&#10022; Meet <em>Esi</em> — the AI tutor that revolutionizes how nurses learn</span>'
    '<span>&#10022; Esi guides you through the site &amp; tutors you 1-on-1</span>'
    '<span>&#10022; Add <em>Esi</em> to any prep course — study smarter, remember longer</span>'
    for _ in range(2))

TICKER_COURSES = "".join(
    '<span>&#9733; <em>NCLEX Complete</em> — our flagship prep course is live</span>'
    '<span>&#9733; New Scrub TV drops every 2 weeks — watch, quiz, earn points</span>'
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
          <li><a href="course-lab-values.html">Free NCLEX Practice <small>Start with a free audio scene</small></a></li>
          <li><a href="courses.html">Courses <small>NCLEX prep, entrance exams &amp; more</small></a></li>
          <li><a href="scrubtv.html">Scrub TV <small>Audio scenes + quizzes, new every 2 weeks</small></a></li>
          <li><a href="esi.html">Esi <small>Your AI tutor &amp; site guide</small></a></li>
        </ul>
      </div>
      <div>
        <h4>Community</h4>
        <ul class="mega-links">
          <li><a href="spotlight.html">Nurse Spotlight <small>Real stories, beautifully told</small></a></li>
          <li><a href="jobs.html">Job Search <small>A small Indeed, just for nurses</small></a></li>
          <li><a href="blog.html">Blog <small>News, tips &amp; nurse life</small></a></li>
          <li><a href="store.html">Store <small>Curated nurse lifestyle goods</small></a></li>
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
      <a class="mega-promo" href="courses.html">
        <span class="art">NCLEX</span>
        <b>NCLEX Complete</b>
        <p>The flagship prep course — built on proven retention science.</p>
        <span class="btn btn-coral" style="padding:0.6rem 1.3rem; font-size:0.85rem;">Start Learning</span>
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
          <li><a href="courses.html">Courses</a></li>
          <li><a href="course-lab-values.html">Free NCLEX Practice</a></li>
          <li><a href="scrubtv.html">Scrub TV</a></li>
          <li><a href="esi.html">Esi Tutoring</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Discover</h5>
        <ul>
          <li><a href="spotlight.html">Spotlight</a></li>
          <li><a href="jobs.html">Job Search</a></li>
          <li><a href="blog.html">Blog</a></li>
          <li><a href="store.html">Store</a></li>
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
    <a class="bn-item{' active' if active == 'store' else ''}" href="store.html">{I['bag']}<span>Store</span></a>
    <a class="bn-item{' active' if active == 'profile' else ''}" href="profile.html">{I['user']}<span>Profile</span></a>
  </nav>

  <button class="esi-fab" data-esi-launch aria-label="Esi — your AI tutor">
    <span class="orb"></span>
    <span>Esi<span class="lock">PREMIUM TUTOR</span></span>
  </button>

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
    ("What is Must Love Scrubs?", "A premium nursing education ecosystem: prep courses built on proven retention science, Scrub TV learning videos with quizzes, a curated nurse lifestyle store, and Esi — an AI tutor that guides your studying and helps you navigate the site."),
    ("Is Esi free?", "Esi is a premium add-on to any prep course. She tutors you one-on-one, targets your weak areas, and helps you find your way around the site. You can preview what she does on the Esi page."),
    ("How do points work?", "Log in and claim 5 free points every day on your Profile Dashboard. Earn more by completing quizzes, puzzles, and video activities. Redeem points for digital downloads in the store — study guides, brain sheets, planners and more."),
    ("What courses do you offer?", "NCLEX Complete is our flagship, alongside specialty courses like Pharmacology Mastery, Med-Surg Essentials, and NGN Prioritization &amp; Delegation. The library grows constantly."),
    ("How often does Scrub TV update?", "Fresh videos drop every two weeks across eight specialty channels — each with quizzes and activities that earn you points."),
    ("Can I use Must Love Scrubs on my phone?", "Absolutely — the entire site is designed mobile-first, with app-style navigation. Study on the bus, in the break room, or on the couch."),
]

def faq_list():
    out = []
    chev = '<svg class="chev" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="m6 9 6 6 6-6"/></svg>'
    for q, a in FAQS:
        out.append(f"""<div class="faq-item">
          <button class="faq-q">{q} {chev}</button>
          <div class="faq-a"><p>{a}</p></div>
        </div>""")
    return '<div class="faq-list">' + "".join(out) + '</div>'

# ---------------------------------------------------------------- HOMEPAGE
HERO_SCENE = """<svg viewBox="0 0 560 420" role="img" aria-label="Instructor training nursing students at a hospital bed">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#4d2b9e"/><stop offset="1" stop-color="#2b1055"/>
    </linearGradient>
    <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#4d2b9e"/><stop offset="1" stop-color="#1a0942"/>
    </linearGradient>
  </defs>
  <rect width="560" height="420" fill="url(#sky)"/>
  <rect y="300" width="560" height="120" fill="url(#floor)"/>
  <rect x="40" y="60" width="120" height="150" rx="10" fill="#3a1f7a"/>
  <path d="M60 100h80M60 125h80M60 150h55" stroke="#a78bff" stroke-width="6" stroke-linecap="round" opacity="0.8"/>
  <path d="M60 175 h20 l8-16 10 30 9-14h33" stroke="#8b5cff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="120" y="250" width="330" height="70" rx="16" fill="#14b8a8"/>
  <rect x="130" y="230" width="310" height="34" rx="14" fill="#f6f3ff"/>
  <ellipse cx="175" cy="247" rx="22" ry="14" fill="#ffffff"/>
  <path d="M205 252 q90 -18 220 -6 l0 18 -220 0z" fill="#a78bff" opacity="0.92"/>
  <rect x="135" y="318" width="14" height="70" fill="#432a8a"/>
  <rect x="425" y="318" width="14" height="70" fill="#432a8a"/>
  <circle cx="480" cy="120" r="26" fill="#f4c39a"/>
  <path d="M462 112a26 26 0 0 1 36-4l4-10a32 32 0 0 0-46 6z" fill="#2b1055"/>
  <path d="M450 210 q30 -66 60 0 l6 90 h-72z" fill="#14b8a8"/>
  <path d="M452 170 q-24 34 -40 44l10 14q26 -14 42 -40z" fill="#14b8a8"/>
  <path d="M420 216 l-16 12 8 10 16 -10z" fill="#f4c39a"/>
  <circle cx="340" cy="150" r="22" fill="#e8b088"/>
  <path d="M322 144a22 22 0 0 1 34-6l6-8a30 30 0 0 0-46 8z" fill="#3b2a20"/>
  <path d="M315 230 q25 -54 50 0 l5 74 h-60z" fill="#8b5cff"/>
  <path d="M318 196 q-20 26 -34 34l8 12q22 -10 36 -32z" fill="#8b5cff"/>
  <circle cx="255" cy="160" r="21" fill="#8a5a3b"/>
  <path d="M238 154a21 21 0 0 1 33-6l5-8a29 29 0 0 0-44 8z" fill="#161616"/>
  <path d="M232 236 q23 -50 46 0 l5 68 h-56z" fill="#a78bff"/>
  <path d="M234 202 q-16 22 -28 30l7 11q20 -10 32 -28z" fill="#a78bff"/>
  <circle cx="500" cy="60" r="3" fill="#ffc23d"/><circle cx="520" cy="80" r="2" fill="#ffc23d" opacity="0.7"/>
  <circle cx="60" cy="40" r="2.5" fill="#a78bff" opacity="0.8"/><circle cx="90" cy="28" r="2" fill="#8b5cff" opacity="0.8"/>
</svg>"""

INDEX_BODY = f"""  <main>
    <section class="hero">
      <div class="hero-layer" data-parallax="0.22" aria-hidden="true">
        <div class="glow glow-coral"></div><div class="glow glow-teal"></div><div class="glow glow-gold"></div>
      </div>
      <div class="wrap hero-grid">
        <div>
          <span class="flag">{I['star']} #1 IN NCLEX PREP CONFIDENCE</span>
          <h1>Train for the nurse you're <span class="hl on-dark">becoming</span>.</h1>
          <p class="lede">Prep courses built on proven retention science, videos that teach like a great preceptor, and Esi — the AI tutor that makes it stick. This is the ecosystem of nursing.</p>
          <div class="hero-cta">
            <a class="btn btn-coral" href="course-lab-values.html">Try a free scene</a>
            <a class="btn btn-ghost" href="courses.html">See all courses</a>
          </div>
          <p class="hero-note">Free NCLEX practice &middot; daily points &middot; no card required</p>
        </div>
        <div class="hero-visual fade-up">
          <div class="scene">{HERO_SCENE}</div>
          <div class="float-chip tl"><span class="ico" style="background:var(--teal-100);color:var(--teal-600);">{I['check']}</span> Clinical-judgment focused</div>
          <div class="float-chip br"><span class="ico" style="background:var(--gold-100);color:var(--gold-600);">{I['star']}</span> Earn points as you learn</div>
          <span class="scene-tag">Swap-ready: bedside training photo goes here</span>
        </div>
      </div>
    </section>

    <section class="scrubtv" id="scrubtv">
      <div class="wrap">
        <div class="section-head fade-up">
          <div class="row">
            <div>
              <span class="eyebrow">Scrub TV</span>
              <h2>Watch. Quiz. <span class="hl">Remember.</span></h2>
              <p>Eight specialty channels. Fresh videos every two weeks — each with quizzes and activities that earn you points.</p>
            </div>
            <a class="btn btn-line" href="scrubtv.html">All channels</a>
          </div>
        </div>
        {cat_grid()}
        {video_row()}
      </div>
    </section>

    <section class="welcome">
      <div class="hero-layer" data-parallax="0.14" aria-hidden="true"><div class="glow glow-coral" style="opacity:0.5;"></div></div>
      <div class="wrap fade-up" style="position:relative;z-index:2;">
        <p class="kicker">Wherever you are on your nursing journey…</p>
        <h2>WELCOME <span class="heart">HOME</span>.</h2>
        <p class="sub">Student, new grad, seasoned RN, or somewhere in between — Must Love Scrubs was built around one belief: nurses deserve tools as excellent as the care they give.</p>
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
            <div class="price-line"><span class="price">$129</span><span class="per">one-time &middot; or $39/mo</span></div>
            <div class="chip-row"><span class="chip">+ Add Esi tutoring &middot; $19/mo</span></div>
            <a class="btn btn-coral" href="courses.html">Explore the course</a>
          </div>
        </div>
        {course_shelf()}
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
            <p>NCLEX Complete leads a growing catalog of specialty prep — pharmacology, med-surg, peds, mental health, NGN drills — with new content added constantly.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="store" id="store">
      <div class="wrap">
        <div class="section-head fade-up">
          <div class="row">
            <div>
              <span class="eyebrow gold">The Store</span>
              <h2>Wear the <span class="hl">love</span>.</h2>
              <p>Small, curated, and made for nurse life — every piece carries the MLS mark.</p>
            </div>
            <a class="btn btn-line" href="store.html">Shop all</a>
          </div>
        </div>
        {product_grid(4)}
        <div class="points-strip fade-up">
          <div class="txt">
            <b>Your points are currency here.</b>
            <p>Claim 5 free points daily, earn more from quizzes &amp; contests, then redeem for study guides, brain sheets, planners and other digital downloads.</p>
          </div>
          <a class="btn btn-dark" href="profile.html">Claim today's points</a>
        </div>
      </div>
    </section>

    <section class="proof">
      <div class="wrap">
        <div class="stat-row">
          <div class="stat-big fade-up"><b><span data-count="1400">0</span><span class="plus">+</span></b><span>Nurses trained with our courses</span></div>
          <div class="stat-big fade-up"><b><span data-count="8">0</span></b><span>Specialty video channels</span></div>
          <div class="stat-big fade-up"><b>24/7</b><span>Esi tutoring, whenever you study</span></div>
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
          <span class="eyebrow teal">Questions</span>
          <h2>Everything you're wondering.</h2>
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
            <span>{I['check']} 5 points daily</span>
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
              "Adaptive question banks, real test-format mocks, and analytics that show your exact weak areas. Add Esi and get a tutor who never sleeps.",
              '<div class="hero-cta" style="margin-top:1.8rem;"><a class="btn btn-coral" href="join.html">Start free</a><a class="btn btn-ghost" href="esi.html">Add Esi tutoring</a></div>')
    + f"""  <main class="content-block">
    <div class="wrap">
      <div class="course-hero fade-up">
        <div class="art"><span class="big">NCLEX</span></div>
        <div class="body">
          <div class="chip-row"><span class="chip gold">FLAGSHIP</span><span class="chip teal">NGN READY</span></div>
          <h3>NCLEX Complete</h3>
          <p>Everything to test day: adaptive banks, clinical-judgment cases, timed mocks in real test format, score analytics, and a visual progress map. Built on how memory actually works — spaced repetition and active recall, not cramming.</p>
          <div class="price-line"><span class="price">$129</span><span class="per">one-time &middot; or $39/mo</span></div>
          <div class="chip-row"><span class="chip">+ Esi tutoring $19/mo</span></div>
          <a class="btn btn-coral" href="join.html">Enroll (coming at launch)</a>
        </div>
      </div>
      <div style="height:1.2rem;"></div>
      {course_shelf()}
      <div class="section-head fade-up" style="margin-top:3.5rem;">
        <span class="eyebrow teal">How it works</span>
        <h2>Learn it once. Keep it forever.</h2>
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
        <span class="eyebrow" style="color:var(--gold-400);">Premium add-on</span>
        <h2>Add Esi to any prep course.</h2>
        <p><b style="font-size:1.6rem;">$19/mo</b> &nbsp;&middot;&nbsp; requires an active course &middot; cancel anytime</p>
        <a class="btn btn-coral" href="#" data-esi-subscribe>Subscribe to Esi (demo)</a>
        <div class="perks">
          <span>{I['check']} Unlimited tutoring sessions</span>
          <span>{I['check']} Weak-area tracking</span>
          <span>{I['check']} Smart study plans</span>
        </div>
      </div>
      <p style="margin-top:1.6rem;font-size:0.78rem;color:var(--ink-60);max-width:70ch;">Esi is an educational tutor only. She does not provide medical advice, diagnose, or prescribe, and she is not a substitute for clinical judgment, faculty guidance, or professional medical care. In an emergency, call 911.</p>
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
        <div class="txt"><b>5 free points every day.</b><p>Claim daily on your dashboard, stack them up, and cash them in right here.</p></div>
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
        <p style="margin:0.3rem 0 1rem;font-size:0.85rem;">Claim 5 free points every day you visit.</p>
        <button class="btn btn-dark" data-claim-daily>Claim today's 5 points</button>
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

COURSE_BODY = f"""  <div class="page-hero">
    <div class="wrap inner">
      <a href="scrubtv.html" style="color:rgba(255,255,255,0.7);font-size:0.85rem;font-weight:700;">&larr; Back to Scrub TV</a>
      <p class="lesson-kicker" style="margin-top:1.4rem;">ER / Night shift &middot; 6 min listen &middot; Free</p>
      <span class="lesson-label" style="color:var(--gold-400);">Scrub TV &middot; Audio Scene &middot; Ep. 01</span>
      <h1 style="margin-top:0.6rem;">When the lab calls at <span class="em">3 a.m.</span></h1>
      <p>Listen to the scene. Catch what matters. Make the call. This is how the floor really sounds &mdash; and how you learn to think before you touch a textbook.</p>
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

  <section style="background:var(--card);">
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

# ---------------------------------------------------------------- write out
for fname, (title, desc, body, *rest) in PAGES.items():
    active = rest[0] if rest else ""
    path = os.path.join(ROOT, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(chrome(fname, title, desc, body, active))
    print("wrote", fname)

print(f"\n{len(PAGES)} pages generated.")
