const test = require('node:test');
const assert = require('node:assert/strict');
const app = require('./app');
const server = app.listen(0);
test('invalid identifier returns 400', async () => {
  const address = server.address();
  const response = await fetch(`http://127.0.0.1:${address.port}/invalid-id`);
  assert.equal(response.status, 400);
});
test.after(() => server.close());
