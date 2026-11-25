const test = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');

const webhook = require('../../netlify/functions/lemonsqueezy-webhook.js');

function sign(body, secret) {
  return crypto.createHmac('sha256', secret).update(body, 'utf8').digest('hex');
}

test('rejects non-POST methods with 405', async () => {
  const res = await webhook.handler({ httpMethod: 'GET' });
  assert.equal(res.statusCode, 405);
});

test('fails closed with 401 when X-Signature is invalid or missing', async () => {
  process.env.LEMON_SQUEEZY_WEBHOOK_SECRET = 'super_secret_32_chars';
  process.env.BREVO_API_KEY = 'xkeysib-test';
  process.env.BREVO_BUYERS_LIST_ES = '7';
  process.env.BREVO_BUYERS_LIST_EN = '8';

  const body = JSON.stringify({ meta: { event_name: 'order_created' }, data: { attributes: {} } });
  const badRes = await webhook.handler({
    httpMethod: 'POST',
    headers: { 'x-signature': 'deadbeef' },
    body,
  });
  assert.equal(badRes.statusCode, 401);
});

test('ignores test_mode orders without calling Brevo', async () => {
  const secret = 'super_secret_32_chars';
  process.env.LEMON_SQUEEZY_WEBHOOK_SECRET = secret;
  process.env.BREVO_API_KEY = 'xkeysib-test';
  process.env.BREVO_BUYERS_LIST_ES = '7';
  process.env.BREVO_BUYERS_LIST_EN = '8';

  let called = false;
  global.fetch = async () => {
    called = true;
    return { ok: true, status: 201 };
  };

  const body = JSON.stringify({
    meta: { event_name: 'order_created' },
    data: { attributes: { status: 'paid', test_mode: true, user_email: 'buyer@example.com' } },
  });
  const res = await webhook.handler({
    httpMethod: 'POST',
    headers: { 'X-Signature': sign(body, secret) },
    body,
  });
  assert.equal(res.statusCode, 200);
  const parsed = JSON.parse(res.body);
  assert.equal(parsed.ignored, true);
  assert.equal(called, false);
});

test('routes valid paid order to correct ES/EN Brevo buyers list and strips PII from response', async () => {
  const secret = 'super_secret_32_chars';
  process.env.LEMON_SQUEEZY_WEBHOOK_SECRET = secret;
  process.env.BREVO_API_KEY = 'xkeysib-test';
  process.env.BREVO_BUYERS_LIST_ES = '7';
  process.env.BREVO_BUYERS_LIST_EN = '8';

  let sentPayload = null;
  global.fetch = async (url, opts) => {
    assert.equal(url, 'https://api.brevo.com/v3/contacts');
    sentPayload = JSON.parse(opts.body);
    return { ok: true, status: 201 };
  };

  const body = JSON.stringify({
    meta: { event_name: 'order_created' },
    data: {
      attributes: {
        status: 'paid',
        refunded: false,
        test_mode: false,
        user_email: 'Alice.Buyer@Example.com',
        user_name: 'Alice Buyer',
        billing_address: { country: 'US' },
        first_order_item: { product_name: 'Suite 01 (EN)' },
      },
    },
  });
  const res = await webhook.handler({
    httpMethod: 'POST',
    headers: { 'X-Signature': sign(body, secret) },
    body,
  });
  assert.equal(res.statusCode, 200);
  const parsed = JSON.parse(res.body);
  assert.equal(parsed.success, true);
  assert.equal(parsed.lang, 'en');
  assert.equal(parsed.listId, 8);
  assert.ok(!res.body.includes('Example.com'));
  assert.ok(!res.body.includes('Alice'));
  assert.equal(sentPayload.email, 'alice.buyer@example.com');
  assert.deepEqual(sentPayload.listIds, [8]);
  assert.equal(sentPayload.attributes.FIRSTNAME, 'Alice');
  assert.equal(sentPayload.attributes.LASTNAME, 'Buyer');
});
