# -*- coding: utf-8 -*-
"""Loads data/market-updates.json for the build.

One entry per monthly edition. Adding a month means adding an entry and dropping that
month's PDF into reports/, which is the whole publishing job: no page is rebuilt, no
template is copied, and every earlier month stays exactly where it was.

The trend chart is drawn here as inline SVG rather than pasted in as a picture. It stays
sharp at any size, costs no extra request, carries the site's own colours instead of the
report's, and the figures sit in the markup where a search engine can read them.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, '..', 'data', 'market-updates.json')


def load():
    with open(PATH, encoding='utf-8') as f:
        data = json.load(f)
    eds = data.get('editions', [])
    for e in eds:
        for key in ('slug', 'period', 'published', 'h1'):
            if not e.get(key):
                raise SystemExit('market update missing %s: %r' % (key, e.get('slug')))
        e['path'] = 'market-updates/%s/' % e['slug']
    eds.sort(key=lambda e: e.get('published') or '', reverse=True)
    return eds


def money(n):
    return '$' + format(int(n), ',d')


def delta(now, before):
    """Returns (text, direction) with direction used only to pick a colour."""
    if not before:
        return ('', 'flat')
    pct = (now - before) / float(before) * 100.0
    if abs(pct) < 0.05:
        return ('level', 'flat')
    return ('%.1f%% %s' % (abs(pct), 'up' if pct > 0 else 'down'),
            'up' if pct > 0 else 'down')


def trend_svg(points, width=1000, height=320):
    """A line chart as a path, with a soft fill under it. No library, no request."""
    if len(points) < 2:
        return ''
    vals = [p['value'] for p in points]
    lo, hi = min(vals), max(vals)
    pad = (hi - lo) * 0.18 or 1
    lo, hi = lo - pad, hi + pad
    left, right, top, bottom = 58, 14, 18, 34
    w = width - left - right
    h = height - top - bottom

    def xy(i, v):
        x = left + (w * i / float(len(points) - 1))
        y = top + h - (h * (v - lo) / float(hi - lo))
        return x, y

    pts = [xy(i, v) for i, v in enumerate(vals)]
    line = 'M ' + ' L '.join('%.1f %.1f' % p for p in pts)
    area = line + ' L %.1f %.1f L %.1f %.1f Z' % (pts[-1][0], top + h, pts[0][0], top + h)

    # Four gridlines, labelled in round millions.
    grid = []
    steps = 4
    for s in range(steps + 1):
        v = lo + (hi - lo) * s / float(steps)
        y = top + h - (h * s / float(steps))
        grid.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" class="mu-grid"/>'
                    % (left, y, width - right, y))
        grid.append('<text x="%d" y="%.1f" class="mu-ylab">$%.2fm</text>'
                    % (left - 10, y + 4, v / 1000000.0))

    # Year ticks only, or the axis turns to mush.
    ticks = []
    for i, p in enumerate(points):
        if not (p['label'].startswith('Jan') or i == len(points) - 1):
            continue
        x, _ = xy(i, vals[i])
        # The first tick would sit on top of the y axis labels, so it is dropped.
        if x < left + 26:
            continue
        ticks.append('<text x="%.1f" y="%d" class="mu-xlab">%s</text>'
                     % (x, height - 12, p['label'].split()[-1].join(["'", ""])))

    last_x, last_y = pts[-1]
    return '''<svg class="mu-chart" viewBox="0 0 %d %d" role="img"
     aria-label="Twelve month moving average sale price, %s to %s, from %s to %s">
  <defs><linearGradient id="muFill" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%%" class="mu-stop-a"/><stop offset="100%%" class="mu-stop-b"/>
  </linearGradient></defs>
  %s
  <path d="%s" fill="url(#muFill)"/>
  <path d="%s" class="mu-line" fill="none"/>
  <circle cx="%.1f" cy="%.1f" r="4.5" class="mu-dot"/>
  %s
</svg>''' % (width, height, points[0]['label'], points[-1]['label'],
              money(vals[0]), money(vals[-1]),
              '\n  '.join(grid), area, line, last_x, last_y, '\n  '.join(ticks))
