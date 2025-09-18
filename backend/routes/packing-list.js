import express from 'express';

const router = express.Router();

router.get('/', (req, res) => {
  res.send('Packing list data placeholder');
});

export default router;
