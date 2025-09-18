
import admin from 'firebase-admin';

/**
 * Middleware to authenticate users via Firebase ID token.
 * Expects a Bearer token in the Authorization header.
 * Verifies the token and attaches the decoded user object to req.user.
 */
export async function authenticate(req, res, next) {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ message: 'Unauthorized: Missing or invalid Authorization header' });
  }

  const idToken = authHeader.split('Bearer ')[1];

  try {
    const decodedToken = await admin.auth().verifyIdToken(idToken);
    req.user = decodedToken;
    next();
  } catch (error) {
    console.error('Error verifying auth token:', error);
    return res.status(403).json({ message: 'Forbidden: Invalid or expired token' });
  }
}
