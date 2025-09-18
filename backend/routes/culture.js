import express from 'express';

const router = express.Router();

router.get('/', (req, res) => {
  res.send('Culture data placeholder');
});

export default router;
