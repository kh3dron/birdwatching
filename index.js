const express = require('express');
const axios = require('axios');
const app = express();
const port = 9550;

// Serve static files from the 'public' directory
app.use(express.static('public'));

// API endpoint to fetch image and text
app.get('/api/data', async (req, res) => {
  try {
    // Replace this with your actual API call
    const response = await axios.get('http://localhost:9111/detect');
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching data:', error);
    res.status(500).json({ error: 'Failed to fetch data' });
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
