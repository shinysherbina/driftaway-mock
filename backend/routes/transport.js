import express from 'express';
import { setTripContext } from '../../firebase/firebaseAdmin.js';
import { authenticate } from '../middleware/auth.js';

const router = express.Router();

/**
 * @api {post} /transport/ Update Trip Details
 * @apiName UpdateTrip
 * @apiGroup Transport
 *
 * @apiBody {String} uid User's unique ID.
 * @apiBody {Object} location Starting location object.
 * @apiBody {String} location.name Name of the location.
 * @apiBody {Number} location.lat Latitude.
 * @apiBody {Number} location.lng Longitude.
 * @apiBody {Object} destination Destination object.
 * @apiBody {String} destination.name Name of the destination.
 * @apiBody {Number} destination.lat Latitude.
 * @apiBody {Number} destination.lng Longitude.
 * @apiBody {String="TRAIN","BUS","CAR","PLANE"} preferredTransport User's preferred mode of transport.
 *
 * @apiSuccess {String} message Success message.
 *
 * @apiSuccessExample {json} Success-Response:
 *     HTTP/1.1 200 OK
 *     {
 *       "message": "Trip context updated successfully for user: [uid]"
 *     }
 *
 * @apiError {String} message Error message.
 *
 * @apiErrorExample {json} Error-Response:
 *     HTTP/1.1 400 Bad Request
 *     {
 *       "message": "Missing required fields: uid, location, destination, or preferredTransport"
 *     }
 */
router.post('/', authenticate, async (req, res) => {
  const { location, destination, preferredTransport } = req.body;
  const { uid } = req.user; // Use UID from authenticated user

  if (!uid || !location || !destination || !preferredTransport) {
    return res.status(400).json({ message: 'Missing required fields: uid, location, destination, or preferredTransport' });
  }

  try {
    const context = {
      location,
      destination,
      preferredTransport,
    };
    await setTripContext(uid, context);
    res.status(200).json({ message: `Trip context updated successfully for user: ${uid}` });
  } catch (error) {
    console.error('Error updating trip context:', error);
    res.status(500).json({ message: 'Failed to update trip context' });
  }
});

export default router;