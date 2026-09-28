// Netlify wrapper around the shared handler in api/lead.js
const { handle } = require('../../api/lead.js');

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: JSON.stringify({ success: 'false' }) };
  }
  try {
    const result = await handle(JSON.parse(event.body || '{}'));
    return { statusCode: 200, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(result) };
  } catch (err) {
    console.error(err);
    return { statusCode: 500, body: JSON.stringify({ success: 'false', message: 'Could not send' }) };
  }
};
