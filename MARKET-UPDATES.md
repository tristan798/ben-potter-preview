# Publishing a monthly Market Update

Two things change each month. Nothing else.

1. Drop the month's PDF into `reports/`, named like
   `peninsula-sales-statistics-october-2026.pdf`.
2. Add an entry to the top of `editions` in `data/market-updates.json`.
3. `python3 build.py`

That is the whole job. The page, its URL, the archive entry, the sitemap entry, the
Article schema, the canonical and the Open Graph tags are all generated from that entry.
Every earlier month stays exactly where it was, at the same URL.

## The fields

| Field | What it does |
| --- | --- |
| `slug` | The URL. `october-2026` becomes `/market-updates/october-2026/`. |
| `period` | Shown on the card and in the breadcrumb, e.g. `October 2026`. |
| `published` | Sorts the archive and fills `datePublished` in the schema. |
| `updated` | `dateModified`. Leave it equal to `published` unless the page is revised. |
| `h1` | The page heading. `<em>` around the last few words gives the two-tone treatment. |
| `lede` | The line under the heading, and the card summary. |
| `seo_title` | The browser title and search result title. |
| `meta` | The meta description. |
| `eyebrow` | The small blue line above the heading. |
| `pdf` | Path to that month's report, relative to the repo root. |
| `glance` | Pairs of `[value, label]`. The first three also appear on the archive card. |
| `trend` | `{label, value}` points for the chart. Labels like `Sep 26`. |
| `trend_caption` | The line under the chart. |
| `commentary` | One string per paragraph. |
| `suburbs` | Per suburb: `name`, `sales`, `prior_sales`, `avg`, `prior_avg`, `note`, and `link` to that suburb page where one exists. |
| `cta_title`, `cta_body` | The closing call to action. |
| `source` | The small print under the figures. |

Percentages are worked out from the raw numbers rather than typed in, so they cannot
drift from the figures beside them.

## The chart

Drawn as inline SVG from the `trend` numbers, in the site's own colours. There is no
image to export and nothing to re-cut when the design changes. Give it the 12 month
moving average column from the report, one point per month.
