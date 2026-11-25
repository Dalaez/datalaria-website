// netlify/functions/lemonsqueezy-webhook.js
// Webhook serverless coste 0 EUR (INV-MERCATOR-WH-1 / INV-PULSE-13):
// Recibe `order_created` de Lemon Squeezy, verifica firma HMAC-SHA256 (`X-Signature`),
// infiere idioma (es/en) y registra al comprador en las listas de Brevo sin registrar PII en logs.

const crypto = require('node:crypto');

const ES_COUNTRIES = new Set([
  'ES', 'MX', 'AR', 'CO', 'CL', 'PE', 'EC', 'UY', 'PY', 'BO',
  'VE', 'CR', 'PA', 'GT', 'HN', 'SV', 'NI', 'DO', 'CU', 'PR',
]);

function getHeader(headers, targetName) {
  if (!headers || typeof headers !== 'object') return '';
  const low = targetName.toLowerCase();
  for (const [k, v] of Object.entries(headers)) {
    if (String(k).toLowerCase() === low) {
      return String(v || '').trim();
    }
  }
  return '';
}

function verifyLemonSqueezySignature(rawBody, signatureHeader, secret) {
  if (!rawBody || !signatureHeader || !secret) return false;
  const expectedHex = crypto.createHmac('sha256', secret).update(rawBody, 'utf8').digest('hex');
  const providedHex = signatureHeader.trim().toLowerCase();
  if (expectedHex.length !== providedHex.length) return false;
  try {
    return crypto.timingSafeEqual(
      Buffer.from(expectedHex, 'hex'),
      Buffer.from(providedHex, 'hex'),
    );
  } catch {
    return false;
  }
}

function inferBuyerLanguage(attrs) {
  const firstItem = (attrs && attrs.first_order_item) || {};
  const productName = String(firstItem.product_name || '').toLowerCase();
  if (productName.includes('español') || productName.includes('(es)') || productName.includes('estrategia')) {
    return 'es';
  }
  if (productName.includes('(en)') || productName.includes('english')) {
    return 'en';
  }
  const billing = (attrs && attrs.billing_address) || {};
  const country = String(billing.country || attrs.country || '').trim().toUpperCase();
  if (ES_COUNTRIES.has(country)) return 'es';
  return 'en';
}

function resolveBuyersListId(lang, env) {
  const esId = Number(env.BREVO_BUYERS_LIST_ES || env.BREVO_BUYERS_LIST_ID || 0);
  const enId = Number(env.BREVO_BUYERS_LIST_EN || env.BREVO_BUYERS_LIST_ID || 0);
  const chosen = lang === 'es' ? esId : enId;
  return Number.isFinite(chosen) && chosen > 0 ? chosen : null;
}

exports.handler = async (event) => {
  if (!event || event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ success: false, error: 'Method Not Allowed' }),
    };
  }

  const webhookSecret = (process.env.LEMON_SQUEEZY_WEBHOOK_SECRET || '').trim();
  const brevoApiKey = (process.env.BREVO_API_KEY || '').trim();
  if (!webhookSecret || !brevoApiKey) {
    console.error('[ls-webhook] Missing server configuration (webhook secret or Brevo key).');
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ success: false, error: 'Server configuration missing' }),
    };
  }

  const rawBody = event.isBase64Encoded
    ? Buffer.from(event.body || '', 'base64').toString('utf8')
    : String(event.body || '');

  const signature = getHeader(event.headers, 'x-signature');
  if (!verifyLemonSqueezySignature(rawBody, signature, webhookSecret)) {
    return {
      statusCode: 401,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ success: false, error: 'Invalid signature' }),
    };
  }

  let payload;
  try {
    payload = JSON.parse(rawBody);
  } catch {
    return {
      statusCode: 400,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ success: false, error: 'Malformed JSON payload' }),
    };
  }

  const meta = (payload && payload.meta) || {};
  const eventName = String(meta.event_name || '').trim();
  if (eventName !== 'order_created') {
    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ success: true, ignored: true, reason: `event:${eventName || 'unknown'}` }),
    };
  }

  const attrs = (payload && payload.data && payload.data.attributes) || {};
  const status = String(attrs.status || '').toLowerCase();
  if (Boolean(attrs.test_mode) || Boolean(attrs.refunded) || (status && status !== 'paid' && status !== 'completed')) {
    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ success: true, ignored: true, reason: 'test_or_unpaid_order' }),
    };
  }

  const email = String(attrs.user_email || '').trim().toLowerCase();
  if (!email || !email.includes('@')) {
    return {
      statusCode: 400,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ success: false, error: 'Order missing buyer email' }),
    };
  }

  const lang = inferBuyerLanguage(attrs);
  const listId = resolveBuyersListId(lang, process.env);
  if (!listId) {
    console.error('[ls-webhook] Missing BREVO_BUYERS_LIST_ES/EN or BREVO_BUYERS_LIST_ID.');
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ success: false, error: 'Brevo buyers list not configured' }),
    };
  }

  const fullName = String(attrs.user_name || '').trim();
  const nameParts = fullName ? fullName.split(/\s+/) : [];
  const firstName = nameParts[0] || '';
  const lastName = nameParts.slice(1).join(' ') || '';
  const firstItem = attrs.first_order_item || {};
  const productName = String(firstItem.product_name || 'Datalaria Kit').trim().slice(0, 120);

  const brevoBody = {
    email,
    attributes: {
      FIRSTNAME: firstName,
      LASTNAME: lastName,
      LANGUAGE: lang,
      LAST_PRODUCT_NAME: productName,
    },
    listIds: [listId],
    updateEnabled: true,
  };

  try {
    const resp = await fetch('https://api.brevo.com/v3/contacts', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'api-key': brevoApiKey,
      },
      body: JSON.stringify(brevoBody),
    });

    if (resp.ok || resp.status === 201 || resp.status === 204) {
      // INV-PULSE-13: sin PII en logs (nunca loggear email ni nombre)
      console.info(`[ls-webhook] Synced paid order (${lang}, listId=${listId}).`);
      return {
        statusCode: 200,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ success: true, lang, listId }),
      };
    }

    const errText = await resp.text();
    console.error(`[ls-webhook] Brevo API HTTP ${resp.status}: ${errText.slice(0, 200)}`);
    return {
      statusCode: 502,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ success: false, error: 'Upstream Brevo error' }),
    };
  } catch (err) {
    console.error(`[ls-webhook] Network error calling Brevo: ${err && err.message}`);
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ success: false, error: 'Internal webhook error' }),
    };
  }
};

exports._test = {
  verifyLemonSqueezySignature,
  inferBuyerLanguage,
  resolveBuyersListId,
};
