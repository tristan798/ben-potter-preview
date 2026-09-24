#!/usr/bin/env python3
"""Static site generator for ben-potter.com.

Renders every page, the schema graph, sitemap.xml, robots.txt and host redirect
configs. Run: python3 build.py
"""
import json, os, re, shutil, sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'tools'))
import content as C

TODAY = date.today().isoformat()
ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')


def esc(t):
    """Plain text for JSON-LD and meta attributes."""
    return (t.replace('&amp;', '&').replace('&nbsp;', ' ')
             .replace('<em>', '').replace('</em>', '').replace('"', "'"))


# ---------------------------------------------------------------- page registry
def pages():
    p = [
        {'path': '', 'file': 'index.html',
         'title': 'Ben Potter | Devonport, Belmont &amp; Bayswater Real Estate Agent',
         'desc': ('Ben Potter is a Harcourts Cooper & Co real estate agent with 38 years on the Devonport '
                  'Peninsula, selling homes across Devonport, Belmont and Bayswater and the wider North '
                  'Shore. Free, no obligation property appraisals.'),
         'crumbs': [], 'nav': 'home'},
    ]
    for s in C.SUBURBS:
        p.append({'path': s['slug'] + '/', 'file': s['slug'] + '/index.html',
                  'title': s['title'].replace('&', '&amp;'), 'desc': s['desc'],
                  'crumbs': [(s['name'], None)], 'nav': 'areas', 'suburb': s})
    p += [
        {'path': 'recently-sold/', 'file': 'recently-sold/index.html',
         'title': 'Recently Sold in Devonport, Belmont &amp; Bayswater | Ben Potter',
         'desc': ('Homes recently sold by Ben Potter across Devonport, Belmont and Bayswater, plus current '
                  'listings and off-market opportunities on the Devonport Peninsula.'),
         'crumbs': [('Recently sold', None)], 'nav': 'sold'},
        {'path': 'free-selling-guide/', 'file': 'free-selling-guide/index.html',
         'title': 'Free Selling Guide for Devonport, Belmont &amp; Bayswater | Ben Potter',
         'desc': ('A free guide to preparing, pricing and selling a home on the Devonport Peninsula, written '
                  'by Ben Potter from 38 years selling in Devonport, Belmont and Bayswater.'),
         'crumbs': [('Free selling guide', None)], 'nav': 'guide'},
        {'path': 'property-appraisal/', 'file': 'property-appraisal/index.html',
         'title': 'Free Property Appraisal, Devonport Peninsula | Ben Potter',
         'desc': ('Book a free, no obligation property appraisal for your Devonport, Belmont or Bayswater '
                  'home. A written estimate from recent comparable sales, plus a recommended method of sale.'),
         'crumbs': [('Property appraisal', None)], 'nav': 'contact'},
    ]
    return p


NAV = [('About', '#about', 'about'), ('Areas', 'areas', 'areas'),
       ('Sold', 'recently-sold/', 'sold'), ('Reviews', '#reviews', 'reviews'),
       ('Contact', 'property-appraisal/', 'contact')]


def rel(depth):
    return '../' * depth


def link(href, depth):
    """Resolve an internal link for a page at the given folder depth."""
    if href.startswith('#') or href.startswith('http') or href.startswith('tel:') or href.startswith('mailto:'):
        return href
    if href == 'areas':
        return rel(depth) + ('#areas' if depth == 0 else '')  or rel(depth)
    return rel(depth) + href


# ---------------------------------------------------------------- components
def header(depth, nav_key):
    home = rel(depth) if depth else '#top'
    items = []
    for label, href, key in NAV:
        if href.startswith('#'):
            target = href if depth == 0 else rel(depth) + href
        elif href == 'areas':
            target = '#areas' if depth == 0 else rel(depth) + '#areas'
        else:
            target = rel(depth) + href
        cur = ' class="active" aria-current="page"' if key == nav_key else ''
        items.append(f'      <a href="{target}"{cur}>{label}</a>')
    nav = '\n'.join(items)
    mob = '\n'.join(f'      <a href="{i.split(chr(34))[1]}">{i.split(">")[1].split("<")[0]}</a>'
                    for i in items)
    return f'''<header class="header" id="top">
  <div class="wrap">
    <a class="wordmark" href="{home}">Ben Potter</a>
    <nav class="nav" aria-label="Main">
{nav}
    </nav>
    <a class="btn btn-ink" href="{rel(depth)}property-appraisal/">Book a Free Appraisal</a>
    <button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="mobileNav" aria-label="Open menu">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" aria-hidden="true"><path d="M3 8h18M3 16h18"/></svg>
    </button>
  </div>
  <nav class="mobile-nav" id="mobileNav" aria-label="Mobile">
    <div class="wrap">
{mob}
      <a href="{rel(depth)}property-appraisal/">Book a Free Appraisal</a>
    </div>
  </nav>
</header>'''


def crumbs(items, depth):
    if not items:
        return ''
    parts = [f'<a href="{rel(depth)}">Home</a>']
    for label, href in items:
        parts.append('<i aria-hidden="true">/</i>')
        if href:
            parts.append(f'<a href="{rel(depth)}{href}">{label}</a>')
        else:
            parts.append(f'<span aria-current="page">{label}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + ''.join(parts) + '</nav>'


def faq_block(items, open_first=True):
    out = []
    for i, (q, a) in enumerate(items):
        o = ' open' if (i == 0 and open_first) else ''
        out.append(f'''          <details{o}>
            <summary>{q}</summary>
            <p>{a}</p>
          </details>''')
    return '\n'.join(out)


def card(suburb, addr, meta, result, status, live=False, depth=0):
    slug = re.sub(r'[^a-z0-9]+', '-', addr.lower()).strip('-')
    alt = f'{addr}, {suburb}, sold by Ben Potter'
    return f'''        <a class="card" href="{rel(depth)}property-appraisal/" aria-label="{addr}, {suburb}">
          <div class="card-media" data-note="Photography to come"><!-- <img src="{rel(depth)}img/listings/{slug}-{suburb.lower()}.jpg" alt="{alt}" width="800" height="600" loading="lazy"> --></div>
          <div class="card-body">
            <p class="label">{suburb}</p>
            <h3>{addr}</h3>
            <p class="card-meta">{meta}</p>
            <p class="card-meta">{result}</p>
            <p class="card-status{' live' if live else ''}">{status}</p>
          </div>
        </a>'''


def offmarket(depth):
    return f'''        <a class="card text-card" href="{rel(depth)}property-appraisal/">
          <div class="card-body">
            <p class="label">Off market</p>
            <h3>Some homes never reach this page.</h3>
            <p class="card-meta">Ben sells a good share of Peninsula homes quietly, to buyers already on his list. Tell him what you're looking for.</p>
            <p class="card-status live">Register as a buyer {ARROW}</p>
          </div>
        </a>'''


def reviews_section(depth):
    return f'''  <section class="section words" id="reviews" aria-labelledby="reviewsTitle">
    <div class="wrap">
      <h2 class="label" id="reviewsTitle">In their words</h2>
      <p class="stars" aria-hidden="true" style="margin-top:1.4rem">★★★★★</p>
      <blockquote class="quote" id="quoteText">{C.REVIEWS[0][0]}</blockquote>
      <div class="quote-by"><b id="quoteName">{C.REVIEWS[0][1]}</b><span id="quoteWhere">{C.REVIEWS[0][2]}</span></div>
      <div class="quote-nav">
        <button type="button" id="qPrev" aria-label="Previous review"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 18l-6-6 6-6"/></svg></button>
        <span class="count" id="qCount" aria-live="polite">1 / {len(C.REVIEWS)}</span>
        <button type="button" id="qNext" aria-label="Next review"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
      </div>
      <p class="trust"><a href="{C.RATEMYAGENT}" rel="noopener">Verified reviews on RateMyAgent</a></p>
    </div>
  </section>'''


def appraisal_form(depth, heading='Request appraisal'):
    return f'''        <form id="appraisal" novalidate aria-label="Appraisal request">
          <div class="field">
            <label for="f-address">Property address</label>
            <input id="f-address" name="address" type="text" autocomplete="street-address" placeholder="12 Cheltenham Road, Devonport" required>
          </div>
          <div class="field-row">
            <div class="field">
              <label for="f-name">Name</label>
              <input id="f-name" name="name" type="text" autocomplete="name" required>
            </div>
            <div class="field">
              <label for="f-phone">Mobile</label>
              <input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required>
            </div>
          </div>
          <div class="field">
            <label for="f-email">Email</label>
            <input id="f-email" name="email" type="email" autocomplete="email">
          </div>
          <div class="field">
            <label for="f-when">Timeframe</label>
            <select id="f-when" name="timeframe">
              <option>Selling in the next three months</option>
              <option>Selling in three to twelve months</option>
              <option>Just curious about value</option>
            </select>
          </div>
          <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
          <div class="form-foot">
            <button class="btn btn-blue" type="submit">{heading}</button>
            <small>No cost, no obligation. Ben replies personally.</small>
          </div>
        </form>'''


def contact_section(depth):
    return f'''  <section class="section appraise on-light stone" id="contact" aria-labelledby="contactTitle">
    <div class="wrap">
      <div class="appraise-copy">
        <p class="label blue">Book a free appraisal</p>
        <h2 id="contactTitle">Talk to Ben <em>before</em> you list.</h2>
        <p class="lede">A written appraisal of your property and an honest view on what it needs before the first open home.</p>
        <div class="details">
          <a href="tel:{C.PHONE_LINK}"><span>Mobile</span><b>{C.PHONE_DISPLAY}</b></a>
          <a href="mailto:{C.EMAIL}"><span>Email</span><b>{C.EMAIL}</b></a>
          <div><span>Agency</span><b>{C.AGENCY}</b></div>
        </div>
      </div>
      <div class="form-card">
{appraisal_form(depth)}
      </div>
    </div>
  </section>'''


def switcher(depth, current=None):
    out = []
    for s in C.SUBURBS:
        cur = ' aria-current="page"' if s['name'] == current else ''
        out.append(f'''        <a href="{rel(depth)}{s['slug']}/"{cur}>
          <p class="coord">{s['coord']}</p>
          <h3>{s['name']}</h3>
          <p>{s['card']}</p>
          <span class="quietlink">Explore {s['name']} {ARROW}</span>
        </a>''')
    return '\n'.join(out)


def footer(depth):
    d = rel(depth)
    links = [('About Ben', d + '#about' if depth == 0 else d + '#about'),
             ('Devonport', d + 'devonport-real-estate/'),
             ('Belmont', d + 'belmont-real-estate/'),
             ('Bayswater', d + 'bayswater-real-estate/'),
             ('Recently sold', d + 'recently-sold/'),
             ('Selling guide', d + 'free-selling-guide/'),
             ('Appraisal', d + 'property-appraisal/')]
    ls = '\n'.join(f'        <a href="{h}">{t}</a>' for t, h in links)
    return f'''<footer class="footer">
  <div class="wrap">
    <div class="footer-top">
      <div style="display:flex; flex-direction:column; gap:14px">
        <a class="wordmark" href="{d or '#top'}">Ben Potter</a>
        <p class="coord">Devonport Peninsula · 36.8290° S · 174.7961° E</p>
      </div>
      <div class="footer-links">
{ls}
      </div>
    </div>
    <div class="footer-bottom">
      <span>© {date.today().year} {C.AGENT_NAME} · {C.AGENCY} · Licensed under the REA Act 2008</span>
      <span><a href="tel:{C.PHONE_LINK}">{C.PHONE_DISPLAY}</a></span>
    </div>
  </div>
</footer>

<div class="sticky" aria-label="Quick action">
  <a class="btn btn-blue" href="{d}property-appraisal/">Book a Free Appraisal</a>
</div>

<dialog class="modal" id="guideModal" aria-labelledby="guideTitle">
  <button class="modal-close" type="button" id="guideClose" aria-label="Close">×</button>
  <div class="modal-body">
    <p class="label blue">Free download</p>
    <h3 id="guideTitle">The Peninsula Selling Guide</h3>
    <p class="muted" style="font-size:.95rem">How to prepare, price and sell a home in Devonport, Belmont or Bayswater. Written by Ben from {C.YEARS} years on the Peninsula.</p>
    <form id="guideForm" novalidate>
      <div class="field"><label for="g-name">Name</label><input id="g-name" name="name" type="text" autocomplete="name" required></div>
      <div class="field"><label for="g-email">Email</label><input id="g-email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="g-phone">Mobile</label><input id="g-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel"></div>
      <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <div class="form-foot"><button class="btn btn-blue" type="submit">Send me the guide</button><small>Ben emails the guide and follows up personally.</small></div>
    </form>
  </div>
</dialog>'''


# ---------------------------------------------------------------- page bodies
def home_body():
    d = 0
    sold = '\n'.join(card(*r, depth=d) for r in C.SOLD[:3])
    return f'''{header(d, 'home')}

<main>
  <section class="hero" aria-labelledby="heroTitle">
    <div class="hero-glow" aria-hidden="true"></div>
    <div class="wrap">
      <div class="hero-copy">
        <p class="label blue rise d1">{C.AGENCY} &nbsp;·&nbsp; Devonport</p>
        <h1 id="heroTitle" class="rise d2">Nearly forty years in the <em>neighbourhood.</em></h1>
        <p class="lede rise d3">{C.SUPPORT_COPY}</p>
        <div class="hero-actions rise d4">
          <a class="btn btn-ink" href="property-appraisal/">Book a Free Appraisal</a>
          <a class="btn btn-line" href="free-selling-guide/">Get the Free Selling Guide</a>
        </div>
        <a class="quietlink rise d5" href="#areas">Explore Devonport, Belmont &amp; Bayswater {ARROW}</a>
      </div>
      <figure class="hero-figure">
        <picture>
          <source srcset="{C.HERO_IMG}.webp" type="image/webp">
          <img src="{C.HERO_IMG}.png" alt="{C.HERO_ALT}" width="1122" height="1402" fetchpriority="high" decoding="async">
        </picture>
      </figure>
    </div>
    <p class="hero-note" aria-hidden="true">Devonport Peninsula</p>
  </section>

  <div class="stats" aria-label="At a glance">
    <div class="wrap">
      <div class="stat"><b>{C.YEARS} years</b><span>On the Devonport Peninsula</span></div>
      <div class="stat"><b>Three suburbs</b><span>Devonport · Belmont · Bayswater</span></div>
      <div class="stat"><b>Harcourts</b><span>Cooper &amp; Co</span></div>
    </div>
  </div>

  <section class="section on-light" id="about" aria-labelledby="aboutTitle">
    <div class="wrap split">
      <div class="split-head">
        <p class="label blue">About Ben</p>
      </div>
      <div>
        <h2 id="aboutTitle" class="statement">Most agents can show you a map of the Peninsula. Ben can tell you <em>who lives on it.</em></h2>
        <div class="prose">
          <p>{C.ABOUT[0]}</p>
          <p>{C.ABOUT[1]}</p>
        </div>
        <button class="reel" id="reelBtn" type="button" aria-label="Play the reel">
          <span class="reel-ring"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></span>
          <span class="reel-caption"><b>Ben on Devonport, Belmont and Bayswater</b><span>Watch the reel</span></span>
        </button>
        <p class="reel-msg" id="reelMsg" hidden>Reel slot. Add a YouTube or Vimeo link in the page config and it plays here.</p>
      </div>
    </div>
  </section>

  <section class="section" id="areas" aria-labelledby="areasTitle">
    <div class="wrap">
      <div class="areas-head">
        <div>
          <p class="label blue">The Peninsula</p>
          <h2 id="areasTitle">Three suburbs. <em>One agent.</em></h2>
        </div>
        <p class="lede">Each of these suburbs has its own housing stock, its own buyers and its own rhythm. Choose one for a closer look at what sells there and what it takes to sell well.</p>
      </div>
      <div class="switch" style="margin-top:clamp(40px, 5vw, 64px)">
{switcher(d)}
      </div>
      <div class="secondary">
        <p class="label">Also sells in</p>
        <p>Narrow Neck &nbsp;·&nbsp; Stanley Point &nbsp;·&nbsp; Hauraki &nbsp;·&nbsp; Takapuna</p>
      </div>
    </div>
  </section>

  <section class="section on-light white" id="sold" aria-labelledby="soldTitle">
    <div class="wrap">
      <div class="list-head">
        <div>
          <p class="label blue">Results</p>
          <h2 id="soldTitle">Recently <em>sold.</em></h2>
        </div>
        <a class="ruled" href="recently-sold/">See all results {ARROW}</a>
      </div>
      <div class="cards">
{sold}
      </div>
      <p class="card-note">Sample entries shown for layout. Listings and photography connect to Ben's CRM feed or are uploaded manually.</p>
    </div>
  </section>

{reviews_section(d)}

  <section class="section on-light" id="faq" aria-labelledby="faqTitle">
    <div class="wrap split">
      <div class="split-head">
        <p class="label blue">Questions</p>
        <h2 id="faqTitle">Selling and buying on the <em>Peninsula.</em></h2>
        <p class="muted" style="font-size:.94rem; max-width:34ch">Straight answers about Devonport, Belmont, Bayswater and the wider North Shore.</p>
      </div>
      <div class="faq-list">
{faq_block(C.FAQ_HOME)}
      </div>
    </div>
  </section>

{contact_section(d)}
</main>

{footer(d)}'''


def suburb_body(s):
    d = 1
    blocks = []
    for h, paras in s['blocks']:
        body = '\n        '.join(f'<p>{t}</p>' for t in paras)
        blocks.append(f'''      <div class="block">
        <h2>{h}</h2>
        {body}
      </div>''')
    facts = '\n'.join(f'        <div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in s['facts'])
    others = [o for o in C.SUBURBS if o['name'] != s['name']]
    other_links = ' and '.join(f'<a href="../{o["slug"]}/">{o["name"]}</a>' for o in others)
    return f'''{header(d, 'areas')}

<main>
  <section class="page-hero" aria-labelledby="pageTitle">
    <div class="hero-glow" aria-hidden="true"></div>
    <div class="wrap">
      {crumbs([(s['name'], None)], d)}
      <p class="coord">{s['coord']}</p>
      <h1 id="pageTitle">{s['h1']}</h1>
      <p class="lede">{s['lede']}</p>
      <div class="page-actions">
        <a class="btn btn-ink" href="../property-appraisal/">Book a Free Appraisal</a>
        <a class="btn btn-line" href="../free-selling-guide/">Get the Free Selling Guide</a>
      </div>
    </div>
  </section>

  <section class="section on-light">
    <div class="wrap content">
      <div class="content-main">
{chr(10).join(blocks)}
        <div class="block">
          <h2>Recently sold nearby</h2>
          <p>A sample of homes Ben has sold across the peninsula. <a href="../recently-sold/">See every recent result</a>, or <a href="../property-appraisal/">ask what your own home would achieve</a>.</p>
        </div>
      </div>
      <div class="aside">
        <div class="panel">
          <h3>Thinking of selling in {s['name']}?</h3>
          <p>Ben will give you a written estimate of value from recent comparable sales nearby, with no cost and no obligation.</p>
          <a class="btn btn-blue" href="../property-appraisal/">Book a free appraisal</a>
        </div>
        <dl class="keyfacts">
{facts}
        </dl>
        <p class="muted" style="font-size:.85rem">Nearby: {s['landmarks']}.</p>
      </div>
    </div>
  </section>

  <section class="section on-light white" aria-labelledby="sFaq">
    <div class="wrap split">
      <div class="split-head">
        <p class="label blue">{s['name']} questions</p>
        <h2 id="sFaq">Asked about <em>{s['name']}.</em></h2>
        <p class="muted" style="font-size:.94rem; max-width:34ch">Also selling in {other_links}.</p>
      </div>
      <div class="faq-list">
{faq_block(s['faq'])}
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="switchTitle">
    <div class="wrap">
      <p class="label blue">The Peninsula</p>
      <h2 id="switchTitle" style="margin-bottom:clamp(32px,4vw,52px)">Three suburbs. <em>One agent.</em></h2>
      <div class="switch">
{switcher(d, s['name'])}
      </div>
    </div>
  </section>

{contact_section(d)}
</main>

{footer(d)}'''


def sold_body():
    d = 1
    sold = '\n'.join(card(*r, depth=d) for r in C.SOLD)
    sale = '\n'.join(card(*r, live=True, depth=d) for r in C.SALE) + '\n' + offmarket(d)
    return f'''{header(d, 'sold')}

<main>
  <section class="page-hero" aria-labelledby="pageTitle">
    <div class="hero-glow" aria-hidden="true"></div>
    <div class="wrap">
      {crumbs([('Recently sold', None)], d)}
      <h1 id="pageTitle">Recently sold on the <em>Peninsula.</em></h1>
      <p class="lede">Every sale below was handled by Ben from the first appraisal through to settlement, across Devonport, Belmont and Bayswater.</p>
      <div class="page-actions">
        <a class="btn btn-ink" href="../property-appraisal/">What would mine sell for?</a>
      </div>
    </div>
  </section>

  <section class="section on-light white" aria-labelledby="soldTitle">
    <div class="wrap">
      <div class="list-head">
        <div><p class="label blue">Results</p><h2 id="soldTitle">Recently <em>sold.</em></h2></div>
      </div>
      <div class="cards">
{sold}
      </div>

      <div class="list-head second">
        <div><h2>Currently for <em>sale.</em></h2></div>
        <a class="ruled" href="../property-appraisal/">Register as a buyer {ARROW}</a>
      </div>
      <div class="cards">
{sale}
      </div>
      <p class="card-note">Sample entries shown for layout. Listings and photography connect to Ben's CRM feed or are uploaded manually.</p>
    </div>
  </section>

  <section class="section" aria-labelledby="areasTitle">
    <div class="wrap">
      <p class="label blue">The Peninsula</p>
      <h2 id="areasTitle" style="margin-bottom:clamp(32px,4vw,52px)">Where these homes are.</h2>
      <div class="switch">
{switcher(d)}
      </div>
    </div>
  </section>

{contact_section(d)}
</main>

{footer(d)}'''


def guide_body():
    d = 1
    items = '\n'.join(f'''      <div class="block">
        <h3>{t}</h3>
        <p>{b}</p>
      </div>''' for t, b in C.GUIDE_CONTENTS)
    return f'''{header(d, 'guide')}

<main>
  <section class="page-hero" aria-labelledby="pageTitle">
    <div class="hero-glow" aria-hidden="true"></div>
    <div class="wrap">
      {crumbs([('Free selling guide', None)], d)}
      <p class="label blue">Free download</p>
      <h1 id="pageTitle">The Peninsula <em>Selling Guide.</em></h1>
      <p class="lede">How to prepare, price and sell a home in Devonport, Belmont or Bayswater, written by Ben from {C.YEARS} years on the peninsula. Useful whether you're selling next month or next year.</p>
      <div class="page-actions">
        <button class="btn btn-blue" type="button" id="guideBtn">Get the free guide</button>
        <a class="btn btn-line" href="../property-appraisal/">Book a Free Appraisal</a>
      </div>
    </div>
  </section>

  <section class="section on-light" aria-labelledby="insideTitle">
    <div class="wrap content">
      <div class="content-main">
        <div class="block">
          <h2 id="insideTitle">What's inside</h2>
          <p>Six short sections, written for homes on this peninsula rather than generic advice about selling anywhere in New Zealand.</p>
        </div>
{items}
        <div class="block">
          <h2>Where to next</h2>
          <p>Read about selling in <a href="../devonport-real-estate/">Devonport</a>, <a href="../belmont-real-estate/">Belmont</a> or <a href="../bayswater-real-estate/">Bayswater</a>, or see <a href="../recently-sold/">what has recently sold</a>.</p>
        </div>
      </div>
      <div class="aside">
        <div class="panel">
          <h3>Ready to talk instead?</h3>
          <p>If you already know you're selling, a free appraisal is the faster route. No cost, no obligation.</p>
          <a class="btn btn-blue" href="../property-appraisal/">Book a free appraisal</a>
        </div>
      </div>
    </div>
  </section>

{contact_section(d)}
</main>

{footer(d)}'''


def appraisal_body():
    d = 1
    steps = '\n'.join(f'''      <div class="block">
        <h3>{t}</h3>
        <p>{b}</p>
      </div>''' for t, b in C.APPRAISAL_STEPS)
    return f'''{header(d, 'contact')}

<main>
  <section class="page-hero" aria-labelledby="pageTitle">
    <div class="hero-glow" aria-hidden="true"></div>
    <div class="wrap">
      {crumbs([('Property appraisal', None)], d)}
      <p class="label blue">Free appraisal</p>
      <h1 id="pageTitle">Talk to Ben <em>before</em> you list.</h1>
      <p class="lede">A written appraisal of your property, built from recent comparable sales, with an honest view on what it needs before the first open home.</p>
      <div class="page-actions">
        <a class="btn btn-blue" href="#form">Request an appraisal</a>
        <a class="btn btn-line" href="tel:{C.PHONE_LINK}">Call {C.PHONE_DISPLAY}</a>
      </div>
    </div>
  </section>

  <section class="section on-light" aria-labelledby="stepsTitle">
    <div class="wrap content">
      <div class="content-main">
        <div class="block">
          <h2 id="stepsTitle">What happens</h2>
          <p>An appraisal with Ben is a conversation about your home and your timing, not a listing pitch. Four things come out of it.</p>
        </div>
{steps}
        <div class="block">
          <h2>Common questions</h2>
          <div class="faq-list">
{faq_block(C.FAQ_APPRAISAL)}
          </div>
        </div>
      </div>
      <div class="aside">
        <div class="panel">
          <h3>Prefer to call?</h3>
          <p>Ben answers his own phone and replies personally.</p>
          <a class="btn btn-blue" href="tel:{C.PHONE_LINK}">{C.PHONE_DISPLAY}</a>
        </div>
        <dl class="keyfacts">
          <div><dt>Cost</dt><dd>Free</dd></div>
          <div><dt>Obligation</dt><dd>None</dd></div>
          <div><dt>Turnaround</dt><dd>Usually a few days</dd></div>
          <div><dt>Covers</dt><dd>Devonport, Belmont, Bayswater</dd></div>
        </dl>
      </div>
    </div>
  </section>

  <section class="section appraise on-light stone" id="form" aria-labelledby="formTitle">
    <div class="wrap">
      <div class="appraise-copy">
        <p class="label blue">Book a free appraisal</p>
        <h2 id="formTitle">Request your <em>appraisal.</em></h2>
        <p class="lede">Fill this in and Ben will call you within one business day to arrange a time that suits.</p>
        <div class="details">
          <a href="tel:{C.PHONE_LINK}"><span>Mobile</span><b>{C.PHONE_DISPLAY}</b></a>
          <a href="mailto:{C.EMAIL}"><span>Email</span><b>{C.EMAIL}</b></a>
          <div><span>Agency</span><b>{C.AGENCY}</b></div>
        </div>
      </div>
      <div class="form-card">
{appraisal_form(d, 'Request appraisal')}
      </div>
    </div>
  </section>
</main>

{footer(d)}'''


# ---------------------------------------------------------------- structured data
AGENT_ID = C.SITE + '/#agent'
PERSON_ID = C.SITE + '/#benpotter'
ORG_ID = C.SITE + '/#agency'


def base_entities():
    address = {"@type": "PostalAddress", "addressLocality": C.LOCALITY, "addressRegion": C.REGION,
               "postalCode": C.POSTCODE, "addressCountry": C.COUNTRY}
    if C.STREET:
        address["streetAddress"] = C.STREET
    areas = []
    for s in C.SUBURBS:
        areas.append({"@type": "Place", "name": f"{s['name']}, Auckland",
                      "geo": {"@type": "GeoCoordinates", "latitude": s['lat'], "longitude": s['lng']}})
    for n in ("Narrow Neck", "Stanley Point", "Hauraki", "Takapuna"):
        areas.append({"@type": "Place", "name": f"{n}, Auckland"})

    agent = {
        "@type": ["RealEstateAgent", "LocalBusiness"],
        "@id": AGENT_ID,
        "name": f"{C.AGENT_NAME} | {C.AGENCY}",
        "description": esc(f"Real estate agent for Devonport, Belmont and Bayswater on Auckland's North "
                           f"Shore. {C.YEARS} years on the Devonport Peninsula."),
        "url": C.SITE + "/",
        "telephone": C.PHONE_LINK,
        "email": C.EMAIL,
        "image": C.SITE + "/" + C.OG_IMAGE,
        "logo": C.SITE + "/img/icon-512.png",
        "address": address,
        "geo": {"@type": "GeoCoordinates", "latitude": -36.8290, "longitude": 174.7961},
        "areaServed": areas,
        "parentOrganization": {"@id": ORG_ID},
        "employee": {"@id": PERSON_ID},
        "sameAs": C.SAMEAS,
        "priceRange": "$$$",
        "knowsLanguage": "en-NZ",
    }
    if C.GOOGLE_MAPS:
        agent["hasMap"] = C.GOOGLE_MAPS
    person = {
        "@type": "Person",
        "@id": PERSON_ID,
        "name": C.AGENT_NAME,
        "jobTitle": "Licensed Real Estate Salesperson (REA Act 2008)",
        "worksFor": {"@id": ORG_ID},
        "memberOf": {"@id": AGENT_ID},
        "telephone": C.PHONE_LINK,
        "email": C.EMAIL,
        "image": C.SITE + "/" + C.HERO_IMG + ".png",
        "url": C.SITE + "/",
        "sameAs": C.SAMEAS,
        "knowsAbout": ["Devonport property", "Belmont property", "Bayswater property",
                       "Residential property appraisal", "Auction marketing", "Character villas"],
        "homeLocation": {"@type": "Place", "name": "Devonport Peninsula, Auckland"},
    }
    org = {"@type": "Organization", "@id": ORG_ID, "name": C.AGENCY,
           "url": "https://harcourts.net/nz/office/devonport", "address": address}
    website = {"@type": "WebSite", "@id": C.SITE + "/#website", "url": C.SITE + "/",
               "name": f"{C.AGENT_NAME} | Devonport, Belmont & Bayswater Real Estate",
               "publisher": {"@id": AGENT_ID}, "inLanguage": "en-NZ"}
    return [agent, person, org, website]


def schema_for(page):
    graph = []
    url = C.SITE + '/' + page['path']
    if page['path'] == '':
        graph += base_entities()
        graph.append({"@type": "WebPage", "@id": url + "#webpage", "url": url,
                      "name": esc(page['title']), "description": esc(page['desc']),
                      "isPartOf": {"@id": C.SITE + "/#website"},
                      "about": {"@id": AGENT_ID}, "inLanguage": "en-NZ"})
        graph.append(faq_schema(C.FAQ_HOME, url))
    else:
        crumb_items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": C.SITE + "/"}]
        for i, (label, _) in enumerate(page['crumbs'], start=2):
            crumb_items.append({"@type": "ListItem", "position": i, "name": esc(label), "item": url})
        graph.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": crumb_items})
        graph.append({"@type": "WebPage", "@id": url + "#webpage", "url": url,
                      "name": esc(page['title']), "description": esc(page['desc']),
                      "isPartOf": {"@id": C.SITE + "/#website"},
                      "breadcrumb": {"@id": url + "#breadcrumb"},
                      "about": {"@id": AGENT_ID}, "inLanguage": "en-NZ"})
        s = page.get('suburb')
        if s:
            graph.append({
                "@type": "Place", "@id": url + "#place", "name": f"{s['name']}, Auckland, New Zealand",
                "geo": {"@type": "GeoCoordinates", "latitude": s['lat'], "longitude": s['lng']},
                "containedInPlace": {"@type": "Place", "name": "North Shore, Auckland"},
            })
            graph.append({
                "@type": "Service", "@id": url + "#service",
                "name": f"Real estate sales and appraisals in {s['name']}",
                "serviceType": "Residential real estate agency",
                "provider": {"@id": AGENT_ID},
                "areaServed": {"@id": url + "#place"},
                "description": esc(s['desc']),
            })
            graph.append(faq_schema(s['faq'], url))
        if page['path'] == 'property-appraisal/':
            graph.append(faq_schema(C.FAQ_APPRAISAL, url))
            graph.append({"@type": "Service", "@id": url + "#service",
                          "name": "Free property appraisal, Devonport Peninsula",
                          "serviceType": "Property appraisal",
                          "provider": {"@id": AGENT_ID},
                          "areaServed": [{"@type": "Place", "name": x['name'] + ", Auckland"} for x in C.SUBURBS],
                          "offers": {"@type": "Offer", "price": "0", "priceCurrency": "NZD",
                                     "description": "Free, no obligation written appraisal"}})
    return {"@context": "https://schema.org", "@graph": graph}


def faq_schema(items, url):
    return {"@type": "FAQPage", "@id": url + "#faq",
            "mainEntity": [{"@type": "Question", "name": esc(q),
                            "acceptedAnswer": {"@type": "Answer", "text": esc(a)}} for q, a in items]}


# ---------------------------------------------------------------- head + shell
def head(page, depth):
    d = rel(depth)
    url = C.SITE + '/' + page['path']
    robots = ('<meta name="robots" content="noindex, nofollow">'
              if C.PREVIEW else
              '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">')
    gsc = f'\n<meta name="google-site-verification" content="{C.GSC_TOKEN}">' if C.GSC_TOKEN else ''
    ga = ''
    if C.GA4_ID:
        ga = f'''
<script async src="https://www.googletagmanager.com/gtag/js?id={C.GA4_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{C.GA4_ID}');</script>'''
    schema = json.dumps(schema_for(page), indent=2, ensure_ascii=False)
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page['title']}</title>
<meta name="description" content="{page['desc']}">
<link rel="canonical" href="{url}">
{robots}{gsc}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{C.AGENT_NAME}">
<meta property="og:locale" content="en_NZ">
<meta property="og:title" content="{page['title']}">
<meta property="og:description" content="{page['desc']}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{C.SITE}/{C.OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{C.HERO_ALT}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{page['title']}">
<meta name="twitter:description" content="{page['desc']}">
<meta name="twitter:image" content="{C.SITE}/{C.OG_IMAGE}">
<meta name="theme-color" content="#131315">
<link rel="icon" href="{d}favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{d}apple-touch-icon.png">
<link rel="preload" href="{d}assets/fonts/clash-display-500.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{d}assets/fonts/poppins-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{d}assets/site.css">{ga}
<script type="application/ld+json">
{schema}
</script>'''


def script_block():
    reviews = json.dumps([{"t": t, "n": n, "w": w} for t, n, w in C.REVIEWS], indent=6, ensure_ascii=False)
    return '''<script>
  (function(){
    // Fill these in as Ben supplies them.
    var CONFIG = {
      // Paste the Web3Forms access key for LEAD_EMAIL here and every submission is
      // emailed straight to that address. Get one free at https://web3forms.com (no account).
      formKey: 'FORM_KEY',
      formEndpoint: 'https://api.web3forms.com/submit',
      leadEmail: 'LEAD_EMAIL',
      guideUrl: 'GUIDE_URL',                               // the selling guide PDF
      reelEmbed: 'REEL_EMBED'                              // e.g. https://www.youtube.com/embed/VIDEO_ID
    };
    var PHONE = 'PHONE_D', PHONE_LINK = 'PHONE_L';
    var $ = function(id){ return document.getElementById(id); };

    var header = document.querySelector('.header'), menuBtn = $('menuBtn');
    if(menuBtn){
      menuBtn.addEventListener('click', function(){
        var open = header.classList.toggle('open');
        menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
      document.querySelectorAll('.mobile-nav a').forEach(function(a){
        a.addEventListener('click', function(){ header.classList.remove('open'); menuBtn.setAttribute('aria-expanded','false'); });
      });
    }

    var reelBtn = $('reelBtn'), reelMsg = $('reelMsg');
    if(reelBtn){
      reelBtn.addEventListener('click', function(){
        if(CONFIG.reelEmbed){
          var f = document.createElement('iframe');
          f.src = CONFIG.reelEmbed + (CONFIG.reelEmbed.indexOf('?') > -1 ? '&' : '?') + 'autoplay=1';
          f.allow = 'autoplay; fullscreen'; f.title = 'Ben Potter reel';
          f.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;border:0';
          reelBtn.innerHTML = ''; reelBtn.appendChild(f);
        } else if(reelMsg){ reelMsg.hidden = !reelMsg.hidden; }
      });
    }

    var quotes = REVIEWS_JSON;
    var qi = 0, qText = $('quoteText'), qName = $('quoteName'), qWhere = $('quoteWhere'), qCount = $('qCount');
    function showQuote(i){
      qi = (i + quotes.length) % quotes.length;
      qText.innerHTML = quotes[qi].t; qName.textContent = quotes[qi].n; qWhere.textContent = quotes[qi].w;
      qCount.textContent = (qi + 1) + ' / ' + quotes.length;
    }
    if(qText){
      $('qPrev').addEventListener('click', function(){ showQuote(qi - 1); });
      $('qNext').addEventListener('click', function(){ showQuote(qi + 1); });
    }

    function sendLead(kind, form){
      var data = {};
      form.querySelectorAll('input, select, textarea').forEach(function(el){
        if(!el.name) return;
        data[el.name] = (el.type === 'checkbox') ? el.checked : el.value.trim();
      });
      var label = (kind === 'guide') ? 'Selling guide download' : 'Appraisal request';
      if(!CONFIG.formKey){
        console.warn('No form key set: this lead was not emailed. See README launch checklist.');
        return Promise.resolve();
      }
      var payload = {
        access_key: CONFIG.formKey,
        subject: label + ' from ' + (data.name || 'the website') + (data.address ? ' — ' + data.address : ''),
        from_name: 'benpotter.co.nz',
        replyto: data.email || '',
        Enquiry: label,
        Name: data.name || '',
        Mobile: data.phone || '',
        Email: data.email || '',
        Property: data.address || '',
        Timeframe: data.timeframe || '',
        Page: location.href,
        botcheck: data.botcheck || false
      };
      return fetch(CONFIG.formEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(payload)
      }).catch(function(){});
    }
    function validate(form){
      var ok = true;
      form.querySelectorAll('[required]').forEach(function(el){
        var bad = !el.value.trim() || (el.type === 'email' && el.value.indexOf('@') < 0);
        el.style.borderColor = bad ? '#D0342C' : '';
        if(bad){ ok = false; el.setAttribute('aria-invalid','true'); } else { el.removeAttribute('aria-invalid'); }
      });
      if(!ok) form.querySelector('[aria-invalid]').focus();
      return ok;
    }
    var clean = function(s){ return s.replace(/[<>&]/g, ''); };
    function firstName(form){ return (form.querySelector('[name="name"]').value.trim().split(' ')[0]) || 'there'; }
    function done(form, html){
      form.innerHTML = '<div class="form-done">' + html + '</div>';
      var h = form.querySelector('h3'); h.setAttribute('tabindex','-1'); h.focus();
    }

    var form = $('appraisal');
    if(form){
      form.addEventListener('submit', function(e){
        e.preventDefault();
        if(!validate(form)) return;
        var name = clean(firstName(form));
        sendLead('appraisal', form);
        done(form, '<p class="label blue">Received</p><h3>Thank you, ' + name + '.</h3><p>Ben will call you within one business day to arrange a time. If it\\u2019s urgent, ring him on <a href="tel:' + PHONE_LINK + '">' + PHONE + '</a>.</p>');
      });
    }

    var modal = $('guideModal'), guideBtn = $('guideBtn');
    if(modal && guideBtn){
      guideBtn.addEventListener('click', function(){ modal.showModal(); });
      $('guideClose').addEventListener('click', function(){ modal.close(); });
      modal.addEventListener('click', function(e){ if(e.target === modal) modal.close(); });
      var gform = $('guideForm');
      gform.addEventListener('submit', function(e){
        e.preventDefault();
        if(!validate(gform)) return;
        var name = clean(firstName(gform));
        sendLead('guide', gform);
        done(gform, '<p class="label blue">On its way</p><h3>Thanks, ' + name + '.</h3><p>Check your inbox for the guide, or open it now.</p><p style="margin-top:6px"><a class="btn btn-blue" href="' + CONFIG.guideUrl + '" download>Download the guide</a></p>');
      });
    }
  })();
</script>'''.replace('REVIEWS_JSON', reviews).replace('PHONE_D', C.PHONE_DISPLAY) \
             .replace('PHONE_L', C.PHONE_LINK).replace('GUIDE_URL', 'guide/ben-potter-selling-guide.pdf') \
             .replace('FORM_KEY', C.FORM_KEY).replace('LEAD_EMAIL', C.LEAD_EMAIL) \
             .replace('REEL_EMBED', C.REEL_EMBED)


# ---------------------------------------------------------------- output files
def sitemap(page_list):
    rows = []
    for p in page_list:
        prio = '1.0' if p['path'] == '' else ('0.9' if p.get('suburb') else '0.8')
        rows.append(f'''  <url>
    <loc>{C.SITE}/{p['path']}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{prio}</priority>
  </url>''')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.w3.org/1999/sitemap/0.9">\n'.replace('1999/sitemap', '1999/sitemap')
            + '\n'.join(rows) + '\n</urlset>\n').replace(
        'http://www.w3.org/1999/sitemap/0.9', 'http://www.sitemaps.org/schemas/sitemap/0.9')


def robots():
    if C.PREVIEW:
        return ('# Preview build: indexing is switched off.\n'
                '# Set PREVIEW = False in tools/content.py before launch.\n'
                'User-agent: *\nDisallow: /\n')
    return ('User-agent: *\nAllow: /\n\n'
            '# AI and answer engines are welcome.\n'
            'User-agent: GPTBot\nAllow: /\n\n'
            'User-agent: PerplexityBot\nAllow: /\n\n'
            'User-agent: Google-Extended\nAllow: /\n\n'
            f'Sitemap: {C.SITE}/sitemap.xml\n')


def redirect_configs():
    os.makedirs(os.path.join(HERE, 'deploy'), exist_ok=True)
    netlify = '\n'.join(f'{a}  {b}  301' for a, b in C.REDIRECTS) + '\n'
    open(os.path.join(HERE, 'deploy/_redirects'), 'w').write(netlify)
    vercel = {"redirects": [{"source": a, "destination": b, "permanent": True} for a, b in C.REDIRECTS]}
    open(os.path.join(HERE, 'deploy/vercel.json'), 'w').write(json.dumps(vercel, indent=2) + '\n')
    ht = ['RewriteEngine On'] + [f'Redirect 301 {a} {C.SITE}{b}' for a, b in C.REDIRECTS]
    open(os.path.join(HERE, 'deploy/.htaccess'), 'w').write('\n'.join(ht) + '\n')


def write(path, text):
    full = os.path.join(HERE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True) if os.path.dirname(full) else None
    open(full, 'w', encoding='utf-8').write(text)


def main():
    page_list = pages()
    # stylesheet + fonts are shared and cached across pages
    shutil.copyfile(os.path.join(HERE, 'src/site.css'), os.path.join(HERE, 'assets/site.css'))

    bodies = {'': home_body(), 'recently-sold/': sold_body(),
              'free-selling-guide/': guide_body(), 'property-appraisal/': appraisal_body()}
    for s in C.SUBURBS:
        bodies[s['slug'] + '/'] = suburb_body(s)

    for p in page_list:
        depth = p['path'].count('/')
        doc = ('<!doctype html>\n<html lang="en-NZ">\n<head>\n' + head(p, depth)
               + '\n</head>\n<body>\n' + bodies[p['path']] + '\n' + script_block() + '\n</body>\n</html>\n')
        write(p['file'], doc)
        print('  ', p['file'], f'{len(doc)/1024:.0f} KB')

    write('sitemap.xml', sitemap(page_list))
    write('robots.txt', robots())
    redirect_configs()

    # Self-contained fragment for the Claude artifact preview (homepage only)
    home = open(os.path.join(HERE, 'index.html'), encoding='utf-8').read()
    frag = home[home.index('<head>') + len('<head>'):home.index('</html>')]
    frag = frag.replace('</head>\n<body>', '').replace('\n</body>\n', '\n')
    frag = frag.replace('<meta name="robots" content="noindex, nofollow">\n', '')
    os.makedirs(os.path.join(HERE, 'dist'), exist_ok=True)
    open(os.path.join(HERE, 'dist/page.html'), 'w', encoding='utf-8').write(frag)
    print('   dist/page.html (artifact fragment)')
    print('built', len(page_list), 'pages + sitemap, robots, redirects')


main()
