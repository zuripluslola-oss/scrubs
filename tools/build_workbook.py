#!/usr/bin/env python3
"""Render content/nclex-complete-workbook.md into a branded, print-ready HTML.

Open the HTML in a browser and 'Save as PDF' for the downloadable workbook.
Styled in the Must Love Scrubs Violet & Mint palette, with page breaks so each
question starts cleanly.
"""
import os, re, markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'content', 'nclex-complete-workbook.md')
OUT = os.path.join(ROOT, 'content', 'nclex-complete-workbook.html')

md = open(SRC, encoding='utf-8').read()
body = markdown.markdown(md, extensions=['extra', 'sane_lists', 'nl2br'])

# Put each question on its own printed page: break before every <h3>.
body = body.replace('<h3>', '<h3 class="qbreak">')
# Section titles (h1) start a page too.
body = body.replace('<h1>', '<h1 class="pbreak">')

HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Must Love Scrubs — The NGN Workbook (50 Original Questions)</title>
<style>
  :root {
    --violet:#8b5cff; --violet-d:#4d2b9e; --indigo:#2b1055; --ink:#1e1233;
    --mint:#14b8a8; --mint-l:#2ad4c4; --gold:#d99a1f; --bg:#f6f3ff;
    --paper:#ffffff; --line:rgba(30,18,51,0.10);
  }
  * { box-sizing:border-box; }
  body {
    margin:0; background:var(--bg); color:var(--ink);
    font-family:'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif;
    line-height:1.6; font-size:15px;
  }
  .sheet { max-width:800px; margin:0 auto; background:var(--paper);
    padding:56px 60px; box-shadow:0 20px 60px rgba(30,18,51,0.12); }
  h1,h2,h3,h4 { font-family:'Helvetica Neue',Arial,sans-serif; line-height:1.2; }
  h1 { font-size:1.7rem; font-weight:800; color:var(--violet-d);
    border-bottom:3px solid var(--mint-l); padding-bottom:0.4rem; margin:2.4rem 0 1.2rem; }
  h2 { font-size:1.15rem; color:var(--ink); }
  h3 { font-size:1.18rem; font-weight:800; color:var(--indigo); margin:1.8rem 0 0.3rem; }
  h3 + p { margin-top:0; }
  p { margin:0.7rem 0; }
  strong { color:var(--ink); }
  ul { margin:0.5rem 0 0.9rem; padding-left:1.2rem; }
  li { margin:0.28rem 0; }
  hr { border:none; border-top:1px solid var(--line); margin:1.6rem 0; }
  blockquote { background:var(--bg); border-left:4px solid var(--gold);
    margin:1.4rem 0; padding:0.9rem 1.2rem; border-radius:0 10px 10px 0;
    font-size:0.92rem; }
  code { background:#efeaff; padding:0 4px; border-radius:4px; }
  /* Cover */
  .cover { text-align:center; padding:60px 0 30px; }
  .cover .mark { font-family:'Helvetica Neue',Arial,sans-serif; font-weight:800;
    font-size:2.2rem; color:var(--violet-d); letter-spacing:-0.02em; }
  .cover .mark b { color:#e5484d; }
  /* Emoji-led callout lines get a soft tint */
  p:first-child { }
  @media print {
    body { background:#fff; font-size:11.5pt; }
    .sheet { box-shadow:none; max-width:none; padding:0 0.4in; margin:0; }
    h1.pbreak { page-break-before:always; }
    h3.qbreak { page-break-before:always; }
    h1.pbreak:first-of-type, h3.qbreak:first-of-type { page-break-before:auto; }
    blockquote, ul, li, p { page-break-inside:avoid; }
    a { color:inherit; text-decoration:none; }
  }
  @page { margin:0.7in; }
</style>
</head>
<body>
  <div class="sheet">
""" + body + """
  </div>
</body>
</html>
"""

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(HTML)
print('wrote', OUT, f'({os.path.getsize(OUT)//1024} KB)')
