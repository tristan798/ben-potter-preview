# -*- coding: utf-8 -*-
"""Pulls Ben's listings from an external source into data/listings.json.

Run: python3 tools/sync_listings.py [--dry-run]

Exit code 0 = no change, 10 = listings changed (CI rebuilds and commits on 10).

Sources, in order of how well they actually work:

  feed      An XML or JSON feed of Ben's listings. This is the right answer. Every
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

SOURCE     = os.environ.get('LISTINGS_SOURCE', 'manual')
FEED_URL   = os.environ.get('LISTINGS_FEED_URL', '')
AGENT_NAME = os.environ.get('LISTINGS_AGENT', 'Ben Potter')


def slugify(*parts):
    return re.sub(r'[^a-z0-9]+', '-', ' '.join(parts).lower()).strip('-')


def normalise(raw):
    """Map one source record onto the shape build.py renders. Unknown fields stay absent."""
    out = {
        'address': (raw.get('address') or '').strip(),
        'suburb': (raw.get('suburb') or '').strip(),
    }
    if not out['address'] or not out['suburb']:
        return None
    out['id'] = slugify(out['address'], out['suburb'])
    for key in ('bedrooms', 'bathrooms', 'parking', 'land_m2', 'url', 'photo',
                'result', 'status_label', 'sold_on'):
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
    if SOURCE == 'trademe':
        from_trademe()
    if SOURCE == 'feed':
        if not FEED_URL:
            raise SystemExit('LISTINGS_FEED_URL is not set.')
        live, sold = from_feed(FEED_URL)
    else:
        raise SystemExit('Unknown LISTINGS_SOURCE: %s' % SOURCE)

    # Keep any hand-entered sale that the feed has dropped, so history is never lost.
    known = {i['id'] for i in sold}
    for old in current.get('sold', []):
        if old.get('id') not in known:
            sold.append(old)
    sold.sort(key=lambda i: i.get('sold_on') or '', reverse=True)

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
