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
        {'path': C.FUNNEL_SLUG + '/', 'file': C.FUNNEL_SLUG + '/index.html',
         'title': C.FUNNEL_TITLE.replace('&', '&amp;'), 'desc': C.FUNNEL_DESC,
         'crumbs': [], 'nav': None, 'funnel': True, 'noindex': True},
        {'path': 'property-appraisal/', 'file': 'property-appraisal/index.html',
         'title': 'Free Property Appraisal | Ben Potter, Harcourts Cooper &amp; Co',
         'desc': ('Book a free, no obligation property appraisal anywhere on Auckland\'s North Shore. A '
                  'written estimate from recent comparable sales, plus a recommended method of sale.'),
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
      <p class="trust"><a href="{C.RATEMYAGENT}" rel="noopener">Over {C.REVIEW_COUNT} five-star reviews on RateMyAgent</a></p>
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
        <p class="lede">A written appraisal of your home, built from recent comparable sales nearby, and an honest view on what it needs before the first open home.</p>
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
    <h3 id="guideTitle">Where should Ben send it?</h3>
    <p class="muted" style="font-size:.95rem">{C.GUIDE_TITLE}, {C.GUIDE_PAGES} pages. It arrives in your inbox in a moment.</p>
    <form id="guideForm" novalidate>
      <div class="field"><label for="g-name">Name</label><input id="g-name" name="name" type="text" autocomplete="name" required></div>
      <div class="field"><label for="g-email">Email</label><input id="g-email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="g-phone">Mobile</label><input id="g-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel"></div>
      <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <div class="form-foot"><button class="btn btn-blue" type="submit">Email me the guide</button><small>One email with the guide. No list, no spam.</small></div>
    </form>
  </div>
</dialog>'''


# ---------------------------------------------------------------- page bodies
def home_body():
    d = 0
    sold = '\n'.join(card(*r, depth=d) for r in C.SOLD[:3])
    return f'''{header(d, 'home')}

<main>
  <div class="first-screen">
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
        <figure class="reel-wrap">
          <div class="reel" id="reelBtn" role="button" tabindex="0" aria-label="Play the reel: {C.REEL_TITLE}">
            <video id="reelVideo" poster="{C.REEL_POSTER}" preload="none" playsinline
                   width="720" height="1280" aria-label="{C.REEL_TITLE}">
              <source src="{C.REEL_FILE}" type="video/mp4">
            </video>
            <span class="reel-ring" aria-hidden="true"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></span>
          </div>
          <figcaption class="reel-caption"><b>{C.REEL_TITLE}</b><span>Watch the reel &nbsp;·&nbsp; {C.REEL_SECONDS} sec</span></figcaption>
        </figure>
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


def funnel_body():
    d = 1
    steps = []
    for i, st in enumerate(C.FUNNEL_STEPS):
        n = i + 1
        help_html = f'<p class="step-help">{st["help"]}</p>' if st.get('help') else ''
        if st['type'] == 'text':
            field = (f'<input class="step-input" id="q-{st["key"]}" name="{st["key"]}" type="text" '
                     f'autocomplete="street-address" placeholder="{st.get("placeholder","")}" '
                     f'inputmode="text" data-required="1">')
        elif st['type'] == 'choice':
            opts = '\n'.join(
                f'            <button class="opt" type="button" data-field="{st["key"]}" data-value="{o}">{o}</button>'
                for o in st['options'])
            field = f'<div class="opts" role="group" aria-label="{st["q"]}">\n{opts}\n          </div>'
        else:
            field = '''<div class="step-fields">
            <div class="field"><label for="q-name">Name</label><input id="q-name" name="name" type="text" autocomplete="name" data-required="1"></div>
            <div class="field"><label for="q-phone">Mobile</label><input id="q-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" data-required="1"></div>
            <div class="field"><label for="q-email">Email</label><input id="q-email" name="email" type="email" autocomplete="email" data-required="1"></div>
          </div>'''
        if st['type'] == 'contact':
            nav = '<button class="btn btn-blue" type="submit">Send me my appraisal</button>'
        elif st['type'] == 'choice':
            nav = ''
        else:
            nav = '<button class="btn btn-blue step-next" type="button">Continue</button>'
        back = '<button class="step-back" type="button">Back</button>' if i else ''
        navrow = f'<div class="step-nav">{nav}{back}</div>' if (nav or back) else ''
        steps.append(f'''        <fieldset class="step" data-step="{n}" {"" if i == 0 else "hidden"}>
          <legend class="step-q">{st["q"]}</legend>
          {help_html}
          {field}
          {navrow}
        </fieldset>''')

    promise = '\n'.join(f'''        <div class="promise">
          <span class="promise-n" aria-hidden="true">{i:02d}</span>
          <h3>{t}</h3>
          <p>{b}</p>
        </div>''' for i, (t, b) in enumerate(C.FUNNEL_PROMISE, start=1))
    faq = faq_block(C.FUNNEL_FAQ, open_first=False)

    return f'''<header class="header funnel-header">
  <div class="wrap">
    <span class="wordmark">Ben Potter</span>
    <a class="phone-link" href="tel:{C.PHONE_LINK}">{C.PHONE_DISPLAY}</a>
  </div>
</header>

<main>
  <section class="funnel-hero" aria-labelledby="funnelTitle">
    <div class="hero-glow" aria-hidden="true"></div>
    <div class="wrap funnel-stack">
      <p class="label blue">Free property appraisal</p>
      <h1 id="funnelTitle">{C.FUNNEL_H1}</h1>
      <p class="lede">{C.FUNNEL_LEDE}</p>

      <div class="funnel-card">
        <form id="funnelForm" novalidate>
          <div class="card-head">
            <div class="progress" aria-hidden="true"><span id="progressBar"></span></div>
            <p class="step-count">Step <span id="stepNow">1</span> of {len(C.FUNNEL_STEPS)}</p>
          </div>
{chr(10).join(steps)}
          <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
          <p class="step-foot">Free, no obligation, and Ben replies personally.</p>
        </form>
        <div class="funnel-done" id="funnelDone" hidden>
          <p class="label blue">Received</p>
          <h2 id="doneTitle">Thanks, <span id="doneName">there</span>.</h2>
          <p>Ben will call you within one business day to arrange a time to see the property.</p>
          <p class="done-actions">
            <a class="btn btn-blue" href="tel:{C.PHONE_LINK}">Call Ben now</a>
            <a class="btn btn-line" href="../free-selling-guide/">Read the selling guide</a>
          </p>
        </div>
      </div>

      <ul class="trust-row">
        <li><b>38 years</b><span>On the North Shore</span></li>
        <li><b>{C.REVIEW_COUNT}+ five-star</b><span>Verified reviews</span></li>
        <li><b>Harcourts</b><span>Cooper &amp; Co</span></li>
      </ul>
    </div>
  </section>

  <section class="section on-light funnel-section" aria-labelledby="promiseTitle">
    <div class="wrap">
      <div class="funnel-head">
        <p class="label blue">What you get</p>
        <h2 id="promiseTitle">More than a number.</h2>
      </div>
      <div class="promises">
{promise}
      </div>
    </div>
  </section>

  <section class="section words funnel-section" aria-labelledby="fReviews">
    <div class="wrap">
      <h2 class="label" id="fReviews">In their words</h2>
      <p class="stars" aria-hidden="true" style="margin-top:1.2rem">★★★★★</p>
      <blockquote class="quote" id="quoteText">{C.REVIEWS[0][0]}</blockquote>
      <div class="quote-by"><b id="quoteName">{C.REVIEWS[0][1]}</b><span id="quoteWhere">{C.REVIEWS[0][2]}</span></div>
      <div class="quote-nav">
        <button type="button" id="qPrev" aria-label="Previous review"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 18l-6-6 6-6"/></svg></button>
        <span class="count" id="qCount" aria-live="polite">1 / {len(C.REVIEWS)}</span>
        <button type="button" id="qNext" aria-label="Next review"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
      </div>
      <p class="trust"><a href="{C.RATEMYAGENT}" rel="noopener">Over {C.REVIEW_COUNT} five-star reviews on RateMyAgent</a></p>
    </div>
  </section>

  <section class="section on-light funnel-section" aria-labelledby="fFaq">
    <div class="wrap funnel-narrow">
      <div class="funnel-head">
        <p class="label blue">Before you ask</p>
        <h2 id="fFaq">The honest answers.</h2>
      </div>
      <div class="faq-list">
{faq}
      </div>
    </div>
  </section>

  <section class="section funnel-close">
    <div class="wrap">
      <h2>Ready when you are.</h2>
      <p class="lede">Five questions, about a minute, and nothing to sign.</p>
      <p><a class="btn btn-blue" href="#funnelTitle">Start my appraisal</a></p>
      <p class="or">or call Ben on <a href="tel:{C.PHONE_LINK}">{C.PHONE_DISPLAY}</a></p>
    </div>
  </section>
</main>

<footer class="footer funnel-footer">
  <div class="wrap">
    <div class="footer-bottom">
      <span>© {date.today().year} {C.AGENT_NAME} · {C.AGENCY} · Licensed under the REA Act 2008</span>
      <span><a href="tel:{C.PHONE_LINK}">{C.PHONE_DISPLAY}</a></span>
    </div>
  </div>
</footer>'''


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
    half = (len(C.GUIDE_CONTENTS) + 1) // 2
    cols = [C.GUIDE_CONTENTS[:half], C.GUIDE_CONTENTS[half:]]
    lists = '\n'.join(
        '          <ul>\n' + '\n'.join(f'            <li>{t}</li>' for t in col) + '\n          </ul>'
        for col in cols)
    return f'''{header(d, 'guide')}

<main>
  <section class="page-hero guide-hero" aria-labelledby="pageTitle">
    <div class="hero-glow" aria-hidden="true"></div>
    <div class="wrap guide-grid">
      <div class="guide-copy">
        {crumbs([('Free selling guide', None)], d)}
        <p class="label blue">Free download &nbsp;·&nbsp; {C.GUIDE_PAGES} pages</p>
        <h1 id="pageTitle">A proven strategy to <em>maximise your sale price.</em></h1>
        <p class="lede">{C.GUIDE_STRAP} Written by Ben from {C.YEARS} years selling on the Devonport Peninsula, for owners who want to know what actually moves the price before they go to market.</p>
        <div class="page-actions">
          <button class="btn btn-blue" type="button" id="guideBtn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11M7 10l5 5 5-5M5 19h14"/></svg>
            Download the guide
          </button>
        </div>
        <a class="quietlink" href="../property-appraisal/">or book a free appraisal {ARROW}</a>
      </div>
      <figure class="guide-cover">
        <img src="../{C.GUIDE_COVER}" alt="Cover of Ben Potter's selling guide, A Proven Strategy to Maximise Your Sale Price" width="706" height="1000" loading="eager" decoding="async">
      </figure>
    </div>
  </section>

  <section class="section on-light" aria-labelledby="insideTitle">
    <div class="wrap guide-inside">
      <div class="funnel-head">
        <p class="label blue">What's inside</p>
        <h2 id="insideTitle">Fourteen short chapters.</h2>
      </div>
      <p class="guide-note">Written for homes on this peninsula, not generic advice about selling anywhere in New Zealand.</p>
      <div class="guide-contents">
{lists}
      </div>
      <blockquote class="guide-pull">The difference between an average result and a premium sale price is not luck. It is preparation and positioning.</blockquote>
    </div>
  </section>

  <section class="section funnel-close">
    <div class="wrap">
      <h2>Get your copy.</h2>
      <p class="lede">Enter your details and Ben emails it straight to you.</p>
      <p><button class="btn btn-blue" type="button" id="guideBtn2">Download the guide</button></p>
      <p class="or">or call Ben on <a href="tel:{C.PHONE_LINK}">{C.PHONE_DISPLAY}</a></p>
    </div>
  </section>
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
      <p class="lede">A written appraisal of your property, built from recent comparable sales nearby, with an honest view on what it needs before the first open home. Anywhere on Auckland's North Shore.</p>
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
          <div><dt>Covers</dt><dd>Auckland's North Shore</dd></div>
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
        graph.append({
            "@type": "VideoObject", "@id": url + "#reel",
            "name": C.REEL_TITLE,
            "description": esc(C.REEL_DESC),
            "thumbnailUrl": C.SITE + "/" + C.REEL_POSTER,
            "contentUrl": C.SITE + "/" + C.REEL_FILE,
            "uploadDate": C.REEL_DATE,
            "duration": f"PT{C.REEL_SECONDS}S",
            "creator": {"@id": PERSON_ID},
            "publisher": {"@id": AGENT_ID},
            "inLanguage": "en-NZ",
            "isFamilyFriendly": True,
        })
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
        if page['path'] == 'free-selling-guide/':
            graph.append({
                "@type": "DigitalDocument", "@id": url + "#guide",
                "name": C.GUIDE_TITLE,
                "description": esc(f"{C.GUIDE_STRAP} A {C.GUIDE_PAGES} page guide to preparing and "
                                   f"positioning a North Shore home for a premium sale."),
                "author": {"@id": PERSON_ID},
                "publisher": {"@id": AGENT_ID},
                "inLanguage": "en-NZ",
                "encodingFormat": "application/pdf",
                "url": C.SITE + "/" + C.GUIDE_FILE,
                "isAccessibleForFree": True,
                "about": [{"@type": "Thing", "name": t} for t in C.GUIDE_CONTENTS],
            })
        if page['path'] == 'property-appraisal/':
            graph.append(faq_schema(C.FAQ_APPRAISAL, url))
            graph.append({"@type": "Service", "@id": url + "#service",
                          "name": "Free property appraisal, Devonport Peninsula",
                          "serviceType": "Property appraisal",
                          "provider": {"@id": AGENT_ID},
                          "areaServed": {"@type": "Place", "name": "North Shore, Auckland, New Zealand"},
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
              if (C.PREVIEW or page.get('noindex')) else
              '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">')
    gsc = f'\n<meta name="google-site-verification" content="{C.GSC_TOKEN}">' if C.GSC_TOKEN else ''
    ga = ''
    if C.GA4_ID:
        ga = f'''
<script async src="https://www.googletagmanager.com/gtag/js?id={C.GA4_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{C.GA4_ID}');</script>'''
    pixel = ''
    if page.get('funnel') and C.META_PIXEL_ID:
        pixel = ('\n<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?'
                 'n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;'
                 'n.push=n;n.loaded=!0;n.version="2.0";n.queue=[];t=b.createElement(e);t.async=!0;'
                 't.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}'
                 '(window,document,"script","https://connect.facebook.net/en_US/fbevents.js");'
                 f'fbq("init","{C.META_PIXEL_ID}");fbq("track","PageView");</script>')
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
<link rel="stylesheet" href="{d}assets/site.css">{ga}{pixel}
<script type="application/ld+json">
{schema}
</script>'''


def script_block(depth=0):
    reviews = json.dumps([{"t": t, "n": n, "w": w} for t, n, w in C.REVIEWS], indent=6, ensure_ascii=False)
    js = '''<script>
  (function(){
    // Fill these in as Ben supplies them.
    var CONFIG = {
      // Where appraisal and guide submissions are emailed. See tools/content.py.
      provider: '@@FORM_PROVIDER@@',
      formKey: '@@FORM_KEY@@',
      leadEmail: '@@LEAD_EMAIL@@',
      formAlias: '@@FORM_ALIAS@@',
      formEndpoint: '@@FORM_ENDPOINT@@',
      guideUrl: '@@GUIDE_URL@@',                           // the selling guide PDF
      replyGuide: @@REPLY_GUIDE@@,                         // confirmation emailed to the requester
      replyAppraisal: @@REPLY_APPRAISAL@@
    };
    var PHONE = '@@PHONE_DISPLAY@@', PHONE_LINK = '@@PHONE_LINK@@';
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

    var reelBtn = $('reelBtn'), reelVideo = $('reelVideo');
    if(reelBtn && reelVideo){
      function playReel(){
        if(reelBtn.classList.contains('playing')){
          reelVideo.paused ? reelVideo.play() : reelVideo.pause();
          return;
        }
        reelBtn.classList.add('playing');
        reelVideo.controls = true;
        reelVideo.play();
      }
      reelBtn.addEventListener('click', playReel);
      reelBtn.addEventListener('keydown', function(e){
        if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); playReel(); }
      });
      reelVideo.addEventListener('ended', function(){
        reelBtn.classList.remove('playing');
        reelVideo.controls = false;
        reelVideo.load();
      });
    }

    var quotes = @@REVIEWS_JSON@@;
    var qi = 0, qText = $('quoteText'), qName = $('quoteName'), qWhere = $('quoteWhere'), qCount = $('qCount');
    function showQuote(i){
      qi = (i + quotes.length) % quotes.length;
      qText.innerHTML = quotes[qi].t; qName.textContent = quotes[qi].n; qWhere.textContent = quotes[qi].w;
      qCount.textContent = (qi + 1) + ' / ' + quotes.length;
    }
    if(qText){
      var timer = null, REVIEW_MS = 7000;
      var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      function start(){ if(!reduce && !timer) timer = setInterval(function(){ showQuote(qi + 1); }, REVIEW_MS); }
      function stop(){ if(timer){ clearInterval(timer); timer = null; } }
      function step(n){ stop(); showQuote(n); start(); }
      $('qPrev').addEventListener('click', function(){ step(qi - 1); });
      $('qNext').addEventListener('click', function(){ step(qi + 1); });
      var band = qText.closest('section');
      if(band){
        ['mouseenter','focusin'].forEach(function(e){ band.addEventListener(e, stop); });
        ['mouseleave','focusout'].forEach(function(e){ band.addEventListener(e, start); });
      }
      document.addEventListener('visibilitychange', function(){ document.hidden ? stop() : start(); });
      start();
    }

    function sendLead(kind, form, preset){
      var data = preset || {};
      if(!preset){
        form.querySelectorAll('input, select, textarea').forEach(function(el){
          if(!el.name) return;
          data[el.name] = (el.type === 'checkbox') ? el.checked : el.value.trim();
        });
      }
      var label = kind === 'guide' ? 'Selling guide download'
                : kind === 'funnel' ? 'Appraisal request (Meta ad)'
                : 'Appraisal request';
      var subject = label + ' from ' + (data.name || 'the website') + (data.address ? ', ' + data.address : '');
      var fields = {
        Enquiry: label,
        Name: data.name || '',
        Mobile: data.phone || '',
        Email: data.email || '',
        Property: data.address || '',
        Timeframe: data.timeframe || '',
        PropertyType: data.type || '',
        Bedrooms: data.bedrooms || '',
        Page: location.href
      };
      var url, payload;
      if(CONFIG.provider === 'endpoint'){
        url = CONFIG.formEndpoint;
        payload = Object.assign({ kind: kind, botcheck: data.botcheck || false }, data);
      } else if(CONFIG.provider === 'web3forms' && CONFIG.formKey){
        url = 'https://api.web3forms.com/submit';
        payload = Object.assign({ access_key: CONFIG.formKey, subject: subject,
                                  from_name: 'ben-potter.com', replyto: data.email || '',
                                  botcheck: data.botcheck || false }, fields);
      } else if(CONFIG.provider === 'formsubmit'){
        url = 'https://formsubmit.co/ajax/' + (CONFIG.formAlias || CONFIG.leadEmail);
        payload = Object.assign({ _subject: subject, _template: 'table',
                                  _replyto: data.email || '',
                                  _autoresponse: (kind === 'guide' ? CONFIG.replyGuide : CONFIG.replyAppraisal),
                                  _honey: data.botcheck ? 'bot' : '' }, fields);
      } else {
        console.warn('Lead delivery is off: this submission was not emailed. See README.');
        return Promise.resolve();
      }
      return fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(payload)
      }).then(function(r){ return r.json(); })
        .then(function(j){ if(!j || String(j.success) !== 'true') throw new Error('not delivered'); })
        .catch(function(){
          deliveryFailed(fields);
          throw new Error('lead delivery failed');
        });
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
    // If the provider is unreachable, hand the visitor a way to reach Ben anyway.
    function deliveryFailed(fields){
      var lines = Object.keys(fields).map(function(k){ return k + ': ' + fields[k]; }).join('%0D%0A');
      var href = 'mailto:@@LEAD_EMAIL@@?subject=' + encodeURIComponent('Appraisal enquiry') + '&body=' + lines;
      var box = document.createElement('div');
      box.className = 'send-failed';
      box.innerHTML = '<p><b>That did not send.</b> Please call Ben on <a href="tel:@@PHONE_LINK@@">@@PHONE_DISPLAY@@</a> ' +
                      'or <a href="' + href + '">email him directly</a>.</p>';
      var host = document.querySelector('.form-card') || document.querySelector('.funnel-card') || document.body;
      host.appendChild(box);
    }
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

    // ---- Scroll reveal, applied globally. The class is added by script, so if this file
    // ---- ever fails to run the content is still visible rather than stuck at opacity 0.
    (function(){
      if(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      if(!('IntersectionObserver' in window)) return;
      var sel = ['.section .split-head', '.section .areas-head', '.section .list-head',
                 '.content-main > .block', '.aside > *', '.card', '.switch > a', '.stat',
                 '.faq-list details', '.form-card', '.appraise-copy', '.promise',
                 '.reel-wrap', '.quote-by', '.secondary', '.page-hero .lede',
                 '.page-hero h1', '.page-hero .crumbs', '.funnel-close > .wrap > *'].join(',');
      var els = Array.prototype.slice.call(document.querySelectorAll(sel));
      if(!els.length) return;
      els.forEach(function(el){
        el.classList.add('reveal');
        var sibs = el.parentNode ? Array.prototype.slice.call(el.parentNode.children) : [];
        var i = sibs.indexOf(el);
        if(i > 0 && i < 8) el.style.transitionDelay = (i * 70) + 'ms';
      });
      var io = new IntersectionObserver(function(entries){
        entries.forEach(function(en){
          if(!en.isIntersecting) return;
          en.target.classList.add('in');
          io.unobserve(en.target);
        });
      }, { rootMargin: '0px 0px -10% 0px', threshold: 0 });
      function inView(el){
        var r = el.getBoundingClientRect();
        return r.top < window.innerHeight && r.bottom > 0;
      }
      requestAnimationFrame(function(){
        els.forEach(function(el){
          if(inView(el)){ el.style.transitionDelay = '0ms'; el.classList.add('in'); }
          else { io.observe(el); }
        });
      });
      // safety net: never leave something on screen stuck invisible
      setTimeout(function(){
        els.forEach(function(el){ if(inView(el)) el.classList.add('in'); });
      }, 1200);
    })();

    // ---- Paid-ads funnel: one question at a time ----
    var fForm = $('funnelForm');
    if(fForm){
      var steps = Array.prototype.slice.call(fForm.querySelectorAll('.step'));
      var answers = {}, at = 0;
      var bar = $('progressBar'), now = $('stepNow');
      function paint(){
        steps.forEach(function(s, i){ s.hidden = (i !== at); });
        bar.style.width = Math.round(((at) / steps.length) * 100) + '%';
        now.textContent = at + 1;
        var focusable = steps[at].querySelector('input, .opt');
        if(focusable && focusable.tagName === 'INPUT') focusable.focus({preventScroll:true});
      }
      function valid(step){
        var ok = true;
        step.querySelectorAll('[data-required]').forEach(function(el){
          var bad = !el.value.trim() || (el.type === 'email' && el.value.indexOf('@') < 0);
          el.classList.toggle('bad', bad);
          if(bad) ok = false;
        });
        return ok;
      }
      function go(n){
        if(n > at && !valid(steps[at])) return;
        at = Math.max(0, Math.min(steps.length - 1, n));
        paint();
      }
      fForm.addEventListener('click', function(e){
        var opt = e.target.closest('.opt');
        if(opt){
          answers[opt.getAttribute('data-field')] = opt.getAttribute('data-value');
          opt.parentNode.querySelectorAll('.opt').forEach(function(o){ o.classList.remove('on'); });
          opt.classList.add('on');
          setTimeout(function(){ go(at + 1); }, 180);
          return;
        }
        if(e.target.closest('.step-next')) go(at + 1);
        if(e.target.closest('.step-back')) go(at - 1);
      });
      fForm.addEventListener('keydown', function(e){
        if(e.key === 'Enter' && e.target.classList.contains('step-input')){
          e.preventDefault(); go(at + 1);
        }
      });
      fForm.addEventListener('submit', function(e){
        e.preventDefault();
        if(!valid(steps[at])) return;
        fForm.querySelectorAll('input').forEach(function(el){
          if(el.name && el.type !== 'checkbox') answers[el.name] = el.value.trim();
        });
        answers.botcheck = fForm.querySelector('[name=botcheck]').checked;
        sendLead('funnel', fForm, answers);
        if(window.fbq) fbq('track', 'Lead', { content_name: 'Home appraisal funnel' });
        $('doneName').textContent = clean((answers.name || 'there').split(' ')[0]);
        fForm.hidden = true;
        var done = $('funnelDone');
        done.hidden = false;
        done.querySelector('h2').setAttribute('tabindex', '-1');
        done.querySelector('h2').focus();
      });
      paint();
    }

    var modal = $('guideModal'), guideBtn = $('guideBtn');
    if(modal && guideBtn){
      guideBtn.addEventListener('click', function(){ modal.showModal(); });
      var guideBtn2 = $('guideBtn2');
      if(guideBtn2) guideBtn2.addEventListener('click', function(){ modal.showModal(); });
      $('guideClose').addEventListener('click', function(){ modal.close(); });
      modal.addEventListener('click', function(e){ if(e.target === modal) modal.close(); });
      var gform = $('guideForm');
      gform.addEventListener('submit', function(e){
        e.preventDefault();
        if(!validate(gform)) return;
        var name = clean(firstName(gform));
        sendLead('guide', gform);
        done(gform, '<p class="label blue">On its way</p><h3>Check your inbox, ' + name + '.</h3><p>The guide is on its way to your email now. It usually lands within a minute.</p><p class="micro-fallback">Not there? <a href="' + CONFIG.guideUrl + '" target="_blank" rel="noopener">open it here</a>, and check your junk folder.</p>');
      });
    }
  })();
</script>'''
    tokens = {
        '@@REVIEWS_JSON@@': reviews,
        '@@PHONE_DISPLAY@@': C.PHONE_DISPLAY,
        '@@PHONE_LINK@@': C.PHONE_LINK,
        '@@GUIDE_URL@@': rel(depth) + C.GUIDE_FILE,
        '@@FORM_KEY@@': C.FORM_KEY,
        '@@LEAD_EMAIL@@': C.LEAD_EMAIL,
        '@@FORM_ALIAS@@': getattr(C, 'FORM_ALIAS', ''),
        '@@FORM_ENDPOINT@@': getattr(C, 'FORM_ENDPOINT', '/api/lead'),
        '@@FORM_PROVIDER@@': C.FORM_PROVIDER,
        '@@REPLY_GUIDE@@': json.dumps(C.guide_autoresponse(C.SITE)),
        '@@REPLY_APPRAISAL@@': json.dumps(C.appraisal_autoresponse(C.SITE)),
    }
    for k, v in tokens.items():
        js = js.replace(k, v)
    assert '@@' not in js, 'unsubstituted token left in the script block'
    return js


# ---------------------------------------------------------------- output files
def sitemap(page_list):
    rows = []
    for p in page_list:
        if p.get('noindex'):
            continue
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



def check_scripts(page_list):
    """Parse every generated inline script with node. Two shipped syntax errors is enough."""
    import subprocess
    if not shutil.which('node'):
        print('   ! node not found, skipping script syntax check')
        return
    for p in page_list:
        html = open(os.path.join(HERE, p['file']), encoding='utf-8').read()
        for m in re.finditer(r'<script>(.*?)</script>', html, re.S):
            r = subprocess.run(['node', '--check', '-'], input=m.group(1),
                               text=True, capture_output=True)
            if r.returncode != 0:
                raise SystemExit('SCRIPT SYNTAX ERROR in %s:\n%s' % (p['file'], r.stderr.strip()))
    print('   script syntax checked on', len(page_list), 'pages')


def main():
    page_list = pages()
    # stylesheet + fonts are shared and cached across pages
    shutil.copyfile(os.path.join(HERE, 'src/site.css'), os.path.join(HERE, 'assets/site.css'))

    bodies = {'': home_body(), 'recently-sold/': sold_body(),
              'free-selling-guide/': guide_body(), 'property-appraisal/': appraisal_body(),
              C.FUNNEL_SLUG + '/': funnel_body()}
    for s in C.SUBURBS:
        bodies[s['slug'] + '/'] = suburb_body(s)

    for p in page_list:
        depth = p['path'].count('/')
        doc = ('<!doctype html>\n<html lang="en-NZ">\n<head>\n' + head(p, depth)
               + '\n</head>\n<body>\n' + bodies[p['path']] + '\n' + script_block(depth) + '\n</body>\n</html>\n')
        write(p['file'], doc)
        print('  ', p['file'], f'{len(doc)/1024:.0f} KB')

    check_scripts(page_list)
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
