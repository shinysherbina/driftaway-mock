import firebase_admin
from firebase_admin import credentials, firestore
import logging

# Configure logging to see potential errors or info messages.
logging.basicConfig(level=logging.INFO)

# The Firebase Admin SDK is assumed to be initialized in the main application entry point.
# If not, you would initialize it here like this:
# if not firebase_admin._apps:
#     # Ensure the environment variable GOOGLE_APPLICATION_CREDENTIALS is set,
#     # or provide the path to your service account key directly.
#     cred = credentials.ApplicationDefault() 
#     firebase_admin.initialize_app(cred)

db = firestore.client()

def get_trip_context(uid: str) -> dict | None:
    """
    Retrieves trip details for a given user ID from Firestore.

    This function connects to the 'trips' collection and fetches the document
    whose ID matches the provided user ID.

    Args:
        uid: The user ID (which is the document ID) to fetch trip details for.

    Returns:
        A dictionary containing the trip data if the document is found.
        Returns None if the document does not exist or if an error occurs.
    """
    try:
        # Get a reference to the document in the 'trips' collection
        doc_ref = db.collection('trips').document(uid)
        
        # Retrieve the document
        doc = doc_ref.get()

        if doc.exists:
            # If the document exists, return its data as a dictionary
            return doc.to_dict()
        else:
            # If no document is found, log it and return None
            logging.info(f"No trip document found for uid: {uid}")
            return None
    except Exception as e:
        # Log any exceptions that occur during the process
        logging.error(f"An error occurred while fetching trip context for uid {uid}: {e}")
        return None