import firebase_admin
from firebase_admin import credentials, firestore
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT")
    if cred_path:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    else:
        logging.error("FIREBASE_SERVICE_ACCOUNT env variable not set.")
        raise RuntimeError("Missing Firebase credentials")

# Create Firestore client
db = firestore.client()

def get_trip_context(uid: str) -> dict | None:
    """Retrieves trip details for a given user ID from Firestore."""
    try:
        doc_ref = db.collection('trips').document(uid)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            logging.warning(f"No trip document found for uid: {uid}")
            return None
    except Exception as e:
        logging.error(f"Error fetching trip context for uid {uid}: {e}")
        return None

def get_field_data(uid: str, field: str) -> dict | None:
    """Retrieve field data for a given trip ID from Firestore."""
    try:
        doc_ref = db.collection('trips').document(uid)
        doc = doc_ref.get()
        if doc.exists:
            trip_data = doc.to_dict()
            logging.info(f"Fetched {field} data for trip {uid}: {trip_data}")    
            return trip_data.get(field)
        else:
            logging.warning(f"No trip document found for uid: {uid}")
            return None
    except Exception as e:
        logging.error(f"Error fetching field data for uid {uid}: {e}")
        return None

def update_field_data(uid: str, field: str, data: dict):
    """Update field data for a given trip ID in Firestore."""
    try:
        doc_ref = db.collection('trips').document(uid)
        doc_ref.update({field: data})
        logging.info(f"Successfully updated {field} for trip {uid}")
    except Exception as e:
        logging.error(f"Error updating {field} for trip {uid}: {e}")
