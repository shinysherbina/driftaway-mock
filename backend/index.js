import express from 'express';
import weatherRouter from './mcps/weather.js';
import hotelRouter from './mcps/hotel.js';
import translatorRouter from './mcps/translator.js';
import packingListRouter from './mcps/packing-list.js';
import activitiesRouter from './mcps/activities.js';
import transportRouter from './mcps/transport.js';
import budgetRouter from './mcps/budget.js';
import cultureRouter from './mcps/culture.js';


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
