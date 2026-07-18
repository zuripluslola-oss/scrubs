#!/usr/bin/env python3
"""Bundle the generated multi-page site into ONE self-contained HTML file.

- Inlines css/styles.css and every js/*.js (no external requests -> works as a
  claude.ai Artifact and can't be crawled page-by-page).
- Extracts each page's unique middle (between the mega </nav> and <footer>) and
  stacks them as routes inside the shared index chrome.
- A tiny hash router (window.MLSROUTE) swaps routes on any .html link click,
  so the whole site feels seamless with zero page reloads.

Run AFTER tools/build_pages.py. Output: mls-site-bundle.html at repo root.
"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOP_SEP = '  </nav>\n\n'
BOT_SEP = '\n\n  <footer class="site-footer">'

def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()

def middle(html):
    """The page-unique body between the mega nav and the footer."""
    after = html.split(TOP_SEP, 1)[1]
    return after.split(BOT_SEP, 1)[0]

# ---- collect pages (index first, rest alphabetical) ----
files = sorted(glob.glob(os.path.join(ROOT, '*.html')))
files = [f for f in files if os.path.basename(f) != 'mls-site-bundle.html']
names = [os.path.basename(f) for f in files]
if 'index.html' in names:
    names.remove('index.html'); names.insert(0, 'index.html')

# strip any per-page <script src="js/*.js"> tags from middles (JS is inlined once)
SCRIPT_TAG = re.compile(r'\s*<script src="js/[^"]+"></script>')
routes_html = []
for n in names:
    mid = SCRIPT_TAG.sub('', middle(read(os.path.join(ROOT, n))))
    vis = '' if n == 'index.html' else ' hidden'
    routes_html.append(f'<div class="mls-route" data-route="{n}"{vis}>\n{mid}\n</div>')
routes_block = '<div id="mls-routes">\n' + '\n'.join(routes_html) + '\n</div>'

# ---- shell = index chrome with its middle replaced by the routes block ----
index_html = read(os.path.join(ROOT, 'index.html'))
top = index_html.split(TOP_SEP, 1)[0] + TOP_SEP
bottom = BOT_SEP + index_html.split(BOT_SEP, 1)[1]
shell = top + routes_block + bottom

# ---- inline CSS ----
css = read(os.path.join(ROOT, 'css', 'styles.css'))
shell = shell.replace(
    '<link rel="stylesheet" href="css/styles.css">',
    '<style>\n' + css + '\n</style>')

# ---- router + inlined JS ----
def route_safe(js):
    # turn `window.location.href = X;` into `MLSROUTE(X);`
    return re.sub(r'window\.location\.href\s*=\s*(.+?);', r'MLSROUTE(\1);', js)

js_files = ['main.js', 'prep.js', 'course.js', 'complete.js', 'dictionary.js', 'specialty.js', 'qbank.js', 'flashcards.js']
inlined_js = []
for jf in js_files:
    p = os.path.join(ROOT, 'js', jf)
    if os.path.exists(p):
        inlined_js.append(f'/* ===== {jf} ===== */\n' + route_safe(read(p)))

ROUTER = r"""
/* ===== MLS single-file router ===== */
(function () {
  var routes = document.getElementById('mls-routes');
  function reveal(r){ r.querySelectorAll('.fade-up').forEach(function(e){ e.classList.add('visible'); }); }
  function show(name, hash){
    var target = null;
    routes.querySelectorAll('.mls-route').forEach(function(r){
      var on = r.getAttribute('data-route') === name;
      r.hidden = !on;
      if(on){ target = r; reveal(r); }
    });
    if(!target){ return false; }
    window.scrollTo(0, 0);
    if(hash){
      var el = target.querySelector(hash);
      if(el){ setTimeout(function(){ el.scrollIntoView({behavior:'smooth', block:'start'}); }, 80); }
    }
    return true;
  }
  window.MLSROUTE = function(href){
    if(!href){ return; }
    var hash = '', name = href, hi = href.indexOf('#');
    if(hi >= 0){ hash = href.slice(hi); name = href.slice(0, hi); }
    name = name.split('/').pop();
    if(!name){ // pure in-page hash
      if(hash){ var cur = document.querySelector('.mls-route:not([hidden]) ' + hash); if(cur){ cur.scrollIntoView({behavior:'smooth', block:'start'}); } }
      return;
    }
    if(!routes.querySelector('.mls-route[data-route="' + name + '"]')){ return; }
    if(show(name, hash)){ history.replaceState(null, '', '#/' + name + hash); }
  };
  document.addEventListener('click', function(e){
    var a = e.target.closest && e.target.closest('a[href]');
    if(!a){ return; }
    var href = a.getAttribute('href');
    if(!href || a.target === '_blank'){ return; }
    if(href.charAt(0) === '#'){ e.preventDefault(); window.MLSROUTE(href); return; }
    if(/^https?:|^mailto:|^tel:/.test(href)){ return; }
    if(/\.html(#|$)/.test(href)){ e.preventDefault(); window.MLSROUTE(href); }
  }, true);
  // initial route from location hash (#/page.html[#anchor])
  var init = location.hash.replace(/^#\//, '');
  if(init){
    var n = init.split('#')[0];
    var h = init.indexOf('#') >= 0 ? ('#' + init.split('#').slice(1).join('#')) : '';
    if(n){ show(n, h); }
    else { reveal(routes.querySelector('.mls-route[data-route="index.html"]')); }
  } else {
    reveal(routes.querySelector('.mls-route[data-route="index.html"]'));
  }
})();
"""

full_js = '<script>\n' + ROUTER + '\n' + '\n\n'.join(inlined_js) + '\n</script>'
shell = shell.replace('<script src="js/main.js"></script>', full_js)

# ---- embed real photos from /images as data URIs (CSP-safe in the artifact) ----
import base64, mimetypes
def _embed_images(html):
    def repl(m):
        rel = m.group(1)  # e.g. images/nurses-group.jpg
        path = os.path.join(ROOT, rel)
        if os.path.exists(path):
            mime = mimetypes.guess_type(path)[0] or 'image/jpeg'
            data = base64.b64encode(open(path, 'rb').read()).decode('ascii')
            return f'url(data:{mime};base64,{data})'
        return 'none'  # file not provided yet -> drop the layer, gradient shows through
    return re.sub(r'url\((images/[^)]+)\)', repl, html)
shell = _embed_images(shell)

out = os.path.join(ROOT, 'mls-site-bundle.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(shell)
print('bundled', len(names), 'pages ->', out, f'({os.path.getsize(out)//1024} KB)')
