# ben-potter.com

Static site for Ben Potter, Harcourts Cooper & Co. No build dependencies beyond Python 3.

```
python3 build.py        # regenerates every page, sitemap.xml, robots.txt and deploy/ configs
```

## Layout

| Path | Purpose |
| --- | --- |
| `tools/content.py` | All copy, listings, FAQs and configuration. Edit here first. |
| `src/site.css` | The stylesheet. Copied to `assets/site.css` on build. |
| `build.py` | Generator: pages, schema graph, sitemap, robots, redirect configs. |
| `assets/fonts/` | Self-hosted Clash Display and Poppins (no third-party font requests). |
| `dist/page.html` | Single-file homepage fragment for the Claude artifact preview. |
| `deploy/` | Redirect configs for Netlify (`_redirects`), Vercel (`vercel.json`) and Apache (`.htaccess`). |

## Pages

`/` · `/devonport-real-estate/` · `/belmont-real-estate/` · `/bayswater-real-estate/` ·
`/recently-sold/` · `/free-selling-guide/` · `/property-appraisal/`

## Launch checklist

Everything below lives in `tools/content.py` unless noted.

1. `PREVIEW = False` — removes `noindex` from every page and switches `robots.txt` from
   disallow-all to allow-all with the sitemap reference.
2. `SITE` — confirm the production origin. Canonicals, Open Graph URLs and the sitemap all derive
   from it.
3. `STREET` — the Devonport office street address. Currently empty, so `streetAddress` is omitted
   from the schema. Local SEO wants it filled.
4. `EMAIL` — currently an assumed `firstname.lastname@harcourts.co.nz` format. Confirm with Ben.
5. `GA4_ID` — add the measurement ID and the gtag snippet appears on every page. Empty means no
   tag is emitted at all.
6. `GSC_TOKEN` — only needed if Search Console verification uses the HTML tag method. DNS or the
   Google Analytics method needs nothing here.
7. Copy the right file from `deploy/` to the host so `/listings` from the old Webflow site
   301s to `/recently-sold/`. GitHub Pages cannot do server redirects; Netlify, Vercel, Cloudflare
   and Apache all can.
8. Submit `sitemap.xml` in Search Console and request indexing on the three suburb pages.
9. `FORM_KEY` — **required for leads to reach Ben.** Go to https://web3forms.com, enter
   `ben.potter@harcourts.co.nz`, confirm the verification email, paste the access key here and
   rebuild. Every appraisal and selling-guide submission is then emailed to that address with the
   sender set as reply-to. Until the key is set, the form shows its thank-you state but sends
   nothing, and logs a console warning.
10. `REEL_EMBED` — paste the YouTube or Vimeo **embed** URL for Ben's Devonport / Belmont /
    Bayswater reel (e.g. `https://www.youtube.com/embed/VIDEO_ID`). The About section tile then
    plays it inline instead of showing the placeholder.
11. Drop the selling guide PDF at `guide/ben-potter-selling-guide.pdf`, or change `CONFIG.guideUrl`
    in `build.py`, `script_block()`.

## Still needed from Ben

Photography (peninsula, streetscapes, listing photos, the beach shot for the hero), the reel link,
the selling guide PDF, real sold listings, CRM API details, and his RateMyAgent feed.

Listing card photos drop into `img/listings/` using the filenames already commented into the card
markup, e.g. `img/listings/old-lake-road-devonport.jpg`.
