const express = require('express');
const axios = require('axios');
const rateLimit = require('express-rate-limit');
const app = express();
const port = process.env.PORT || 9550;
const fs = require('fs').promises;
const path = require('path');

// Create a rate limiter
const limiter = rateLimit({
  windowMs: 1000, // 1 second
  max: 30, // limit each IP to 5 requests per windowMs
});

// Apply rate limiter to all requests
app.use(limiter);

// Serve static files from the 'public' directory
app.use(express.static('public'));

// Fetch image and text
app.get('/api/data', async (req, res) => {
  try {
    const imagePath = path.join(__dirname, 'static', 'latest.jpg');
    const jsonPath = path.join(__dirname, 'static', 'label.json');

    const [imageBuffer, jsonData] = await Promise.all([
      fs.readFile(imagePath),
      fs.readFile(jsonPath, 'utf-8')
    ]);

    const base64Image = imageBuffer.toString('base64');
    const parsedJsonData = JSON.parse(jsonData);

    res.json({
      image: `data:image/jpeg;base64,${base64Image}`,
      ...parsedJsonData
    });
  } catch (error) {
    console.error('Error reading files:', error);
    res.status(500).json({ error: 'Failed to read data' });
  }
});

app.listen(port, () => {
  console.log(`Server running at http://0.0.0.0:${port}`);
});
