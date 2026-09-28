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
  let html = template(name);
  // Drop the rows this kind of enquiry has nothing to say about, so a contact message
  // does not arrive with "Property: Not given" sitting under it.
  html = html.replace(/<tr data-optional="(\w+)">[\s\S]*?<\/tr>/g, (block, key) =>
    values[key] ? block : '');
  html = html.replace(/<p data-optional="(\w+)"[\s\S]*?<\/p>/g, (block, key) =>
    values[key] ? block : '');
  return html.replace(/\{\{(\w+)\}\}/g, (_, k) =>
    escapeHtml(values[k] !== undefined && values[k] !== '' ? values[k] : 'Not given'));
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
    contact: 'Website enquiry',
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
    topic: body.topic || '',
    message: body.message || '',
    page: body.page || '',
  };
  // The line under the name: the address when there is one, otherwise what they asked
  // about. Never the words "Not given".
  values.subtitle = values.property || values.topic || kind;

  const subject = body.kind === 'contact'
    ? `Website enquiry${values.topic ? ': ' + values.topic : ''}${name ? ' from ' + name : ''}`
    : `${kind}${name ? ' from ' + name : ''}${body.address ? ', ' + body.address : ''}`;

  await send({
    from: process.env.MAIL_FROM,
    to: [process.env.LEAD_TO],
    reply_to: values.email || undefined,
    subject,
    html: render('lead-notification.html', values),
  });

  // Every submission gets a confirmation. If this one throws, the notification to Ben
  // has already gone, so the lead is never lost to a confirmation failure.
  if (values.email) {
    const confirmations = {
      guide: ['confirmation-guide.html',
              'Your copy of A Proven Strategy to Maximise Your Sale Price'],
      contact: ['confirmation-contact.html', 'Thanks for getting in touch'],
    };
    const [tpl, subj] = confirmations[body.kind] ||
                        ['confirmation-appraisal.html', 'Thanks, I will call you shortly'];
    try {
      await send({
        from: process.env.MAIL_FROM,
        to: [values.email],
        reply_to: process.env.LEAD_TO,
        subject: subj,
        html: render(tpl, values),
      });
    } catch (err) {
      console.error('confirmation failed, lead still delivered:', err);
    }
  }

  return { success: 'true' };
}

// The site may be served from a different origin to this function (GitHub Pages now,
// ben-potter.com later), so the browser needs these before it will hand over a response.
const ALLOWED = (process.env.ALLOWED_ORIGINS ||
  'https://tristan798.github.io,https://ben-potter.com,https://www.ben-potter.com')
  .split(',').map((s) => s.trim());

function cors(req, res) {
  const origin = req.headers && (req.headers.origin || req.headers.Origin);
  if (origin && ALLOWED.indexOf(origin) !== -1) {
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Vary', 'Origin');
  }
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Access-Control-Max-Age', '86400');
}

// Vercel / Node
module.exports = async (req, res) => {
  cors(req, res);
  if (req.method === 'OPTIONS') return res.status(204).end();
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
