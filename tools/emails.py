# -*- coding: utf-8 -*-
"""Builds the branded HTML email templates into email/.

Email clients are not browsers: no webfonts, no flexbox or grid, no external CSS, and
Outlook renders through Word. So these are table based with inline styles only, 600px
wide, and they degrade to a single readable column on a phone.

The design follows the site rather than the usual marketing-email conventions: paper
background, one small accent label, one large heading, one action, and a hairline rule
instead of boxes. No coloured header bar, no panels, no second button competing with
the first. Restraint is the brand.

Run: python3 tools/emails.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import content as C

INK   = "#17181B"
PAPER = "#F5F3EF"
BODY  = "#55565B"
MUTED = "#8A8A86"
BLUE  = "#0A84FF"
RULE  = "#E3E0DA"
SANS  = "'Helvetica Neue', Helvetica, Arial, sans-serif"

GUIDE_URL = C.asset_base() + "/" + C.GUIDE_FILE


def label(text):
    return (f'<p style="margin:0 0 14px; font-family:{SANS}; font-size:11px; font-weight:bold; '
            f'letter-spacing:2.2px; text-transform:uppercase; color:{BLUE}">{text}</p>')


def h1(text):
    return (f'<h1 style="margin:0 0 20px; font-family:{SANS}; font-size:30px; line-height:1.15; '
            f'font-weight:bold; letter-spacing:-0.8px; color:{INK}">{text}</h1>')


def p(text, top=0, bottom=18, size=16, colour=None):
    return (f'<p style="margin:{top}px 0 {bottom}px; font-family:{SANS}; font-size:{size}px; '
            f'line-height:1.65; color:{colour or BODY}">{text}</p>')


def rule(space=30):
    return (f'<div style="height:1px; background:{RULE}; line-height:1px; '
            f'margin:{space}px 0">&nbsp;</div>')


def button(text, href):
    """One action per email. A padded anchor with the Outlook fallback around it."""
    return f'''<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:4px 0 0">
          <tr><td bgcolor="{INK}" style="border-radius:2px">
            <!--[if mso]>&nbsp;<![endif]-->
            <a href="{href}" target="_blank" style="display:inline-block; padding:16px 32px; font-family:{SANS}; font-size:12px; font-weight:bold; letter-spacing:1.6px; text-transform:uppercase; color:#FFFFFF; text-decoration:none">{text}</a>
            <!--[if mso]>&nbsp;<![endif]-->
          </td></tr>
        </table>'''


def quiet_link(text, href):
    return (f'<a href="{href}" style="color:{INK}; text-decoration:none; '
            f'border-bottom:1px solid {BLUE}">{text}</a>')


def shell(preheader, body):
    return f'''<!doctype html>
<html lang="en-NZ">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<title>{C.AGENT_NAME}</title>
<!--[if mso]><style>body,table,td{{font-family:Arial,Helvetica,sans-serif !important}}</style><![endif]-->
</head>
<body style="margin:0; padding:0; background:{PAPER}; -webkit-text-size-adjust:100%">
<div style="display:none; max-height:0; overflow:hidden; opacity:0">{preheader}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{PAPER}">
  <tr><td align="center" style="padding:44px 20px 40px">
    <table role="presentation" width="560" cellpadding="0" cellspacing="0" border="0" style="width:560px; max-width:100%">

      <tr><td style="padding:0 0 34px">
        <span style="font-family:{SANS}; font-size:13px; font-weight:bold; letter-spacing:3px; text-transform:uppercase; color:{INK}">Ben Potter</span>
      </td></tr>

      <tr><td>{body}</td></tr>

      <tr><td style="padding:40px 0 0">
        <div style="height:1px; background:{RULE}; line-height:1px">&nbsp;</div>
        <p style="margin:22px 0 0; font-family:{SANS}; font-size:13px; line-height:1.7; color:{MUTED}">
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
          <td style="padding:0 0 14px">
            <p style="margin:0 0 3px; font-family:{SANS}; font-size:10px; font-weight:bold; letter-spacing:1.8px; text-transform:uppercase; color:{MUTED}">{name}</p>
            <p style="margin:0; font-family:{SANS}; font-size:16px; line-height:1.5; color:{INK}">{value}</p>
          </td>
        </tr>'''


# ---------------------------------------------------------------- 1. to Ben
lead_body = (
    label('{{kind}}')
    + h1('{{name}}')
    + p('{{subtitle}}', bottom=30, colour=MUTED)
    + f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
          {field("Mobile", '<a href="tel:{{phone_link}}" style="color:' + INK + '; text-decoration:none">{{phone}}</a>')}
          {field("Email", '<a href="mailto:{{email}}" style="color:' + INK + '; text-decoration:none">{{email}}</a>')}
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
    + p(f'<strong style="color:{INK}; font-weight:normal">{C.GUIDE_TITLE}</strong>. '
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
    + p('I have your request for <strong style="color:%s; font-weight:normal">{{property}}</strong> '
        'and I will call you within one business day to arrange a time to see it.' % INK, bottom=26)
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
