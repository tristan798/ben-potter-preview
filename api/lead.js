/**
 * Lead handler: emails Ben a branded notification and sends the enquirer a branded
 * confirmation. Runs on Vercel (api/lead.js) or Netlify (netlify/functions/lead.js).
 *
 * Why a function at all: sending branded HTML email needs an API key, and an API key
 * cannot live in client-side JavaScript. This is the smallest piece of server that
 * makes that safe.
 *
 * Environment variables:
 *   RESEND_API_KEY   from resend.com
 *   MAIL_FROM        e.g. "Ben Potter <ben@ben-potter.com>"  (domain must be verified)
 *   LEAD_TO          e.g. "ben.potter@harcourts.co.nz"
 */
const fs = require('fs');
const path = require('path');

const TEMPLATE_DIR = path.join(__dirname, '..', 'email');
const cache = {};

function template(name) {
  if (!cache[name]) cache[name] = fs.readFileSync(path.join(TEMPLATE_DIR, name), 'utf8');
  return cache[name];
}

function escapeHtml(v) {
  return String(v == null ? '' : v)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function render(name, values) {
  return template(name).replace(/\{\{(\w+)\}\}/g, (_, k) =>
    escapeHtml(values[k] !== undefined && values[k] !== '' ? values[k] : '—'));
}

async function send(payload) {
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`resend ${res.status}: ${await res.text()}`);
  return res.json();
}

async function handle(body) {
  if (body.botcheck) return { success: 'true' };          // honeypot, pretend it worked

  const kindLabels = {
    guide: 'Selling guide download',
    funnel: 'Appraisal request (Meta ad)',
    appraisal: 'Appraisal request',
  };
  const kind = kindLabels[body.kind] || 'Website enquiry';
  const name = (body.name || '').trim();
  const first = name.split(' ')[0] || 'there';
  const phone = (body.phone || '').trim();

  const values = {
    kind,
    name: name || 'New enquiry',
    name_first: first,
    phone,
    phone_link: phone.replace(/[^\d+]/g, '').replace(/^0/, '+64'),
    email: (body.email || '').trim(),
    property: body.address || '',
    type: body.type || '',
    bedrooms: body.bedrooms || '',
    timeframe: body.timeframe || '',
    page: body.page || '',
  };

  const subject = `${kind}${name ? ' from ' + name : ''}${body.address ? ', ' + body.address : ''}`;

  await send({
    from: process.env.MAIL_FROM,
    to: [process.env.LEAD_TO],
    reply_to: values.email || undefined,
    subject,
    html: render('lead-notification.html', values),
  });

  if (values.email) {
    const isGuide = body.kind === 'guide';
    await send({
      from: process.env.MAIL_FROM,
      to: [values.email],
      subject: isGuide
        ? 'Your copy of A Proven Strategy to Maximise Your Sale Price'
        : 'Thanks, I will call you shortly',
      html: render(isGuide ? 'confirmation-guide.html' : 'confirmation-appraisal.html', values),
    });
  }

  return { success: 'true' };
}

// Vercel / Node
module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ success: 'false' });
  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};
    res.status(200).json(await handle(body));
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: 'false', message: 'Could not send' });
  }
};
module.exports.handle = handle;
