import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import weatherRouter from './mcps/weather.js';
import hotelRouter from './mcps/hotel.js';
import translatorRouter from './mcps/translator.js';
import packingListRouter from './mcps/packing-list.js';
import activitiesRouter from './mcps/activities.js';
import transportRouter from './mcps/transport.js';
import budgetRouter from './mcps/budget.js';
import cultureRouter from './mcps/culture.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const port = 3000;

app.use(express.json());

// Serve static files from the React app
app.use(express.static(path.join(__dirname, '../frontend/dist')));

app.use('/weather', weatherRouter);
app.use('/hotel', hotelRouter);
app.use('/translator', translatorRouter);
app.use('/packing-list', packingListRouter);
app.use('/activities', activitiesRouter);
app.use('/transport', transportRouter);
app.use('/budget', budgetRouter);
app.use('/culture', cultureRouter);

// The "catchall" handler: for any request that doesn't
// match one above, send back React's index.html file.
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../frontend/dist/index.html'));
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});
