import re, io, sys, os
p=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','src','page.html')
s=open(p,encoding='utf-8').read()
lines=s.split('\n')

def block(start_marker, end_marker, new, start_at=0):
    """replace from the line containing start_marker to the line containing end_marker (inclusive)"""
    global lines
    i=next(k for k in range(start_at,len(lines)) if start_marker in lines[k])
    j=next(k for k in range(i,len(lines)) if end_marker in lines[k])
    lines[i:j+1]=new.rstrip('\n').split('\n')

ARROW='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
DL='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v11M7 10l5 5 5-5M5 19h14"/></svg>'
HOUSE='<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"><path d="M8 22 24 9l16 13"/><path d="M12 20v18h24V20"/><path d="M21 38V27h6v11"/></svg>'

# ---------------- HERO ----------------
block('<section class="hero" aria-labelledby="heroTitle">','  </section>', f'''  <section class="hero" aria-labelledby="heroTitle">
    <div class="hero-photo" aria-hidden="true"></div>
    <div class="hero-glow" aria-hidden="true"></div>
    <div class="wrap">
      <div class="hero-copy">
        <p class="label rise d1">Real estate agent &nbsp;·&nbsp; Harcourts Cooper &amp; Co</p>
        <h1 id="heroTitle" class="rise d2 suburb-title">
          <span class="suburb-line"><span>Devonport</span><small>36.8290° S &nbsp;·&nbsp; 174.7961° E</small></span>
          <span class="suburb-line"><span>Belmont</span><small>36.8060° S &nbsp;·&nbsp; 174.7898° E</small></span>
          <span class="suburb-line"><span>Bayswater<em>.</em></span><small>36.8163° S &nbsp;·&nbsp; 174.7727° E</small></span>
        </h1>
        <p class="sub rise d3">Nearly forty years in the neighbourhood. Ben Potter has lived on the Devonport peninsula for 38 years and sells its homes with Harcourts Cooper &amp; Co. Talk to him before you list, not after.</p>
        <div class="hero-actions rise d4">
          <a class="btn btn-ivory" href="#contact">Book a free appraisal</a>
          <button class="btn btn-line" type="button" id="guideBtn">Free selling guide {DL}</button>
        </div>
      </div>
      <figure class="hero-figure">
        <img src="img/ben.png" alt="Ben Potter" width="1122" height="1402" fetchpriority="high">
      </figure>
    </div>
    <p class="hero-scroll" aria-hidden="true">Scroll</p>
  </section>''')

# ---------------- ABOUT: reel caption ----------------
s2='\n'.join(lines)
s2=s2.replace('<span class="reel-caption"><b>Nearly forty years in the neighbourhood</b><span>Watch the film · 45 sec</span></span>',
              '<span class="reel-caption"><b>Ben on Devonport, Belmont and Bayswater</b><span>Watch the reel</span></span>')
s2=s2.replace('<p class="reel-msg muted" id="reelMsg" hidden>Film slot. The promo reel plays here, muted with captions.</p>',
              '<p class="reel-msg muted" id="reelMsg" hidden>Reel slot. Add a YouTube or Vimeo link in the page config and it plays here.</p>')
lines=s2.split('\n')

# ---------------- SUBURBS ----------------
def row(name, blurb, tags):
    t=''.join(f'<li>{x}</li>' for x in tags)
    return f'''          <a class="row" href="#contact">
            <h3>{name}</h3>
            <div class="row-body">
              <p>{blurb}</p>
              <ul class="tags" aria-label="{name} search terms">{t}</ul>
            </div>
            <span class="arrow" aria-hidden="true">{ARROW}</span>
          </a>'''
block('<section class="section" id="suburbs" aria-labelledby="suburbsTitle">','  </section>', f'''  <section class="section" id="suburbs" aria-labelledby="suburbsTitle">
    <div class="wrap split">
      <p class="label">The Peninsula</p>
      <div>
        <h2 id="suburbsTitle">Three suburbs. <em>One agent.</em></h2>
        <p class="muted" style="margin-top:1.2rem; max-width:56ch">Ben Potter is the local real estate agent for Devonport, Belmont and Bayswater on Auckland's North Shore: appraisals, sales, auctions and off-market introductions across the whole Devonport peninsula.</p>
        <div class="rows">
{row("Devonport","Heritage villas, Cheltenham Beach and the ferry. Devonport real estate is the most tightly held on the North Shore: Victorian and Edwardian villas around Vauxhall Road, Cheltenham and Stanley Point, bungalows near Narrow Neck, and apartments by the wharf. Ben appraises, markets and sells Devonport homes across every price bracket.",["Devonport real estate","Houses for sale Devonport","Devonport property appraisal","Devonport villas","Cheltenham","Narrow Neck","Stanley Point","Vauxhall","Mt Victoria","Devonport ferry"])}
{row("Belmont","Family homes on the flat between Devonport and Takapuna. Belmont real estate is driven by the Takapuna Grammar and Belmont Intermediate zones, generous sections and a short run up Lake Road: 1950s bungalows, renovated weatherboards and new townhouses, with Ngataringa Bay and the Belmont shops on the doorstep.",["Belmont real estate","Houses for sale Belmont","Belmont property appraisal","Belmont Intermediate zone","Takapuna Grammar zone","Lake Road","Ngataringa Bay","Family homes Belmont"])}
{row("Bayswater","Water on three sides, the marina and views back to the city. Bayswater real estate is quieter than its neighbours and buyers know it: townhouses and apartments on the ridge, weatherboard homes on the flat, with the Bayswater Marina ferry and Bayswater School a short walk away.",["Bayswater real estate","Houses for sale Bayswater","Bayswater property appraisal","Bayswater Marina","Harbour views","Bayswater School","Townhouses Bayswater","City ferry"])}
        </div>
        <p class="also">Ben also sells in <a href="#faq">Narrow Neck</a>, <a href="#faq">Stanley Point</a>, <a href="#faq">Hauraki</a> and <a href="#faq">Takapuna</a>.</p>
      </div>
    </div>
  </section>''')

# ---------------- RESULTS ----------------
def card(suburb, addr, meta, date, live=False):
    tag = f'<span class="card-date live">{date}</span>' if live else f'<span class="card-date">{date}</span>'
    return f'''        <a class="card" href="#contact">
          <div class="card-media" aria-hidden="true">{HOUSE}<span>Photo</span></div>
          <div class="card-body"><p class="label">{suburb}</p><h3>{addr}</h3><p class="card-meta">{meta}</p>{tag}</div>
        </a>'''
block('<section class="section light white" id="results" aria-labelledby="resultsTitle">','  </section>', f'''  <section class="section light white" id="results" aria-labelledby="resultsTitle">
    <div class="wrap">
      <div class="results-head">
        <div><p class="label">Results</p><h2 id="resultsTitle">Recently <em>sold.</em></h2></div>
        <p class="muted">Every sale handled by Ben from the first appraisal to settlement. Select a property for the full story.</p>
      </div>
      <div class="cards">
{card("Bayswater","Roberts Avenue","4 bed · 2 bath · Auction, three registered bidders","Sold · Aug 2026")}
{card("Devonport","Old Lake Road","4 bed · 2 bath · Sold prior to auction in nine days","Sold · Jul 2026")}
{card("Belmont","Kiri Place","5 bed · 3 bath · Deadline sale","Sold · Jul 2026")}
{card("Devonport","Mozeley Avenue","4 bed · 2 bath · Off market to a local buyer","Sold · Jun 2026")}
{card("Belmont","Seabreeze Road","3 bed · 2 bath · Auction, above reserve","Sold · May 2026")}
{card("Devonport","Vauxhall Road","3 bed · 1 bath · By negotiation in three weeks","Sold · May 2026")}
      </div>

      <div class="results-head second">
        <div><h2>Currently for <em>sale.</em></h2></div>
        <a class="textlink" href="#contact">Register as a buyer {ARROW}</a>
      </div>
      <div class="cards">
{card("Devonport","Cheltenham Road","4 bed · 2 bath · Open home Sat and Sun 12.00","Auction · 8 October",True)}
{card("Belmont","Bardia Street","3 bed · 2 bath · Open home Sun 1.00","Deadline · 2 October",True)}
        <a class="card card-cta" href="#contact">
          <div class="card-body"><p class="label">Off market</p><h3>Some homes never reach this page.</h3><p class="card-meta">Ben sells a good share of peninsula homes quietly to buyers already on his list. Tell him what you're after.</p><span class="card-date">Register as a buyer</span></div>
        </a>
      </div>
      <p class="ledger-note">Sample entries for layout. Photos and details connect to Ben's CRM feed, or are uploaded manually.</p>
    </div>
  </section>''')

# ---------------- REVIEWS: trust line ----------------
s2='\n'.join(lines)
s2=s2.replace('<p class="rma">Verified reviews on RateMyAgent <span aria-hidden="true">·</span>','<p class="rma">Verified reviews on RateMyAgent and Google <span aria-hidden="true">·</span>')
lines=s2.split('\n')

# ---------------- FAQ ----------------
FAQ=[
("Who is the best real estate agent in Devonport?","Ben Potter has lived on the North Shore for 38 years and sells across Devonport with Harcourts Cooper &amp; Co, specialising in the suburb's heritage villas and tightly held streets. The right agent for a Devonport sale is the one who already knows the buyers waiting for your street, and on the peninsula that is Ben's whole business."),
("Which suburbs does Ben Potter sell in?","Devonport, Belmont and Bayswater are Ben's core suburbs. He also sells in Narrow Neck, Stanley Point, Hauraki and Takapuna, which together make up the Devonport peninsula and its neighbours on Auckland's North Shore."),
("How do I get a free property appraisal in Devonport, Belmont or Bayswater?","Use the form on this page or call Ben directly. Appraisals are free, come with no obligation, and are usually arranged within a few days. You'll receive a written estimate based on recent comparable sales on the peninsula, plus a recommended method of sale for your home."),
("What is my Devonport home worth in 2026?","In Devonport it depends on the street, the section and the condition of the home more than in almost any other Auckland suburb. Ben tracks every sale on the peninsula and gives you a realistic range from comparable Devonport sales in the last six months, not a headline figure to win the listing."),
("What are houses selling for in Belmont?","Belmont prices are driven by the Takapuna Grammar and Belmont Intermediate school zones, section size and how close a home sits to Lake Road and Ngataringa Bay. Renovated bungalows and new townhouses sit at different points of the market. Ben provides current Belmont comparable sales with every appraisal."),
("Is Bayswater a good place to buy a home?","Bayswater offers harbour views, the Bayswater Marina ferry into the city and a quieter pace than Devonport or Takapuna. Buyers choose it for townhouses and apartments on the ridge, weatherboard family homes on the flat and Bayswater School. Ben can tell you which Bayswater streets suit your budget and what is likely to come up next."),
("Who sells houses in Narrow Neck and Stanley Point?","Ben Potter sells across Narrow Neck and Stanley Point as part of the Devonport peninsula. Narrow Neck offers beachside bungalows and villas near Vauxhall Road; Stanley Point has some of the harbour edge's most sought-after homes. Both are tightly held, and many sales happen before a sign goes up."),
("Does Ben Potter sell in Takapuna and Hauraki?","Yes. Hauraki sits between Belmont and Takapuna and shares their school zones and family homes. Takapuna offers beachfront apartments, townhouses and larger family homes near Takapuna Beach and the town centre. Ben appraises and sells homes in both, alongside his core Devonport, Belmont and Bayswater suburbs."),
("Should I sell by auction, deadline sale or asking price?","Different methods suit different homes. Auction works well for tightly held Devonport villas with several buyers competing. A deadline sale often suits Belmont and Bayswater family homes. Ben recommends a method for your property as part of the appraisal, and explains why."),
("How long does it take to sell a house on the Devonport peninsula?","Most well priced homes in Devonport, Belmont and Bayswater sell within four to six weeks of going to market. Homes prepared properly before listing sell faster and for more, which is why Ben likes to talk to owners before the sign goes up."),
("What does it cost to sell a house with Harcourts Cooper &amp; Co?","Commission is agreed up front and only paid when your home sells. Marketing costs depend on the campaign you choose. Ben gives you a full written estimate before you sign anything, so there are no surprises."),
("How should I prepare a villa or bungalow for sale in Devonport?","Devonport buyers pay for character, so the priorities are usually presentation rather than renovation: paint, gardens, decluttering and staging. Ben walks through your home before the campaign and tells you what to fix and what to leave alone, so you spend where it returns."),
("Are there off-market homes for sale in Devonport, Belmont or Bayswater?","Often. Ben sells a good share of peninsula homes quietly to buyers already registered with him. If you're buying, register your brief with Ben so you hear about homes before they are advertised. If you're selling, an off-market introduction can be part of the plan."),
("Which schools and zones cover Devonport, Belmont and Bayswater?","The peninsula's schools include Devonport Primary, Vauxhall School, Stanley Bay School, Bayswater School, Belmont Primary, Hauraki School, Belmont Intermediate and Takapuna Grammar. Zoning varies street by street, so Ben confirms the zones for any specific address as part of an appraisal."),
]
faq_html='\n'.join(f'''          <details{" open" if i==0 else ""}>
            <summary>{q}</summary>
            <p>{a}</p>
          </details>''' for i,(q,a) in enumerate(FAQ))
block('<section class="section light grey" id="faq" aria-labelledby="faqTitle">','  </section>', f'''  <section class="section light grey" id="faq" aria-labelledby="faqTitle">
    <div class="wrap split">
      <div class="faq-side">
        <p class="label">Questions</p>
        <h2 id="faqTitle">Selling and buying on the <em>North Shore.</em></h2>
        <p class="muted" style="margin-top:1rem">Straight answers for Devonport, Belmont, Bayswater, Narrow Neck, Stanley Point, Hauraki and Takapuna.</p>
      </div>
      <div>
        <div class="faq-list">
{faq_html}
        </div>
      </div>
    </div>
  </section>''')

# ---------------- MODAL (before sticky) ----------------
s2='\n'.join(lines)
modal=f'''<dialog class="modal" id="guideModal" aria-labelledby="guideTitle">
  <button class="modal-close" type="button" id="guideClose" aria-label="Close">×</button>
  <div class="modal-body">
    <p class="label">Free download</p>
    <h3 id="guideTitle">The Peninsula Selling Guide</h3>
    <p class="muted">How to prepare, price and sell a home in Devonport, Belmont or Bayswater. Written by Ben from 38 years on the Shore.</p>
    <form id="guideForm" novalidate>
      <div class="field"><label for="g-name">Name</label><input id="g-name" name="name" type="text" autocomplete="name" required></div>
      <div class="field"><label for="g-email">Email</label><input id="g-email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="g-phone">Mobile</label><input id="g-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel"></div>
      <div class="form-foot"><button class="btn btn-ivory" type="submit">Send me the guide</button><small>Ben emails the PDF and follows up personally.</small></div>
    </form>
  </div>
</dialog>

<div class="sticky" aria-label="Quick action">'''
s2=s2.replace('<div class="sticky" aria-label="Quick action">',modal,1)
lines=s2.split('\n')

# ---------------- SCHEMA ----------------
def q(t): return t.replace('&amp;','&').replace('"','\\"')
faq_ld=',\n'.join(f'        {{ "@type": "Question", "name": "{q(a)}", "acceptedAnswer": {{ "@type": "Answer", "text": "{q(b)}" }} }}' for a,b in FAQ)
block('<script type="application/ld+json">','</script>', f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "RealEstateAgent",
      "name": "Ben Potter",
      "description": "Harcourts Cooper & Co real estate agent for Devonport, Belmont and Bayswater on Auckland's North Shore. Ben has lived on the peninsula for nearly forty years and also sells in Narrow Neck, Stanley Point, Hauraki and Takapuna.",
      "telephone": "+64210000000",
      "parentOrganization": {{ "@type": "Organization", "name": "Harcourts Cooper & Co" }},
      "address": {{ "@type": "PostalAddress", "addressLocality": "Devonport", "addressRegion": "Auckland", "addressCountry": "NZ" }},
      "areaServed": [
        {{ "@type": "Place", "name": "Devonport, Auckland", "geo": {{ "@type": "GeoCoordinates", "latitude": -36.8290, "longitude": 174.7961 }} }},
        {{ "@type": "Place", "name": "Belmont, Auckland", "geo": {{ "@type": "GeoCoordinates", "latitude": -36.8060, "longitude": 174.7898 }} }},
        {{ "@type": "Place", "name": "Bayswater, Auckland", "geo": {{ "@type": "GeoCoordinates", "latitude": -36.8163, "longitude": 174.7727 }} }},
        {{ "@type": "Place", "name": "Narrow Neck, Auckland" }},
        {{ "@type": "Place", "name": "Stanley Point, Auckland" }},
        {{ "@type": "Place", "name": "Hauraki, Auckland" }},
        {{ "@type": "Place", "name": "Takapuna, Auckland" }}
      ],
      "knowsAbout": ["Devonport real estate", "Belmont real estate", "Bayswater real estate", "Property appraisals", "Auctions", "Heritage villas"]
    }},
    {{
      "@type": "FAQPage",
      "mainEntity": [
{faq_ld}
      ]
    }}
  ]
}}
</script>''')

# ---------------- JS ----------------
block('<script>','</script>', r'''<script>
  (function(){
    // Page config: fill these in when Ben supplies them
    var CONFIG = {
      formEndpoint: '',                                   // e.g. a Formspree URL; leads POST here as JSON and Ben is emailed
      guideUrl: 'guide/ben-potter-selling-guide.pdf',     // the selling guide PDF
      reelEmbed: ''                                       // e.g. https://www.youtube.com/embed/VIDEO_ID
    };

    var header = document.querySelector('.header');
    var menuBtn = document.getElementById('menuBtn');
    menuBtn.addEventListener('click', function(){
      var open = header.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.querySelectorAll('.mobile-nav a').forEach(function(a){
      a.addEventListener('click', function(){ header.classList.remove('open'); menuBtn.setAttribute('aria-expanded','false'); });
    });

    // Reel: embed when a link is configured, otherwise explain the slot
    var reelBtn = document.getElementById('reelBtn'), reelMsg = document.getElementById('reelMsg');
    reelBtn.addEventListener('click', function(){
      if(CONFIG.reelEmbed){
        var f = document.createElement('iframe');
        f.src = CONFIG.reelEmbed + (CONFIG.reelEmbed.indexOf('?') > -1 ? '&' : '?') + 'autoplay=1';
        f.allow = 'autoplay; fullscreen'; f.title = 'Ben Potter reel';
        f.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;border:0';
        reelBtn.innerHTML = ''; reelBtn.appendChild(f);
      } else { reelMsg.hidden = !reelMsg.hidden; }
    });

    var quotes = [
      { t: "Ben knew exactly who would buy our villa before we'd even signed with him. Sold in ten days, above what two other agents told us to expect.", n: "Sarah and James", w: "Sold in Devonport" },
      { t: "Straight talking, no pressure, and he did everything he said he would. We've used Ben twice now and would use him again without a second thought.", n: "Mark T.", w: "Sold in Belmont" },
      { t: "Ben's advice on what to fix and what to leave alone saved us thousands. The campaign was quiet and classy, and the result was better than we hoped.", n: "The Nguyen family", w: "Sold in Bayswater" }
    ];
    var qi = 0;
    var qText = document.getElementById('quoteText'), qName = document.getElementById('quoteName'), qWhere = document.getElementById('quoteWhere'), qCount = document.getElementById('qCount');
    function showQuote(i){
      qi = (i + quotes.length) % quotes.length;
      qText.textContent = quotes[qi].t; qName.textContent = quotes[qi].n; qWhere.textContent = quotes[qi].w;
      qCount.textContent = (qi + 1) + ' / ' + quotes.length;
    }
    document.getElementById('qPrev').addEventListener('click', function(){ showQuote(qi - 1); });
    document.getElementById('qNext').addEventListener('click', function(){ showQuote(qi + 1); });

    // Leads: both forms go through here. With no endpoint configured the site just shows the thank-you.
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
        el.style.borderColor = bad ? '#A3ABB5' : '';
        if(bad){ ok = false; el.setAttribute('aria-invalid','true'); } else { el.removeAttribute('aria-invalid'); }
      });
      if(!ok) form.querySelector('[aria-invalid]').focus();
      return ok;
    }
    var clean = function(s){ return s.replace(/[<>&]/g, ''); };

    var form = document.getElementById('appraisal');
    form.addEventListener('submit', function(e){
      e.preventDefault();
      if(!validate(form)) return;
      var name = form.querySelector('[name="name"]').value.trim().split(' ')[0] || 'there';
      sendLead('appraisal', form);
      form.innerHTML = '<div class="form-done"><p class="label">Received</p><h3>Thank you, ' + clean(name) + '.</h3><p>Ben will call you within one business day to arrange a time. If it’s urgent, ring him on <a href="tel:+64210000000">021 000 0000</a>.</p></div>';
      form.querySelector('h3').setAttribute('tabindex','-1'); form.querySelector('h3').focus();
    });

    // Selling guide: details in exchange for the PDF
    var modal = document.getElementById('guideModal');
    document.getElementById('guideBtn').addEventListener('click', function(){ modal.showModal(); });
    document.getElementById('guideClose').addEventListener('click', function(){ modal.close(); });
    modal.addEventListener('click', function(e){ if(e.target === modal) modal.close(); });
    var gform = document.getElementById('guideForm');
    gform.addEventListener('submit', function(e){
      e.preventDefault();
      if(!validate(gform)) return;
      var name = gform.querySelector('[name="name"]').value.trim().split(' ')[0] || 'there';
      sendLead('guide', gform);
      gform.innerHTML = '<div class="form-done"><p class="label">On its way</p><h3>Thanks, ' + clean(name) + '.</h3><p>Check your inbox for the guide. You can also open it now.</p><p><a class="btn btn-ivory" href="' + CONFIG.guideUrl + '" download>Download the guide</a></p></div>';
      gform.querySelector('h3').setAttribute('tabindex','-1'); gform.querySelector('h3').focus();
    });
  })();
</script>''')

s='\n'.join(lines)

# ---------------- CSS additions ----------------
css='''
  /* Hero: suburbs as the headline, coordinates beside each */
  .hero{background:radial-gradient(85% 90% at 72% 45%, #2B2D32 0%, #17181B 50%, #0E0F11 100%)}
  .hero-glow{background:radial-gradient(55% 70% at 72% 60%, rgba(255,255,255,.13), transparent 70%)}
  .suburb-title{display:flex; flex-direction:column; gap:.04em; font-size:clamp(2.7rem, 5.6vw, 5.2rem); max-width:none}
  .suburb-line{display:flex; align-items:baseline; gap:22px; flex-wrap:wrap}
  .suburb-line small{font-family:var(--sans); font-weight:500; font-size:.6rem; letter-spacing:.16em; text-transform:uppercase; color:var(--accent); font-variant-numeric:tabular-nums; white-space:nowrap}
  .hero-copy .sub{max-width:50ch}
  .btn svg{width:15px; height:15px}

  /* Suburb rows: body plus search-term tags */
  .row-body{display:flex; flex-direction:column; gap:14px}
  .tags{list-style:none; margin:0; padding:0; display:flex; flex-wrap:wrap; gap:6px 6px}
  .tags li{font-size:.62rem; letter-spacing:.1em; text-transform:uppercase; font-weight:500; color:var(--fg-2); border:1px solid var(--rule); border-radius:2px; padding:5px 9px; white-space:nowrap}
  .row{align-items:start}
  .row h3{padding-top:.2em}

  /* Results: even card grid, identical for sold and for sale */
  .results-head{display:flex; justify-content:space-between; align-items:flex-end; gap:32px; flex-wrap:wrap; margin-bottom:2.2rem}
  .results-head > div{display:flex; flex-direction:column; gap:14px}
  .results-head p.muted{max-width:44ch}
  .results-head.second{margin-top:clamp(56px, 7vw, 88px)}
  .cards{display:grid; grid-template-columns:repeat(3, minmax(0,1fr)); gap:24px}
  .card{display:flex; flex-direction:column; text-decoration:none; color:inherit; background:var(--bg); border:1px solid var(--rule); border-radius:2px; overflow:hidden; transition:border-color .2s, transform .3s}
  .card:hover{border-color:var(--fg); transform:translateY(-2px)}
  .card-media{aspect-ratio:4/3; background:var(--panel); display:grid; place-items:center; align-content:center; gap:8px; color:var(--mute)}
  .card-media svg{width:44px; height:44px; opacity:.6}
  .card-media span{font-size:.58rem; letter-spacing:.2em; text-transform:uppercase; font-weight:500; opacity:.7}
  .card-body{padding:22px 22px 24px; display:flex; flex-direction:column; gap:8px; flex:1}
  .card-body h3{font-size:1.35rem}
  .card-meta{font-size:.86rem; color:var(--mute)}
  .card-date{margin-top:auto; padding-top:12px; font-size:.62rem; letter-spacing:.16em; text-transform:uppercase; font-weight:600; color:var(--fg-2)}
  .card-date.live{color:var(--accent)}
  .card-cta{background:var(--ground); color:var(--ivory); border-color:var(--ground); --fg-2:var(--ivory-2); --mute:var(--muted); --accent:#A3ABB5}
  .card-cta .card-body{padding:32px 26px; justify-content:center}
  .card-cta h3{font-size:1.5rem}
  .card-cta .card-date{color:var(--ivory)}

  /* Selling guide modal */
  .modal{border:0; padding:0; background:var(--surface); color:var(--ivory); width:min(92vw, 520px); border-radius:2px; --bg:var(--surface); --fg:var(--ivory); --fg-2:var(--ivory-2); --mute:var(--muted); --rule:var(--line); --rule-strong:var(--line-strong); --accent:#A3ABB5}
  .modal::backdrop{background:rgba(0,0,0,.7); backdrop-filter:blur(6px)}
  .modal-body{padding:40px 40px 44px; display:flex; flex-direction:column; gap:16px}
  .modal-body h3{font-size:2rem}
  .modal-body form{margin-top:10px; gap:22px}
  .modal-close{position:absolute; top:14px; right:14px; width:40px; height:40px; background:none; border:1px solid var(--line-strong); border-radius:50%; color:var(--ivory); font-size:1.4rem; line-height:1; cursor:pointer}
  .modal-close:hover{border-color:var(--ivory)}
  .modal .form-done a.btn{display:inline-flex}

  @media (max-width: 1000px){ .cards{grid-template-columns:repeat(2, minmax(0,1fr))} .row{grid-template-columns:minmax(0,1fr) auto} .row-body{grid-column:1 / -1} }
  @media (max-width: 640px){ .cards{grid-template-columns:minmax(0,1fr)} .suburb-line{gap:12px} .modal-body{padding:32px 24px} .hero-actions .btn{width:100%} }
'''
s=s.replace('\n</style>', css+'</style>',1)
# old row media rule no longer applies to p
s=s.replace('.row p{grid-column:1 / -1}','')
s=s.replace('<meta name="description" content="Ben Potter. Nearly forty years living on the Devonport peninsula. Harcourts Cooper & Co agent for Devonport, Belmont and Bayswater. Book a free appraisal.">',
            '<meta name="description" content="Ben Potter, Harcourts Cooper & Co. Real estate agent for Devonport, Belmont and Bayswater, plus Narrow Neck, Stanley Point, Hauraki and Takapuna. Nearly forty years on the North Shore. Free property appraisals.">')
open(p,'w',encoding='utf-8').write(s)
print('done', len(s))
