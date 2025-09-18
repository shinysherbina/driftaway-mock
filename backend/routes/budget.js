import express from 'express';
import { updateTripField } from '../../firebase/firebaseAdmin.js';
import { authenticate } from '../middleware/auth.js';

const router = express.Router();

/**
 * @api {post} /budget/ Update Trip Budget
 * @apiName UpdateBudget
 * @apiGroup Budget
 * @apiHeader {String} Authorization User's Firebase ID token (Bearer Token).
 *
 * @apiBody {Number} totalBudget Total trip budget.
 * @apiBody {Object} allocation Budget allocation for different categories. (e.g. hotel, primaryTransport, localTransport, food)
 * @apiBody {String} currency The currency of the budget (e.g., "INR").
 * @apiBody {Boolean} approvedByUser Whether the user has approved this budget.
 *
 * @apiSuccess {String} message Success message.
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     {
 *       "message": "Budget updated successfully for user: [uid]"
 *     }
 *
 * @apiError {String} message Error message.
 */
router.post('/', authenticate, async (req, res) => {
  const { uid } = req.user; // UID from authenticated user
  const budgetDetails = req.body;

  // Basic validation
  if (!budgetDetails || typeof budgetDetails.totalBudget !== 'number') {
    return res.status(400).json({ message: 'Missing or invalid budget details' });
  }

  try {
    // Update the 'budget' field in the user's trip document
    await updateTripField(uid, 'budget', budgetDetails);
    res.status(200).json({ message: `Budget updated successfully for user: ${uid}` });
  } catch (error) {
    console.error('Error updating budget:', error);
    res.status(500).json({ message: 'Failed to update budget' });
  }
});

export default router;