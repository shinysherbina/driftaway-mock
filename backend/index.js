import express from 'express';
import weatherRouter from './routes/weather.js';
import hotelRouter from './routes/hotel.js';
import translatorRouter from './routes/translator.js';
import packingListRouter from './routes/packing-list.js';
import activitiesRouter from './routes/activities.js';
import transportRouter from './routes/transport.js';
import budgetRouter from './routes/budget.js';
import cultureRouter from './routes/culture.js';


const app = express();
const port = 3000;

app.use(express.json());

app.use('/weather', weatherRouter);
app.use('/hotel', hotelRouter);
app.use('/translator', translatorRouter);
app.use('/packing-list', packingListRouter);
app.use('/activities', activitiesRouter);
app.use('/transport', transportRouter);
app.use('/budget', budgetRouter);
app.use('/culture', cultureRouter);


app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});
