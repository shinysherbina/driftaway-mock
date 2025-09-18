import express from 'express';

const router = express.Router();

router.get('/', (req, res) => {
  res.send('Translator data placeholder');
});

export default router;
