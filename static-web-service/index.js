const express = require('express');
const path = require('path');
const app = express();
const port = 3000;

// Route to serve the HTML page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates.html'));
});

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});