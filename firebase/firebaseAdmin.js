import admin from 'firebase-admin';
import { getFirestore } from 'firebase-admin/firestore';

// Load the service account key from environment variables
const serviceAccount = process.env.FIREBASE_SERVICE_ACCOUNT;

// Initialize the Firebase Admin SDK
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

// Get a Firestore instance
const db = getFirestore();

/**
 * Retrieves the trip context document for the given user ID.
 * @param {string} uid - The user ID.
 * @returns {Promise<object|null>} The trip context data, or null if not found.
 */
export async function getTripContext(uid) {
  const docRef = db.collection('trips').doc(uid);
  const doc = await docRef.get();
  if (!doc.exists) {
    return null;
  }
  return doc.data();
}

/**
 * Sets or overwrites the trip context document for the given user ID.
 * @param {string} uid - The user ID.
 * @param {object} context - The trip context data to set.
 * @returns {Promise<void>}
 */
export async function setTripContext(uid, context) {
  const docRef = db.collection('trips').doc(uid);
  await docRef.set(context);
}

/**
 * Updates a specific field in the trip context document for the given user ID.
 * @param {string} uid - The user ID.
 * @param {string} field - The field to update.
 * @param {*} value - The new value for the field.
 * @returns {Promise<void>}
 */
export async function updateTripField(uid, field, value) {
  const docRef = db.collection('trips').doc(uid);
  await docRef.update({
    [field]: value
  });
}
