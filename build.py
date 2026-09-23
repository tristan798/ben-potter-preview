#!/usr/bin/env python3
"""Renders src/page.html into dist/page.html (artifact fragment) and index.html (hosted page)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'tools'))
import content as C

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')


def card(suburb, addr, meta, result, status, live=False):
    slug = addr.lower().replace(' ', '-')
    cls = ' live' if live else ''
    return f'''        <a class="card" href="#contact" aria-label="{addr}, {suburb}">
          <div class="card-media" data-note="Photography to come"><!-- <img src="img/listings/{slug}.jpg" alt="{addr}, {suburb}"> --></div>
          <div class="card-body">
            <p class="label quiet">{suburb}</p>
            <h3>{addr}</h3>
            <p class="card-meta">{meta}</p>
            <p class="card-meta">{result}</p>
            <p class="card-status{cls}">{status}</p>
          </div>
        </a>'''


def faq_html():
    out = []
    for i, (q, a) in enumerate(C.FAQ):
        out.append(f'''          <details{" open" if i == 0 else ""}>
            <summary>{q}</summary>
            <p>{a}</p>
          </details>''')
    return '\n'.join(out)


def schema():
    def plain(t):
        return t.replace('&amp;', '&').replace('&nbsp;', ' ')
    graph = [{
        "@type": "RealEstateAgent",
        "name": "Ben Potter",
        "description": ("Harcourts Cooper & Co real estate agent for Devonport, Belmont and Bayswater on "
                        "Auckland's North Shore. Ben has been on the Devonport Peninsula for 38 years and also "
                        "sells in Narrow Neck, Stanley Point, Hauraki and Takapuna."),
        "telephone": C.PHONE_LINK,
        "parentOrganization": {"@type": "Organization", "name": "Harcourts Cooper & Co"},
        "address": {"@type": "PostalAddress", "addressLocality": "Devonport", "addressRegion": "Auckland",
                    "addressCountry": "NZ"},
        "areaServed": [
            {"@type": "Place", "name": "Devonport, Auckland",
             "geo": {"@type": "GeoCoordinates", "latitude": -36.8290, "longitude": 174.7961}},
            {"@type": "Place", "name": "Belmont, Auckland",
             "geo": {"@type": "GeoCoordinates", "latitude": -36.8060, "longitude": 174.7898}},
            {"@type": "Place", "name": "Bayswater, Auckland",
             "geo": {"@type": "GeoCoordinates", "latitude": -36.8163, "longitude": 174.7727}},
            {"@type": "Place", "name": "Narrow Neck, Auckland"},
            {"@type": "Place", "name": "Stanley Point, Auckland"},
            {"@type": "Place", "name": "Hauraki, Auckland"},
            {"@type": "Place", "name": "Takapuna, Auckland"},
        ],
        "knowsAbout": ["Devonport real estate", "Belmont real estate", "Bayswater real estate",
                       "Property appraisals", "Auctions", "Heritage villas"],
    }, {
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": plain(q),
                        "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in C.FAQ],
    }]
    body = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2)
    return '<script type="application/ld+json">\n' + body + '\n</script>'


def script():
    reviews = json.dumps([{"t": t, "n": n, "w": w} for t, n, w in C.REVIEWS], indent=6)
    return '''<script>
  (function(){
    // Fill these in as Ben supplies them.
    var CONFIG = {
      formEndpoint: '',                                   // leads POST here as JSON, and Ben is emailed
      guideUrl: 'guide/ben-potter-selling-guide.pdf',     // the selling guide PDF
      reelEmbed: ''                                       // e.g. https://www.youtube.com/embed/VIDEO_ID
    };
    var PHONE = '%s', PHONE_LINK = '%s';

    var header = document.querySelector('.header');
    var menuBtn = document.getElementById('menuBtn');
    menuBtn.addEventListener('click', function(){
      var open = header.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.querySelectorAll('.mobile-nav a').forEach(function(a){
      a.addEventListener('click', function(){ header.classList.remove('open'); menuBtn.setAttribute('aria-expanded','false'); });
    });

    // Active nav follows the section in view
    var navLinks = Array.prototype.slice.call(document.querySelectorAll('.nav a'));
    var sections = navLinks.map(function(a){ return document.querySelector(a.getAttribute('href')); });
    if(window.IntersectionObserver){
      var io = new IntersectionObserver(function(entries){
        entries.forEach(function(en){
          if(!en.isIntersecting) return;
          var i = sections.indexOf(en.target);
          navLinks.forEach(function(a, k){ a.classList.toggle('active', k === i); });
        });
      }, { rootMargin: '-45%% 0px -50%% 0px' });
      sections.forEach(function(s){ if(s) io.observe(s); });
    }

    // Reel: embeds when a link is configured
    var reelBtn = document.getElementById('reelBtn'), reelMsg = document.getElementById('reelMsg');
    reelBtn.addEventListener('click', function(){
      if(CONFIG.reelEmbed){
        var f = document.createElement('iframe');
        f.src = CONFIG.reelEmbed + (CONFIG.reelEmbed.indexOf('?') > -1 ? '&' : '?') + 'autoplay=1';
        f.allow = 'autoplay; fullscreen'; f.title = 'Ben Potter reel';
        f.style.cssText = 'position:absolute;inset:0;width:100%%;height:100%%;border:0';
        reelBtn.innerHTML = ''; reelBtn.appendChild(f);
      } else { reelMsg.hidden = !reelMsg.hidden; }
    });

    var quotes = %s;
    var qi = 0;
    var qText = document.getElementById('quoteText'), qName = document.getElementById('quoteName'),
        qWhere = document.getElementById('quoteWhere'), qCount = document.getElementById('qCount');
    function showQuote(i){
      qi = (i + quotes.length) %% quotes.length;
      qText.textContent = quotes[qi].t; qName.textContent = quotes[qi].n; qWhere.textContent = quotes[qi].w;
      qCount.textContent = (qi + 1) + ' / ' + quotes.length;
    }
    document.getElementById('qPrev').addEventListener('click', function(){ showQuote(qi - 1); });
    document.getElementById('qNext').addEventListener('click', function(){ showQuote(qi + 1); });

    function sendLead(kind, form){
      var data = { kind: kind, page: location.href };
      form.querySelectorAll('input, select, textarea').forEach(function(el){ if(el.name) data[el.name] = el.value.trim(); });
      if(!CONFIG.formEndpoint) return Promise.resolve();
      return fetch(CONFIG.formEndpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data) }).catch(function(){});
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

    var form = document.getElementById('appraisal');
    form.addEventListener('submit', function(e){
      e.preventDefault();
      if(!validate(form)) return;
      var name = clean(firstName(form));
      sendLead('appraisal', form);
      done(form, '<p class="label">Received</p><h3>Thank you, ' + name + '.</h3><p>Ben will call you within one business day to arrange a time. If it\\u2019s urgent, ring him on <a href="tel:' + PHONE_LINK + '">' + PHONE + '</a>.</p>');
    });

    var modal = document.getElementById('guideModal');
    document.getElementById('guideBtn').addEventListener('click', function(){ modal.showModal(); });
    document.getElementById('guideClose').addEventListener('click', function(){ modal.close(); });
    modal.addEventListener('click', function(e){ if(e.target === modal) modal.close(); });
    var gform = document.getElementById('guideForm');
    gform.addEventListener('submit', function(e){
      e.preventDefault();
      if(!validate(gform)) return;
      var name = clean(firstName(gform));
      sendLead('guide', gform);
      done(gform, '<p class="label">On its way</p><h3>Thanks, ' + name + '.</h3><p>Check your inbox for the guide, or open it now.</p><p style="margin-top:6px"><a class="btn btn-blue" href="' + CONFIG.guideUrl + '" download>Download the guide</a></p>');
    });
  })();
</script>''' % (C.PHONE_DISPLAY, C.PHONE_LINK, reviews)


def main():
    tpl = open(os.path.join(HERE, 'src/page.html'), encoding='utf-8').read()
    fonts = open(os.path.join(HERE, 'src/fonts.css'), encoding='utf-8').read().strip()
    page = (tpl
            .replace('/*!FONTS!*/', fonts)
            .replace('{{SOLD}}', '\n' + '\n'.join(card(*r) for r in C.SOLD) + '\n      ')
            .replace('{{SALE}}', '\n' + '\n'.join(card(*r, live=True) for r in C.SALE) + '\n' + offmarket() + '\n      ')
            .replace('{{FAQ}}', '\n' + faq_html() + '\n        ')
            .replace('{{SCHEMA}}', schema())
            .replace('{{SCRIPT}}', script()))
    os.makedirs(os.path.join(HERE, 'dist'), exist_ok=True)
    open(os.path.join(HERE, 'dist/page.html'), 'w', encoding='utf-8').write(page)
    i = page.index('</style>') + len('</style>')
    head = page[:i].replace('<title>Ben Potter</title>', '<title>Ben Potter</title>\n<meta name="robots" content="noindex, nofollow">')
    open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(
        '<!doctype html>\n<html lang="en-NZ">\n<head>\n' + head + '\n</head>\n<body>' + page[i:] + '\n</body>\n</html>\n')
    print('built dist/page.html and index.html')


def offmarket():
    return f'''        <a class="card text-card" href="#contact">
          <div class="card-body">
            <p class="label quiet">Off market</p>
            <h3>Some homes never reach this page.</h3>
            <p class="card-meta">Ben sells a good share of Peninsula homes quietly, to buyers already on his list. Tell him what you're looking for.</p>
            <p class="card-status live">Register as a buyer {ARROW}</p>
          </div>
        </a>'''


main()
