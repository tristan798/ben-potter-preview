# -*- coding: utf-8 -*-
"""Builds the branded HTML email templates into email/.

Email clients are not browsers: no webfonts, no flexbox or grid, no external CSS,
and Outlook renders through Word. So these are table based with inline styles only,
600px wide, and they degrade to a single readable column on a phone.
Run: python3 tools/emails.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import content as C

INK   = "#131315"
PAPER = "#F5F3EF"
WHITE = "#FFFFFF"
BLUE  = "#0A84FF"
TEXT  = "#17181B"
MUTED = "#75767A"
RULE  = "#E2DFD9"
SANS  = "'Helvetica Neue', Helvetica, Arial, sans-serif"


def button(label, href, bg=BLUE, fg="#ffffff"):
    """A padded anchor with an Outlook fallback, which is the reliable way to do this."""
    return f'''<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 12px">
                  <tr><td align="center" bgcolor="{bg}" style="border-radius:3px">
                    <!--[if mso]>&nbsp;<![endif]-->
                    <a href="{href}" target="_blank" style="display:inline-block; padding:15px 30px; font-family:{SANS}; font-size:13px; font-weight:bold; letter-spacing:1.4px; text-transform:uppercase; color:{fg}; text-decoration:none; border-radius:3px">{label}</a>
                    <!--[if mso]>&nbsp;<![endif]-->
                  </td></tr>
                </table>'''


def shell(preheader, body, footer_note=""):
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
  <tr><td align="center" style="padding:28px 16px">
    <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px; max-width:100%; background:{WHITE}; border-radius:4px; overflow:hidden">

      <tr><td bgcolor="{INK}" style="padding:26px 32px">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td style="font-family:{SANS}; font-size:16px; font-weight:bold; letter-spacing:2.6px; text-transform:uppercase; color:#F0EEE9">BEN POTTER</td>
          <td align="right" style="font-family:{SANS}; font-size:11px; letter-spacing:1.6px; text-transform:uppercase; color:#8C8B86">{C.AGENCY}</td>
        </tr></table>
      </td></tr>

      <tr><td style="padding:34px 32px 30px">{body}</td></tr>

      <tr><td style="padding:0 32px"><div style="height:1px; background:{RULE}; line-height:1px">&nbsp;</div></td></tr>
      <tr><td style="padding:22px 32px 30px">
        <p style="margin:0 0 4px; font-family:{SANS}; font-size:14px; font-weight:bold; color:{TEXT}">{C.AGENT_NAME}</p>
        <p style="margin:0 0 10px; font-family:{SANS}; font-size:13px; color:{MUTED}">{C.AGENT_TITLE} &middot; {C.AGENCY}</p>
        <p style="margin:0; font-family:{SANS}; font-size:13px; color:{MUTED}">
          <a href="tel:{C.PHONE_LINK}" style="color:{TEXT}; text-decoration:none">{C.PHONE_DISPLAY}</a> &nbsp;&middot;&nbsp;
          <a href="mailto:{C.EMAIL}" style="color:{TEXT}; text-decoration:none">{C.EMAIL}</a>
        </p>
        <p style="margin:12px 0 0; font-family:{SANS}; font-size:11px; letter-spacing:1.4px; text-transform:uppercase; color:#A3A29E">Auckland&rsquo;s North Shore</p>
      </td></tr>

    </table>
    <p style="margin:16px 0 0; font-family:{SANS}; font-size:11px; color:#A3A29E">{footer_note}</p>
  </td></tr>
</table>
</body>
</html>
'''


def row(label, value, mono=False, field=None):
    """field marks the row droppable: the sender strips it when that value is empty, so
    a contact enquiry does not arrive with "Property: Not given" sitting under it."""
    fam = "'SF Mono', Consolas, monospace" if mono else SANS
    tag = ('<tr data-optional="%s">' % field) if field else '<tr>'
    return f'''{tag}
            <td width="132" style="padding:11px 0; border-bottom:1px solid {RULE}; font-family:{SANS}; font-size:11px; letter-spacing:1.3px; text-transform:uppercase; color:{MUTED}; vertical-align:top">{label}</td>
            <td style="padding:11px 0; border-bottom:1px solid {RULE}; font-family:{fam}; font-size:15px; color:{TEXT}">{value}</td>
          </tr>'''


# ---------------------------------------------------------------- 1. lead notification, to Ben
lead_body = f'''<p style="margin:0 0 6px; font-family:{SANS}; font-size:11px; font-weight:bold; letter-spacing:2px; text-transform:uppercase; color:{BLUE}">{{{{kind}}}}</p>
        <h1 style="margin:0 0 6px; font-family:{SANS}; font-size:27px; font-weight:bold; letter-spacing:-0.6px; color:{TEXT}">{{{{name}}}}</h1>
        <p style="margin:0 0 24px; font-family:{SANS}; font-size:16px; color:{MUTED}">{{{{subtitle}}}}</p>

        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 26px">
          {row("Mobile", '<a href="tel:{{phone_link}}" style="color:' + TEXT + '; text-decoration:none">{{phone}}</a>', mono=True)}
          {row("Email", '<a href="mailto:{{email}}" style="color:' + TEXT + '; text-decoration:none">{{email}}</a>')}
          {row("About", "{{topic}}", field="topic")}
          {row("Property", "{{property}}", field="property")}
          {row("Type", "{{type}}", field="type")}
          {row("Bedrooms", "{{bedrooms}}", field="bedrooms")}
          {row("Timeframe", "{{timeframe}}", field="timeframe")}
          {row("Message", "{{message}}", field="message")}
        </table>

        {button("Call {{name_first}}", "tel:{{phone_link}}")}
        {button("Reply by email", "mailto:{{email}}", bg="#FFFFFF", fg=TEXT).replace('border-radius:3px"', 'border-radius:3px; border:1px solid ' + RULE + '"')}

        <p data-optional="page" style="margin:18px 0 0; font-family:{SANS}; font-size:12px; color:{MUTED}">Came in from <a href="{{{{page}}}}" style="color:{MUTED}">{{{{page}}}}</a></p>'''

# ---------------------------------------------------------------- 2. guide confirmation, to the enquirer
guide_body = f'''<p style="margin:0 0 6px; font-family:{SANS}; font-size:11px; font-weight:bold; letter-spacing:2px; text-transform:uppercase; color:{BLUE}">Your free guide</p>
        <h1 style="margin:0 0 14px; font-family:{SANS}; font-size:27px; font-weight:bold; letter-spacing:-0.6px; color:{TEXT}">Here it is, {{{{name_first}}}}.</h1>
        <p style="margin:0 0 22px; font-family:{SANS}; font-size:16px; line-height:1.6; color:#4B4D53">
          <strong>{C.GUIDE_TITLE}</strong>. {C.GUIDE_PAGES} pages on preparing and positioning a home for
          sale so it reaches the widest pool of buyers and sells for more.</p>

        {button("Download the guide", C.SITE + "/" + C.GUIDE_FILE)}

        <p style="margin:6px 0 26px; font-family:{SANS}; font-size:12px; color:{MUTED}">PDF, {C.GUIDE_PAGES} pages. Free to keep and share.</p>

        <div style="height:1px; background:{RULE}; line-height:1px; margin:0 0 22px">&nbsp;</div>

        <p style="margin:0 0 14px; font-family:{SANS}; font-size:16px; line-height:1.6; color:#4B4D53">
          If you would like to know what your own home is worth, I will give you a written appraisal built from
          recent comparable sales near you. No cost, and no obligation to list.</p>
        {button("Book a free appraisal", C.SITE + "/property-appraisal/", bg="#FFFFFF", fg=TEXT).replace('border-radius:3px"', 'border-radius:3px; border:1px solid ' + RULE + '"')}'''

# ---------------------------------------------------------------- 3. appraisal confirmation, to the enquirer
appraisal_body = f'''<p style="margin:0 0 6px; font-family:{SANS}; font-size:11px; font-weight:bold; letter-spacing:2px; text-transform:uppercase; color:{BLUE}">Request received</p>
        <h1 style="margin:0 0 14px; font-family:{SANS}; font-size:27px; font-weight:bold; letter-spacing:-0.6px; color:{TEXT}">Thanks, {{{{name_first}}}}.</h1>
        <p style="margin:0 0 20px; font-family:{SANS}; font-size:16px; line-height:1.6; color:#4B4D53">
          I have your request for <strong>{{{{property}}}}</strong> and I will call you within one business day to
          arrange a time to see the property.</p>

        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 24px; background:{PAPER}; border-radius:3px">
          <tr><td style="padding:18px 20px">
            <p style="margin:0 0 10px; font-family:{SANS}; font-size:11px; font-weight:bold; letter-spacing:1.6px; text-transform:uppercase; color:{MUTED}">What happens next</p>
            <p style="margin:0 0 7px; font-family:{SANS}; font-size:15px; line-height:1.55; color:#4B4D53">1. A walk through the house, half an hour or so.</p>
            <p style="margin:0 0 7px; font-family:{SANS}; font-size:15px; line-height:1.55; color:#4B4D53">2. A written estimate of value from recent comparable sales.</p>
            <p style="margin:0 0 7px; font-family:{SANS}; font-size:15px; line-height:1.55; color:#4B4D53">3. A recommended method of sale, with a marketing plan and budget.</p>
            <p style="margin:0; font-family:{SANS}; font-size:15px; line-height:1.55; color:#4B4D53">4. An honest view on what to fix and what to leave alone.</p>
          </td></tr>
        </table>

        <p style="margin:0 0 16px; font-family:{SANS}; font-size:16px; line-height:1.6; color:#4B4D53">
          While you wait, my selling guide covers how to prepare a home for sale.</p>
        {button("Read the selling guide", C.SITE + "/" + C.GUIDE_FILE, bg="#FFFFFF", fg=TEXT).replace('border-radius:3px"', 'border-radius:3px; border:1px solid ' + RULE + '"')}

        <p style="margin:18px 0 0; font-family:{SANS}; font-size:15px; line-height:1.6; color:#4B4D53">
          If anything is urgent, call me on <a href="tel:{C.PHONE_LINK}" style="color:{BLUE}; text-decoration:none"><strong>{C.PHONE_DISPLAY}</strong></a>.</p>'''


# ---------------------------------------------------------------- 4. contact confirmation, to the enquirer
contact_body = f'''<p style="margin:0 0 6px; font-family:{SANS}; font-size:11px; font-weight:bold; letter-spacing:2px; text-transform:uppercase; color:{BLUE}">Message received</p>
        <h1 style="margin:0 0 14px; font-family:{SANS}; font-size:27px; font-weight:bold; letter-spacing:-0.6px; color:{TEXT}">Thanks, {{{{name_first}}}}.</h1>
        <p style="margin:0 0 22px; font-family:{SANS}; font-size:16px; line-height:1.6; color:#4B4D53">
          Your message has come through and I will come back to you within one business day.</p>

        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 26px; background:{PAPER}; border-radius:3px">
          <tr><td style="padding:18px 20px">
            <p style="margin:0 0 10px; font-family:{SANS}; font-size:11px; font-weight:bold; letter-spacing:1.6px; text-transform:uppercase; color:{MUTED}">What you sent</p>
            <p style="margin:0 0 8px; font-family:{SANS}; font-size:15px; line-height:1.55; color:{TEXT}"><strong>{{{{topic}}}}</strong></p>
            <p style="margin:0; font-family:{SANS}; font-size:15px; line-height:1.6; color:#4B4D53">{{{{message}}}}</p>
          </td></tr>
        </table>

        <p style="margin:0 0 16px; font-family:{SANS}; font-size:16px; line-height:1.6; color:#4B4D53">
          If it is quicker to talk, call me any time.</p>
        {button("Call " + C.PHONE_DISPLAY, "tel:" + C.PHONE_LINK)}

        <p style="margin:12px 0 0; font-family:{SANS}; font-size:15px; line-height:1.6; color:#4B4D53">
          In the meantime, my selling guide covers how to prepare a home for sale.
          <a href="{C.SITE}/{C.GUIDE_FILE}" style="color:{BLUE}; text-decoration:none"><strong>Read it here</strong></a>.</p>'''


def main():
    out = os.path.join(HERE, '..', 'email')
    os.makedirs(out, exist_ok=True)
    files = {
        'lead-notification.html': shell("New enquiry from the website", lead_body,
                                        "Sent by the website at ben-potter.com"),
        'confirmation-guide.html': shell(
            "Your copy of A Proven Strategy to Maximise Your Sale Price", guide_body,
            "You received this because you asked for the guide at ben-potter.com"),
        'confirmation-appraisal.html': shell(
            "Ben will call you within one business day", appraisal_body,
            "You received this because you requested an appraisal at ben-potter.com"),
        'confirmation-contact.html': shell(
            "Ben will come back to you within one business day", contact_body,
            "You received this because you sent a message at ben-potter.com"),
    }
    for name, html in files.items():
        open(os.path.join(out, name), 'w', encoding='utf-8').write(html)
        print('  email/%s  %d KB' % (name, len(html) / 1024))


main()
