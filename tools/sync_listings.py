# -*- coding: utf-8 -*-
"""Pulls Ben's listings from an external source into data/listings.json.

Run: python3 tools/sync_listings.py [--dry-run]

Exit code 0 = no change, 10 = listings changed (CI rebuilds and commits on 10).

Sources, in order of how well they actually work:

  harcourts Ben's own Harcourts profile page, which lists his listings under a path
            scoped to him and tags each card data-status="current" or "sold". This
            is the agent filter Trade Me does not have. Each listing's detail page
            carries labelled specs (li.bed, li.bath, land and floor area), so the
            numbers are read from labels rather than guessed from icon order.
            Photos are copied into img/listings/ so the site never hotlinks their
            CDN. No key, no approval, no agency paperwork. This is the default.

  feed      An XML or JSON feed of Ben's listings. Sturdier than parsing HTML if the
            agency will hand over the URL, because it cannot be broken by a redesign. Every
            agency already generates one to push listings to Trade Me, OneRoof and
            realestate.co.nz, so ask Harcourts Cooper & Co or the CRM provider for
            the URL. Set LISTINGS_FEED_URL.

  trademe   The official Trade Me API. Works, but see the caveat below: it cannot
            filter by individual agent, only by the member account that owns the
            listing, which for an agency is the whole office. Needs OAuth keys.

  manual    Whatever is already in data/listings.json. The default.

Trade Me caveat, confirmed against their API reference: the residential search
endpoint exposes adjacent_suburbs, bathrooms, bedrooms, price, property_type,
region, district, suburb, sales_method, search_string and member_listing, and
nothing for agent, agent id or office. member_listing filters to a seller, so on an
agency account it returns every Harcourts Cooper & Co listing, not only Ben's. The
agent name would have to be matched from each listing's detail, which is brittle.
Authentication is required on that endpoint and commercial use needs their approval.
"""
import json, os, sys, hashlib, re
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, '..', 'data', 'listings.json')

SOURCE      = os.environ.get('LISTINGS_SOURCE', 'harcourts')
FEED_URL    = os.environ.get('LISTINGS_FEED_URL', '')
AGENT_NAME  = os.environ.get('LISTINGS_AGENT', 'Ben Potter')
PROFILE_URL = os.environ.get('LISTINGS_PROFILE_URL',
                             'https://harcourts.net/nz/office/devonport/people/ben-potter')
IMG_DIR     = os.path.join(HERE, '..', 'img', 'listings')
PHOTO_W     = 1600
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/140.0 Safari/537.36')


def slugify(*parts):
    return re.sub(r'[^a-z0-9]+', '-', ' '.join(parts).lower()).strip('-')


def tidy_address(addr):
    """Harcourts writes "Lot 8/3 Corrella Road" for what Ben calls "8/3 Corrella Road".
    Drop the Lot prefix so the two do not become two listings."""
    return re.sub(r'^lot\s+(?=\d+\s*/)', '', addr.strip(), flags=re.I)


def normalise(raw):
    """Map one source record onto the shape build.py renders. Unknown fields stay absent."""
    out = {
        'address': tidy_address(raw.get('address') or ''),
        'suburb': (raw.get('suburb') or '').strip(),
    }
    if not out['address'] or not out['suburb']:
        return None
    out['id'] = slugify(out['address'], out['suburb'])
    for key in ('bedrooms', 'bathrooms', 'parking', 'land_m2', 'url', 'photo',
                'photo_w', 'photo_h', 'result', 'status_label', 'sold_on'):
        if raw.get(key):
            out[key] = raw[key]
    return out


def from_feed(url):
    """Accepts either JSON or a simple XML feed of <listing> elements."""
    import urllib.request
    with urllib.request.urlopen(url, timeout=30) as r:
        body = r.read().decode('utf-8', 'replace')
    if body.lstrip().startswith('{') or body.lstrip().startswith('['):
        data = json.loads(body)
        records = data.get('listings', data) if isinstance(data, dict) else data
    else:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(body)
        records = []
        for node in root.iter():
            if node.tag.lower().endswith('listing'):
                records.append({c.tag.lower(): (c.text or '').strip() for c in node})
    live, sold = [], []
    for rec in records:
        agent = str(rec.get('agent') or rec.get('agent_name') or '')
        if AGENT_NAME and agent and AGENT_NAME.lower() not in agent.lower():
            continue                                   # other agents in the same office
        item = normalise(rec)
        if not item:
            continue
        status = str(rec.get('status') or '').lower()
        (sold if 'sold' in status else live).append(item)
    return live, sold


def fetch(url):
    """A plain GET with a browser user agent. Their edge returns 403 without one."""
    import urllib.request
    req = urllib.request.Request(url, headers={'User-Agent': UA,
                                               'Accept-Language': 'en-NZ,en;q=0.9'})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode('utf-8', 'replace')


def strip_tags(chunk):
    import html as H
    return H.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', chunk))).strip()


def profile_listings(doc):
    """Every listing card on Ben's profile, with the status and price the page states.

    The price is read here rather than from the listing page, because the card puts it
    in one span while the listing page spreads it over an auction/negotiation block."""
    found = {}
    for block in re.split(r'(?=<div class="property-item card)', doc):
        m = re.search(r'href="(/nz/[^"]*?/listing/[^"#?]+)"[^>]*data-category="[^"]*"'
                      r'[^>]*data-status="([^"]*)"', block)
        if not m:
            continue
        url = 'https://harcourts.net' + m.group(1)
        if url in found:
            continue
        price = re.search(r'<span class="price[^"]*">(.*?)</span>', block, re.S)
        found[url] = {'status': m.group(2).strip().lower(),
                      'price': strip_tags(price.group(1)) if price else ''}
    return found


def detail_record(doc, url, status, price=''):
    """Read one listing page. Specs come from labelled classes, never icon order."""
    body = re.sub(r'<script.*?</script>', '', doc, flags=re.S)

    addr = re.search(r'<span class="address">(.*?)</span>', body, re.S)
    if not addr:
        addr = re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S)
    if not addr:
        return None
    parts = [p.strip() for p in strip_tags(addr.group(1)).split(',') if p.strip()]
    if not parts:
        return None
    rec = {'address': parts[0], 'suburb': parts[1] if len(parts) > 1 else '', 'url': url}

    def labelled(cls):
        m = re.search(r'<li class="%s"><span>(\d+)</span>' % cls, body)
        return int(m.group(1)) if m else None

    for key, cls in (('bedrooms', 'bed'), ('bathrooms', 'bath')):
        v = labelled(cls)
        if v:
            rec[key] = v
    park = 0
    # Deliberately not openspaces: those are uncovered spots, and adding them turns a
    # two-car garage into "6 car". Their own card counts covered parking only.
    for cls in ('garage', 'carport', 'carpad'):
        m = re.search(r'<li class="%s"><span>(\d+)</span>' % cls, body)
        if m:
            park += int(m.group(1))
    if park:
        rec['parking'] = park
    # icon-square-meters is the land area; icon-floorarea beside it is the house.
    land = re.search(r'<span>([\d,]+)\s*<i class="mini-icn icon-square-meters"', body)
    if land:
        rec['land_m2'] = int(land.group(1).replace(',', ''))

    # "(USP)" is Unless Sold Prior, trade shorthand that means nothing to a seller.
    label = re.sub(r'\s*\((?:USP|BEO|PBN)\)\s*$', '', price.strip(), flags=re.I)
    if status == 'sold':
        # No status_label: build.py derives "Sold 17 Sep 2026" from sold_on when a date
        # is known, and falls back to plain "Sold" when it is not. Their card has no date.
        pass
    else:
        rec['status_label'] = label or 'For sale'

    photo = re.search(r'(https://listings-photos[^"\' ]+?\.jpe?g)/\d+x\d+', doc)
    if photo:
        rec['_photo_src'] = photo.group(1)
    return rec


def grab_photo(rec, slug, dry=False):
    """Copy the hero shot into the repo at PHOTO_W wide. We do not hotlink their CDN."""
    import urllib.request
    src = rec.pop('_photo_src', None)
    if not src:
        return
    dest_rel = 'img/listings/%s.jpg' % slug
    dest = os.path.join(HERE, '..', dest_rel)
    stamp = os.path.join(IMG_DIR, '.%s.src' % slug)
    # A photo with no stamp beside it was put there by hand. Ben's own photography
    # beats a portal thumbnail, so leave it alone and just point at it.
    if os.path.exists(dest) and not os.path.exists(stamp):
        rec['photo'] = dest_rel
        return
    # Skip the download when this exact photo is already sitting on disk.
    if os.path.exists(dest) and os.path.exists(stamp):
        if open(stamp, encoding='utf-8').read().strip() == src:
            rec['photo'] = dest_rel
            return
    if dry:
        print('   would fetch photo for %s' % slug)
        rec['photo'] = dest_rel if os.path.exists(dest) else None
        if not rec['photo']:
            rec.pop('photo')
        return
    os.makedirs(IMG_DIR, exist_ok=True)
    req = urllib.request.Request('%s/%dx%d' % (src, PHOTO_W, int(PHOTO_W * 2 / 3)),
                                 headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            blob = r.read()
    except Exception as e:                       # a missing photo must not fail the sync
        print('   ! photo failed for %s: %s' % (slug, e))
        return
    if len(blob) < 5000 or not blob.startswith(b'\xff\xd8'):
        print('   ! photo for %s was not a usable JPEG, skipped' % slug)
        return
    open(dest, 'wb').write(blob)
    open(stamp, 'w', encoding='utf-8').write(src + '\n')
    rec['photo'] = dest_rel
    print('   photo %s (%d KB)' % (dest_rel, len(blob) // 1024))


def from_harcourts(dry=False):
    import time
    print('Reading %s' % PROFILE_URL)
    cards = profile_listings(fetch(PROFILE_URL))
    if not cards:
        raise SystemExit(
            'No listing cards found on the profile page. Their markup has probably\n'
            'changed. Check the page by hand before trusting this sync again.')
    print('   %d listings on the profile' % len(cards))

    live, sold = [], []
    for url, card in sorted(cards.items()):
        status = card['status']
        try:
            rec = detail_record(fetch(url), url, status, card.get('price', ''))
        except Exception as e:
            print('   ! %s: %s' % (url.rsplit('/', 1)[1], e))
            continue
        if not rec:
            continue
        item = normalise(rec)
        if not item:
            print('   ! skipped, no address/suburb: %s' % url)
            continue
        grab_photo(rec, item['id'], dry=dry)
        for k in ('photo',):
            if rec.get(k):
                item[k] = rec[k]
        print('   %-8s %s, %s' % (status, item['address'], item['suburb']))
        (sold if status == 'sold' else live).append(item)
        time.sleep(1.0)                          # be a polite visitor
    return live, sold


def from_trademe():
    raise SystemExit(
        'The Trade Me API cannot filter by individual agent, only by the member account\n'
        'that owns the listing, which on an agency account is the whole office.\n'
        'Use LISTINGS_SOURCE=feed with the agency or CRM feed instead. See the module\n'
        'docstring for the detail.')


def main():
    dry = '--dry-run' in sys.argv
    current = json.load(open(PATH, encoding='utf-8'))

    if SOURCE == 'manual':
        print('LISTINGS_SOURCE=manual, nothing to pull.')
        return 0
    elif SOURCE == 'harcourts':
        live, sold = from_harcourts(dry=dry)
    elif SOURCE == 'trademe':
        from_trademe()
        return 0
    elif SOURCE == 'feed':
        if not FEED_URL:
            raise SystemExit('LISTINGS_FEED_URL is not set.')
        live, sold = from_feed(FEED_URL)
    else:
        raise SystemExit('Unknown LISTINGS_SOURCE: %s' % SOURCE)

    # Anything hand-curated outranks the scrape. Their sold cards carry no date, and
    # Ben's own photography is better than the portal thumbnail, so those stay put.
    KEEP = ('sold_on', 'photo', 'photo_w', 'photo_h', 'result')
    previous = {i.get('id'): i for i in current.get('sold', [])}
    for item in sold:
        old = previous.pop(item.get('id'), None)
        if old:
            for k in KEEP:
                if old.get(k):
                    item[k] = old[k]
    # Sales the profile page no longer shows are still Ben's history. Keep them.
    sold.extend(previous.values())
    sold.sort(key=lambda i: i.get('sold_on') or '', reverse=True)

    live_prev = {i.get('id'): i for i in current.get('for_sale', [])}
    for item in live:
        old = live_prev.get(item.get('id'))
        if old:
            for k in ('photo', 'photo_w', 'photo_h'):
                if old.get(k) and not item.get(k):
                    item[k] = old[k]

    fresh = dict(current, updated=date.today().isoformat(), source=SOURCE,
                 for_sale=live, sold=sold)

    def fingerprint(d):
        return hashlib.sha256(json.dumps(
            {'for_sale': d.get('for_sale'), 'sold': d.get('sold')},
            sort_keys=True, default=str).encode()).hexdigest()

    if fingerprint(fresh) == fingerprint(current):
        print('No change: %d for sale, %d sold.' % (len(live), len(sold)))
        return 0

    print('Changed: %d for sale, %d sold.' % (len(live), len(sold)))
    if dry:
        print('(dry run, nothing written)')
        return 10
    json.dump(fresh, open(PATH, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    open(PATH, 'a', encoding='utf-8').write('\n')
    return 10


sys.exit(main())
