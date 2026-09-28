# -*- coding: utf-8 -*-
"""Loads data/listings.json for the build, with light validation.

Every field except address and suburb is optional, so a listing can go live with only
what is actually known. Nothing here invents data it was not given.
"""
import json, os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, '..', 'data', 'listings.json')
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def _fmt(iso):
    if not iso:
        return ''
    try:
        y, m, d = (int(x) for x in iso.split('-'))
        return '%d %s %d' % (d, MONTHS[m - 1], y)
    except Exception:
        return iso


def load():
    with open(PATH, encoding='utf-8') as f:
        data = json.load(f)
    for bucket in ('for_sale', 'sold'):
        for item in data.get(bucket, []):
            if not item.get('address') or not item.get('suburb'):
                raise SystemExit('listing missing address or suburb: %r' % item)
            item.setdefault('id', '')
            item['sold_label'] = 'Sold ' + _fmt(item.get('sold_on')) if item.get('sold_on') else 'Sold'
    data['sold'].sort(key=lambda i: i.get('sold_on') or '', reverse=True)
    return data


def meta_line(item):
    """Only render the specs we actually have."""
    bits = []
    for key, suffix in (('bedrooms', ' bed'), ('bathrooms', ' bath'), ('parking', ' car')):
        if item.get(key):
            bits.append('%s%s' % (item[key], suffix))
    if item.get('land_m2'):
        bits.append('%s m²' % item['land_m2'])
    return ' · '.join(bits)
