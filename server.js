require('dotenv').config();

const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// MongoDB connection
mongoose.connect(process.env.MONGODB_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
  .then(() => console.log('✅ Connected to MongoDB'))
  .catch(err => console.error('❌ MongoDB connection error:', err));

// Define Schema + Model
const ScoreSchema = new mongoose.Schema({
  score: Number,
});

const Score = mongoose.model('Score', ScoreSchema);

// Route to handle score submission
app.post('/submit-score', async (req, res) => {
  try {
    const { score } = req.body;
    if (typeof score !== 'number') {
      return res.status(400).json({ error: 'Score must be a number.' });
    }

    await Score.create({ score });

    const scores = await Score.find();
    const totalUsers = scores.length;
    const averageScore = Math.round(scores.reduce((sum, s) => sum + s.score, 0) / totalUsers);

    res.json({ averageScore, totalUsers });
  } catch (err) {
    console.error('🔥 Error in /submit-score:', err);
    res.status(500).send('Internal Server Error');
  }
});

// Default fallback
app.get('/', (req, res) => {
  res.send('Server is up. Use POST /submit-score');
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Server listening on port ${PORT}`);
});
