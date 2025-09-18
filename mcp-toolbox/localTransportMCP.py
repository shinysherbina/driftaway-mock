import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
from datetime import datetime, timedelta
import google.generativeai as genai
from fastmcp import FastMCP
import asyncio
import logging
import requests

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Local Transport MCP Server 🚍")

def configure_gemini():
    """Configures the Gemini API with the key from environment variables."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)

def initialize_firebase():
    """Initializes the Firebase Admin SDK using service account key."""
    if not firebase_admin._apps:
        cred_path = os.path.join(os.path.dirname(__file__), '../firebase/serviceAccountKey.json')
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

def get_trip_details(uid):
    """Fetches trip details from Firestore for a given user ID."""
    db = firestore.client()
    try:
        trip_ref = db.collection('trips').document(uid)
        trip_doc = trip_ref.get()
        if trip_doc.exists:
            return trip_doc.to_dict()
        else:
            logger.warning(f"No trip found for UID: {uid}")
            return None
    except Exception as e:
        logger.error(f"Error fetching trip details from Firestore: {e}")
        return None

def get_local_transport_from_gemini(destination, start_date, duration_days):
    """Calls the Gemini API to get local transport options for sightseeing."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f'''
        Generate a list of dedicated cab rental options for a trip to {destination}, starting on {start_date} and lasting {duration_days} days. 
        The user may prefer either a self-drive or chauffeur-driven vehicle—include both options if available. 
        The response should be a JSON object with a key "localTransportOptions", which is an array of objects. 
        Each object should have the following structure: - 
        "mode": "CAB", "SUV", or "VAN" - 
        "operator": A realistic rental provider name such as "Zoomcar", "Ola Rentals", "Savaari", or "DriveU" - 
        "driveType": "SELF-DRIVE" or "WITH DRIVER" - 
        "pickupLocation": A suitable pickup point like airport, railway station, or hotel area - 
        "dropLocation": Same as pickup or a flexible drop-off zone - 
        "rentalDurationDays": Integer value matching the trip duration - 
        "fare": An object with "currency" (e.g., "INR") and 
        "amount" (e.g., 4500) - 
        "bookingUrl": A realistic booking URL Ensure the options are relevant to the destination and reflect real-world availability, pricing, and operators. Prioritize full-trip rentals over point-to-point sightseeing transport. 
        
        Example: {{ "localTransportOptions": [ 
            {{  "mode": "CAB", 
                "operator": "Savaari", 
                "driveType": "WITH DRIVER", 
                "pickupLocation": "Chennai Airport", 
                "dropLocation": "Chennai Airport", 
                "rentalDurationDays": 3, 
                "fare": {{ "currency": "INR", "amount": 4800 }}, 
                "bookingUrl": "https://savaari.com/book/chennai/3day" 
            }} ] 
                }}
        '''
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        logger.info("Successfully received response from Gemini API.")

        # --- SnipSmart JSON Cleaning ---
        cleaned_json = None
        try:
            logger.info("Sending response to snipSmart for cleaning...")
            snip_smart_url = os.getenv("SNIP_SMART_URL")
            payload = {"text": raw_text}
            snip_response = requests.post(snip_smart_url, json=payload, timeout=5)

            if snip_response.status_code == 200 and snip_response.json():
                cleaned_json = snip_response.json()
                logger.info("Successfully cleaned JSON with snipSmart.")
            else:
                logger.warning(f"snipSmart returned status {snip_response.status_code}. Falling back to original response.")
        except requests.exceptions.RequestException as e:
            logger.error(f"snipSmart call failed: {e}. Falling back to original response.")

        if cleaned_json:
            return cleaned_json
        else:
            return json.loads(raw_text)
        # ---------------------------------

    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")
        return None

def get_mock_local_transport_options(destination, duration_days):
    """Returns a hardcoded mock response for local transport options."""
    return {
        "localTransportOptions": [
        {
                "mode": "SUV",
                "operator": "Zoomcar",
                "driveType": "SELF-DRIVE",
                "pickupLocation": f"{destination} Airport",
                "dropLocation": f"{destination} Airport",
                "rentalDurationDays": duration_days,
                "fare": {
                    "currency": "INR",
                    "amount": 5500
                },
                "bookingUrl": "https://mock-booking.com/zoomcar/1"
            },
            {
                "mode": "CAB",
                "operator": "Ola Rentals",
                "driveType": "WITH DRIVER",
                "pickupLocation": f"{destination} Railway Station",
                "dropLocation": f"{destination} Railway Station",
                "rentalDurationDays": duration_days,
                "fare": {
                    "currency": "INR",
                    "amount": 4200
                },
                "bookingUrl": "https://mock-booking.com/ola/2"
            },
        ]
    }

@mcp.tool()
def get_local_transport_options(uid: str) -> dict:
    """
    Main function to get local transport options, wrapped as a fastmcp tool.
    """
    try:
        logger.info(f"Received request for local transport options with uid={uid}")

        initialize_firebase()
        configure_gemini()

        trip_details = get_trip_details(uid)
        if not trip_details:
            destination = "Goa"
            start_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            duration_days = 5
        else:
            destination = trip_details.get('destination', {}).get('name', 'Unknown')
            start_date_obj = trip_details.get('startDate')
            end_date_obj = trip_details.get('endDate')

            start_date = start_date_obj.strftime('%Y-%m-%d') if start_date_obj else datetime.now().strftime('%Y-%m-%d')
            end_date = end_date_obj.strftime('%Y-%m-%d') if end_date_obj else (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
            
            # Calculate duration in days
            if start_date_obj and end_date_obj:
                duration_days = (end_date_obj - start_date_obj).days
            else:
                duration_days = 5



        transport_options = get_local_transport_from_gemini(destination, start_date, duration_days)

        if not transport_options:
            logger.warning("Falling back to mock data for local transport options.")
            transport_options = get_mock_local_transport_options(destination, duration_days)

        return transport_options

    except Exception as e:
        logger.error(f"An error occurred in get_local_transport_options: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8083))
    logger.info(f"🚀 MCP server for local transport started on port {port}")
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=port,
        )
    )