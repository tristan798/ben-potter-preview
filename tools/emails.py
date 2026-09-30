# -*- coding: utf-8 -*-
"""Builds the branded HTML email templates into email/.

Email clients are not browsers: no webfonts, no flexbox or grid, no external CSS, and
Outlook renders through Word. So these are table based with inline styles only, 600px
wide, and they degrade to a single readable column on a phone.

The design follows the site's own dark theme, the one the hero opens with: near-black
field, warm off-white type, a single blue accent, hairlines instead of boxes, and one
action. No header bar, no panels, no second button competing with the first.

Clash Display and Poppins are loaded from the site over https, so Apple Mail and iOS
Mail, which is most of the phones these land on, get the real thing. Gmail and Outlook
strip webfonts and fall back to Helvetica, which is why every rule still has to hold up
in the fallback. Nothing depends on the font loading.

Dark mail is the one case where clients fight back: Gmail and Outlook will invert a
light email in dark mode and make a mess of it. Declaring the scheme up front stops
them touching a design that is already dark.

Run: python3 tools/emails.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import content as C

# Straight off the site's dark tokens.
INK    = "#131315"      # --ink, the page field
PANEL  = "#1B1C1F"      # the lighter stop in the hero gradient
FG     = "#F0EEE9"      # --fg
BODY   = "#C7C5C0"      # --fg-2
MUTED  = "#8B8984"      # --mute
BLUE   = "#4DA3FF"      # --accent, the on-dark blue
RULE   = "#2A2B2E"      # rgba(240,238,233,.13) flattened, since email needs it solid
PAPER  = "#F0EEE9"      # the light button, as in the hero

DISPLAY = "'Clash Display', 'Poppins', 'Helvetica Neue', Helvetica, Arial, sans-serif"
SANS    = "'Poppins', 'Helvetica Neue', Helvetica, Arial, sans-serif"
FONT_BASE = C.asset_base() + "/assets/fonts/"

GUIDE_URL = C.asset_base() + "/" + C.GUIDE_FILE


def label(text):
    return (f'<p style="margin:0 0 16px; font-family:{SANS}; font-size:11px; font-weight:600; '
            f'letter-spacing:2.2px; text-transform:uppercase; color:{BLUE}">{text}</p>')


def h1(text):
    """Clash Display where it loads, Helvetica where it does not. The negative tracking
    is what the site uses and it flatters both."""
    return (f'<h1 style="margin:0 0 22px; font-family:{DISPLAY}; font-size:34px; line-height:1.12; '
            f'font-weight:500; letter-spacing:-1px; color:{FG}">{text}</h1>')


def p(text, top=0, bottom=18, size=16, colour=None):
    return (f'<p style="margin:{top}px 0 {bottom}px; font-family:{SANS}; font-size:{size}px; '
            f'font-weight:300; line-height:1.7; color:{colour or BODY}">{text}</p>')


def rule(space=32):
    return (f'<div style="height:1px; background:{RULE}; line-height:1px; '
            f'font-size:0; margin:{space}px 0">&nbsp;</div>')


def button(text, href):
    """One action per email, light on dark exactly as the hero does it."""
    return f'''<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:4px 0 0">
          <tr><td bgcolor="{PAPER}" style="border-radius:2px">
            <!--[if mso]>&nbsp;<![endif]-->
            <a href="{href}" target="_blank" style="display:inline-block; padding:17px 34px; font-family:{SANS}; font-size:12px; font-weight:600; letter-spacing:1.6px; text-transform:uppercase; color:{INK}; text-decoration:none">{text}</a>
            <!--[if mso]>&nbsp;<![endif]-->
          </td></tr>
        </table>'''


def quiet_link(text, href):
    return (f'<a href="{href}" style="color:{FG}; text-decoration:none; '
            f'border-bottom:1px solid {BLUE}">{text}</a>')


def font_faces():
    """Served from the site over https. Apple Mail and iOS Mail honour these; Gmail and
    Outlook strip them and take the Helvetica fallback in every inline font-family."""
    faces = [("Clash Display", 500, "clash-display-500"),
             ("Clash Display", 600, "clash-display-600"),
             ("Poppins", 300, "poppins-300"),
             ("Poppins", 400, "poppins-400"),
             ("Poppins", 600, "poppins-600")]
    return "\n".join(
        '@font-face{font-family:"%s";font-weight:%d;font-style:normal;font-display:swap;'
        'src:url(%s%s.woff2) format("woff2");}' % (fam, weight, FONT_BASE, f)
        for fam, weight, f in faces)


def shell(preheader, body):
    return f'''<!doctype html>
<html lang="en-NZ">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<meta name="color-scheme" content="dark">
<meta name="supported-color-schemes" content="dark">
<title>{C.AGENT_NAME}</title>
<style>
:root{{color-scheme:dark;supported-color-schemes:dark;}}
{font_faces()}
a{{text-decoration:none;}}
@media (max-width:620px){{
  .px{{padding-left:24px !important;padding-right:24px !important;}}
  .h1{{font-size:28px !important;}}
}}
</style>
<!--[if mso]><style>body,table,td,a,p,h1{{font-family:Arial,Helvetica,sans-serif !important}}</style><![endif]-->
</head>
<body style="margin:0; padding:0; background:{INK}; -webkit-text-size-adjust:100%">
<div style="display:none; max-height:0; overflow:hidden; opacity:0">{preheader}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="{INK}" style="background:{INK}">
  <tr><td align="center" style="padding:0">
    <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" bgcolor="{PANEL}" style="width:600px; max-width:100%; background:{PANEL}">

      <tr><td class="px" style="padding:44px 44px 0">
        <span style="font-family:{SANS}; font-size:13px; font-weight:600; letter-spacing:3px; text-transform:uppercase; color:{FG}">Ben Potter</span>
      </td></tr>

      <tr><td class="px" style="padding:38px 44px 0">{body}</td></tr>

      <tr><td class="px" style="padding:44px 44px 44px">
        <div style="height:1px; background:{RULE}; line-height:1px; font-size:0">&nbsp;</div>
        <p style="margin:24px 0 0; font-family:{SANS}; font-size:13px; font-weight:300; line-height:1.8; color:{MUTED}">
          {C.AGENT_NAME}<br>
          <a href="tel:{C.PHONE_LINK}" style="color:{MUTED}; text-decoration:none">{C.PHONE_DISPLAY}</a> &nbsp;
          <a href="mailto:{C.EMAIL}" style="color:{MUTED}; text-decoration:none">{C.EMAIL}</a><br>
          {C.AGENCY}
        </p>
      </td></tr>

    </table>
  </td></tr>
</table>
</body>
</html>
'''


def field(name, value, key=None):
    """One line of enquiry detail. Label above value, hairline under. No boxes."""
    tag = f'<tr data-optional="{key}">' if key else '<tr>'
    return f'''{tag}
          <td style="padding:0 0 16px">
            <p style="margin:0 0 4px; font-family:{SANS}; font-size:10px; font-weight:600; letter-spacing:1.8px; text-transform:uppercase; color:{MUTED}">{name}</p>
            <p style="margin:0; font-family:{SANS}; font-size:16px; font-weight:300; line-height:1.5; color:{FG}">{value}</p>
          </td>
        </tr>'''


# ---------------------------------------------------------------- 1. to Ben
lead_body = (
    label('{{kind}}')
    + h1('{{name}}')
    + p('{{subtitle}}', bottom=30, colour=MUTED)
    + f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
          {field("Mobile", '<a href="tel:{{phone_link}}" style="color:' + FG + '; text-decoration:none">{{phone}}</a>')}
          {field("Email", '<a href="mailto:{{email}}" style="color:' + FG + '; text-decoration:none">{{email}}</a>')}
          {field("About", "{{topic}}", key="topic")}
          {field("Property", "{{property}}", key="property")}
          {field("Type", "{{type}}", key="type")}
          {field("Bedrooms", "{{bedrooms}}", key="bedrooms")}
          {field("Timeframe", "{{timeframe}}", key="timeframe")}
          {field("Message", "{{message}}", key="message")}
        </table>'''
    + '<div style="height:12px; line-height:12px">&nbsp;</div>'
    + button('Call {{name_first}}', 'tel:{{phone_link}}')
    + '<p data-optional="page" style="margin:24px 0 0; font-family:' + SANS
    + f'; font-size:12px; color:{MUTED}">From <a href="{{{{page}}}}" style="color:{MUTED}">{{{{page}}}}</a></p>'
)

# ---------------------------------------------------------------- 2. guide, to the enquirer
guide_body = (
    label('Your free guide')
    + h1('Here it is, {{name_first}}.')
    + p(f'<strong style="color:{FG}; font-weight:400">{C.GUIDE_TITLE}</strong>. '
        f'{C.GUIDE_PAGES} pages on preparing and positioning a home so it reaches the widest '
        f'pool of buyers.', bottom=26)
    + button('Download the guide', GUIDE_URL)
    + rule()
    + p('If you would like to know what your own home is worth, I will give you a written '
        'appraisal built from recent comparable sales near you. No cost, and no obligation '
        f'to list. {quiet_link("Book a free appraisal", C.asset_base() + "/property-appraisal/")}.',
        bottom=0)
)

# ---------------------------------------------------------------- 3. appraisal, to the enquirer
appraisal_body = (
    label('Request received')
    + h1('Thanks, {{name_first}}.')
    + p('I have your request for <strong style="color:%s; font-weight:400">{{property}}</strong> '
        'and I will call you within one business day to arrange a time to see it.' % FG, bottom=26)
    + p('We will walk through the house, then you get a written estimate of value from recent '
        'comparable sales, a recommended method of sale, and an honest view on what is worth '
        'doing before the first open home.', bottom=26)
    + button('Read the selling guide', GUIDE_URL)
    + rule()
    + p('If anything is urgent, call me on %s.'
        % quiet_link(C.PHONE_DISPLAY, 'tel:' + C.PHONE_LINK), bottom=0)
)

# ---------------------------------------------------------------- 4. contact, to the enquirer
contact_body = (
    label('Message received')
    + h1('Thanks, {{name_first}}.')
    + p('Your message has come through and I will come back to you within one business day.',
        bottom=26)
    + f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
          {field("You asked about", "{{topic}}", key="topic")}
          {field("You wrote", "{{message}}", key="message")}
        </table>'''
    + rule()
    + p('If it is quicker to talk, call me on %s.'
        % quiet_link(C.PHONE_DISPLAY, 'tel:' + C.PHONE_LINK), bottom=0)
)


def main():
    out = os.path.join(HERE, '..', 'email')
    os.makedirs(out, exist_ok=True)
    files = {
        'lead-notification.html': shell('New enquiry from the website', lead_body),
        'confirmation-guide.html': shell(
            'Your copy of %s' % C.GUIDE_TITLE, guide_body),
        'confirmation-appraisal.html': shell(
            'Ben will call you within one business day', appraisal_body),
        'confirmation-contact.html': shell(
            'Ben will come back to you within one business day', contact_body),
    }
    for name, html in files.items():
        open(os.path.join(out, name), 'w', encoding='utf-8').write(html)
        print('  email/%s  %d KB' % (name, len(html) / 1024))


main()
