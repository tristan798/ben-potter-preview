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
 *   MAIL_FROM        e.g. "Ben Potter <ben@benpotter.co.nz>"  (domain must be verified)
 *   MAIL_FROM_FALLBACK  a sender on an already verified domain. Used only if MAIL_FROM
 *                    is refused, which is what happens while its DNS is still
 *                    propagating. Lets the switch happen without a window where
 *                    every form is broken.
 *   LEAD_TO          where the notification goes. Internal routing, never shown to a lead.
 *   LEAD_CC          a second, independent inbox. One mail server having a bad morning
 *                    should not be the difference between Ben getting a lead and not.
 *   REPLY_TO         what a lead replies to. Public, so it is always one of Ben's own
 *                    addresses, even while LEAD_TO points somewhere else for testing.
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

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Every submission sends two emails back to back, and Resend rate limits per second,
// so two people submitting at the same moment is enough to get a 429. Without this a
// confirmation just quietly vanishes, which is exactly what it did in testing.
async function post(payload) {
  return fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });
}

async function send(payload, attempt = 0) {
  let res = await post(payload);

  // While Ben's domain is still propagating, Resend refuses to send as him. Rather than
  // fail the form, fall back to a sender that is already verified. The moment his DNS
  // goes green this stops firing on its own, with no redeploy and no flipped setting.
  if (!res.ok && (res.status === 403 || res.status === 422) && process.env.MAIL_FROM_FALLBACK
      && payload.from !== process.env.MAIL_FROM_FALLBACK) {
    const why = await res.text();
    if (/domain|verif/i.test(why)) {
      console.warn('MAIL_FROM refused, falling back:', why.slice(0, 160));
      return send(Object.assign({}, payload, { from: process.env.MAIL_FROM_FALLBACK }), attempt);
    }
    throw new Error(`resend ${res.status}: ${why}`);
  }

  if (res.ok) return res.json();
  const retryable = res.status === 429 || res.status >= 500;
  if (retryable && attempt < 4) {
    await sleep(600 * Math.pow(2, attempt));       // 0.6s, 1.2s, 2.4s, 4.8s
    return send(payload, attempt + 1);
  }
  throw new Error(`resend ${res.status}: ${await res.text()}`);
}

async function handle(body) {
  if (body.botcheck) return { success: 'true' };          // honeypot, pretend it worked

  // Written before anything is attempted, so a lead exists in the record even if every
  // send fails afterwards. One line, one prefix, so it can be found in the logs.
  console.log('LEAD ' + JSON.stringify({
    at: new Date().toISOString(),
    kind: body.kind || 'unknown',
    name: body.name || '',
    email: body.email || '',
    phone: body.phone || '',
    address: body.address || '',
    topic: body.topic || '',
    message: body.message || '',
    timeframe: body.timeframe || '',
    type: body.type || '',
    bedrooms: body.bedrooms || '',
    page: body.page || '',
  }));

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

  const notifyTo = [process.env.LEAD_TO].concat(
    (process.env.LEAD_CC || '').split(',').map((a) => a.trim()).filter(Boolean)
  );
  await send({
    from: process.env.MAIL_FROM,
    to: notifyTo,
    reply_to: values.email || undefined,
    subject,
    html: render('lead-notification.html', values),
  });
  console.log('LEAD DELIVERED to ' + notifyTo.join(', '));

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
        // Never LEAD_TO: that can be a testing address, and a lead hitting reply
        // must always reach Ben rather than whoever is checking the forms.
        reply_to: process.env.REPLY_TO || process.env.LEAD_TO,
        subject: subj,
        html: render(tpl, values),
      });
    } catch (err) {
      console.error('confirmation failed, lead still delivered:', err);
    }
  }

  return { success: 'true' };
}

// The function and the site can be served from different origins, so the browser needs
// these before it will hand over a response. Set ALLOWED_ORIGINS to override.
const ALLOWED = (process.env.ALLOWED_ORIGINS ||
  'https://www.benpotter.co.nz,https://benpotter.co.nz')
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
