const express = require('express');
const { MongoClient } = require('mongodb');
const app = express();
const uri = process.env.MONGO_URI || 'mongodb://localhost:27017/bank_app';
const client = new MongoClient(uri);
app.get('/health', (_req, res) => res.json({ status: 'ok', service: 'transactions' }));
app.get('/:email', async (req, res) => {
  const email = req.params.email;
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return res.status(400).json({ error: 'Invalid email' });
  try {
    const rows = await client.db('bank_app').collection('transactions')
      .find({ email: email.toLowerCase() }, { projection: { _id: 0 } })
      .sort({ created_at: -1 }).limit(50).toArray();
    return res.json({ email: email.toLowerCase(), transactions: rows });
  } catch (_err) { return res.status(503).json({ error: 'Database unavailable' }); }
});
if (require.main === module) app.listen(3000, '0.0.0.0', () => console.log('Transactions listening on 3000'));
module.exports = app;
