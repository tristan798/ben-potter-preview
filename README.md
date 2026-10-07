# benpotter.co.nz

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
| `tools/sync_listings.py` | Pulls Ben's listings from his Harcourts pages. Runs hourly in CI. |
| `tools/images.py` | Sizes listing photos to 1000px and 500px, JPEG and WebP, for the card srcset. |
| `tools/emails.py` | Builds the branded HTML emails into `email/`. |
| `api/lead.js` | Sends the notification and the confirmation. Needs a host that runs functions. |

## Pages

`/` · `/devonport-real-estate/` · `/belmont-real-estate/` · `/bayswater-real-estate/` ·
`/recently-sold/` · `/current-listings/` · `/free-selling-guide/` · `/property-appraisal/` ·
`/contact/` · `/whats-my-home-worth/` (the paid ads funnel, noindex)

## Confirmation emails

**Nothing sends a confirmation to the enquirer while the site is on GitHub Pages.**

Tested on 28 September 2026: FormSubmit delivers the notification to Ben reliably, but
its `_autoresponse` never arrives. Three submissions were sent, with the form activated
and with a submitter address different from the notification address, and no confirmation
came back in any case. Its autoresponder is not available on the free tier. Even if it
were, it sends plain text, so it could never carry a designed email.

The templates in `email/` and the sender in `api/lead.js` are built, tested and ready.
They need somewhere that can run a function, which GitHub Pages cannot.

Harbour Studios already sends through Resend from `website@harbourstudios.nz`, and all
four of Ben's templates were sent through that account on 28 September 2026 and arrived
correctly. So the templates and the key are both proven. What is missing is a place to
run the function, and a verified sending domain of Ben's own.

`benpotter.co.nz` is Ben's own domain, bought in October 2026 and managed by him at
Domains Direct. The old `benpotter.co.nz` Webflow address is not under his control and
nothing on this site points at it. If he regains it, a 301 at the registrar is enough.

To turn them on:

1. Import this repo at [vercel.com/new](https://vercel.com/new) or
   [app.netlify.com/start](https://app.netlify.com/start). `vercel.json` and
   `netlify.toml` are already here, and there is nothing to build: `build.py` has
   written the HTML into the repo already.
2. Add `benpotter.co.nz` in the Resend dashboard, copy the DNS records it gives you
   into Cloudflare, and wait for it to go green. The existing Harbour Studios key can
   then send as Ben, or issue a new one scoped to his domain.
3. Set four environment variables on the host:
   `RESEND_API_KEY`, `MAIL_FROM` (for example `Ben Potter <ben@benpotter.co.nz>`),
   `LEAD_TO` (`ben.potter@harcourts.co.nz`) and `ALLOWED_ORIGINS`.
   `tools/deploy-vercel.sh` does the linking, the variables and the deploy in one go.
4. In `tools/content.py` set `FORM_PROVIDER = "endpoint"`, and set `FORM_ENDPOINT` to
   the deployed function, for example `https://ben-potter.vercel.app/api/lead`. Rebuild.

Until step 2 finishes, `MAIL_FROM` can stay on a verified Harbour Studios address so
forms keep working. Switching to Ben's domain later is one environment variable and no
code change.

The function already sends CORS headers, so the site can stay on GitHub Pages and call
the function on the other host if that is easier. Add any extra origin to
`ALLOWED_ORIGINS`.

Four emails are covered: the notification to Ben, and confirmations for an appraisal
request, a guide download and a contact enquiry. `node` the test in the commit history
to see all four rendered.

## Launch checklist

Everything below lives in `tools/content.py` unless noted.

0. **`LEAD_TEST_MODE = False`** — while it is `True`, every form submission is delivered
   to `LEAD_TEST_EMAIL` and Ben receives nothing. `build.py` prints a warning on every
   build while it is on. This is the easiest thing to forget.
1. `PREVIEW = False` — removes `noindex` from every page and switches `robots.txt` from
   disallow-all to allow-all with the sitemap reference.
2. `SITE` — `https://www.benpotter.co.nz`. Canonicals, Open Graph
   URLs and the sitemap all derive from it.
3. `STREET` — the Devonport office street address. Currently empty, so `streetAddress` is omitted
   from the schema. Local SEO wants it filled.
4. `EMAIL` — `ben.potter@harcourts.co.nz`, confirmed on Ben's selling guide.
5. `GA4_ID` — add the measurement ID and the gtag snippet appears on every page. Empty means no
   tag is emitted at all.
6. `GSC_TOKEN` — only needed if Search Console verification uses the HTML tag method. DNS or the
   Google Analytics method needs nothing here.
7. Copy the right file from `deploy/` to the host so `/listings` from the old Webflow site
   301s to `/recently-sold/`. GitHub Pages cannot do server redirects; Netlify, Vercel, Cloudflare
   and Apache all can.
8. Submit `sitemap.xml` in Search Console and request indexing on the three suburb pages.
9. **Activate lead email.** `FORM_PROVIDER = "formsubmit"` sends every appraisal and guide
   submission to `LEAD_EMAIL`. It needs no account, but the **first** submission triggers a
   one-time confirmation email to that address. Submit the appraisal form once, have Ben click
   the confirmation link, and every lead after that is forwarded automatically with the
   enquirer set as reply-to. To use Web3Forms instead, set `FORM_PROVIDER = "web3forms"` and put
   an access key in `FORM_KEY`. `"none"` disables sending.
10. The reel is self-hosted at `video/` and needs no action. To replace it, drop in a new source
    and run `tools/transcode.swift` (see the header comment for arguments), then update
    `REEL_SECONDS` and `REEL_DATE`.
11. The selling guide PDF is in place at `guide/ben-potter-selling-guide.pdf` (16 pages, 2.6 MB).
    Replace that file to update it; the path lives in `GUIDE_FILE`. If Ben revises the contents,
    update `GUIDE_CONTENTS` so the page listing and the `DigitalDocument` schema stay accurate.

## Still needed from Ben

Photography (peninsula, streetscapes, listing photos, the beach shot for the hero), the reel link,
real sold listings, CRM API details, and his RateMyAgent feed.

Listing card photos drop into `img/listings/` using the filenames already commented into the card
markup, e.g. `img/listings/old-lake-road-devonport.jpg`.

## Branded emails

`email/` holds three HTML templates, built by `python3 tools/emails.py` from
`tools/content.py` so the phone number, address and guide title never drift:

| File | Goes to | Contains |
| --- | --- | --- |
| `lead-notification.html` | Ben | The enquiry, with call and reply buttons |
| `confirmation-guide.html` | The enquirer | A real Download the guide button |
| `confirmation-appraisal.html` | The enquirer | What happens next, in four steps |

They are table based with inline styles, 600px, no webfonts, with an Outlook
fallback, because email clients are not browsers.

**These only send through `FORM_PROVIDER = "endpoint"`.** FormSubmit cannot use custom
HTML: its notification is a generic table and its autoresponder is plain text. Sending
branded HTML needs an email API key, and a key cannot sit in client-side JavaScript,
so `api/lead.js` exists to hold it. That needs hosting with functions.

### Switching it on

1. Move hosting to Netlify, Vercel or Cloudflare Pages. All free, and all three also
   fix two other things GitHub Pages cannot do: the `/listings` redirect from the old
   site, and instant cache purge on deploy.
2. Create a Resend account, verify `benpotter.co.nz` (SPF and DKIM), which is also what
   keeps these emails out of spam.
3. Set `RESEND_API_KEY`, `MAIL_FROM` and `LEAD_TO` as environment variables.
4. Set `FORM_PROVIDER = "endpoint"` in `tools/content.py` and rebuild.

Until then `FORM_PROVIDER = "formsubmit"` keeps leads flowing, just in FormSubmit's
plain styling.
