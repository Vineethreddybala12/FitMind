import express from 'express'
import fetch from 'node-fetch'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
const OPENAI_KEY = process.env.OPENAI_KEY || 'YOUR_OPENAI_API_KEY';

app.post('/chat', async (req, res) => {
  const userMessage = req.body.message || '';

  const systemPrompt = `You are FitMind, a friendly mental & physical wellness coach. Start with an empathetic check-in and gather mood, sleep, energy, injuries, diet constraints, available time, and goals. Follow safety rules: if signs of crisis appear, provide an empathetic safety message and encourage contacting emergency services or a mental-health professional.`;

  const payload = {
    model: 'gpt-4o-mini',
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userMessage }
    ]
  };

  try {
    const r = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${OPENAI_KEY}` },
      body: JSON.stringify(payload)
    });
    const data = await r.json();
    const reply = data.choices?.[0]?.message?.content || 'Sorry, I had an issue.';
    res.json({ reply });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'server error' });
  }
});

app.listen(3000, ()=> console.log('FitMind agent listening on http://localhost:3000'));
