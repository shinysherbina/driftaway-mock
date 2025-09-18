import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
from datetime import datetime
import google.generativeai as genai
from fastmcp import FastMCP
import asyncio
import logging
import requests

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Primary Transport MCP Server 🚌")

def configure_gemini():
    """Configures the Gemini API with the key from environment variables."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)

def initialize_firebase():
    """Initializes the Firebase Admin SDK using service account key."""
    # Check if the app is already initialized to prevent errors
    if not firebase_admin._apps:
        # Path to your service account key file
        cred_path = os.path.join(os.path.dirname(__file__), '../firebase/serviceAccountKey.json')
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

def get_trip_details(uid):
    """Fetches trip details (origin, destination, date) from Firestore."""
    db = firestore.client()
    doc_ref = db.collection('trips').document(uid)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        raise Exception(f'No trip found for user ID: {uid}')

def generate_gemini_prompt(origin, destination, start_date, end_date):
    """
    Constructs a detailed prompt for Gemini to generate a mock transport ticket.
    """
    prompt = f"""
    Generate a list of long-distance transport ticket options for a round trip between '{origin["name"]}' and '{destination["name"]}'.
The onward journey is on {start_date}, and the return journey is on {end_date}.

The response must be a single, valid JSON object with the following structure. Do not include any explanatory text or markdown formatting.

Schema:
{{
  "tickets": [
    {{
      "direction": "ONWARD" | "RETURN",
      "mode": "FLIGHT" | "TRAIN" | "BUS",
      "operator": "<Operator Name>",
      "route": {{
        "from": "<Origin>",
        "to": "<Destination>",
        "departureTime": "<ISO 8601 Timestamp>",
        "arrivalTime": "<ISO 8601 Timestamp>"
      }},
      "boardingPoint": "<Nearest airport, train station, or bus terminal to origin>",
      "dropPoint": "<Nearest airport, train station, or bus terminal to destination>",
      "fare": {{
        "currency": "INR",
        "amount": <Realistic integer fare>
      }},
      "seatType": "Economy" | "Sleeper" | "AC Seater",
      "bookingUrl": "<Unique booking URL>"
    }}
  ]
}}

Instructions:
- Generate 3 to 5 realistic tickets for each direction (ONWARD and RETURN).
- Use varied transport modes and operators like "Air India", "Southern Railways", "Ola Cabs", "KSRTC".
- Ensure each ticket has a unique booking URL.
- All timestamps must be in ISO 8601 format.
- Do not wrap the JSON in markdown or code blocks.
- Fill all fields with realistic, context-appropriate data in English.
    """
    return prompt

@mcp.tool()
def get_primary_transport_options( uid: str = "shiny123") -> dict:
    """
    Main function to generate a mock long-distance transport ticket.
    Fetches data, calls Gemini, and returns the structured JSON response.
    """
    try:
        # Initialize services
        initialize_firebase()
        configure_gemini()

        trip_details = get_trip_details(uid)

        origin = trip_details.get('origin')
        destination = trip_details.get('destination')
        start_date_obj = trip_details.get('startDate')
        end_date_obj = trip_details.get('endDate')

        start_date = start_date_obj.strftime('%Y-%m-%d') if start_date_obj else datetime.now().strftime('%Y-%m-%d')
        end_date = end_date_obj.strftime('%Y-%m-%d') if end_date_obj else datetime.now().strftime('%Y-%m-%d')


        if not all([origin, destination, start_date, end_date]):
            raise ValueError("origin, destination, or travel date is missing from trip details.")

        prompt = generate_gemini_prompt(origin, destination, start_date, end_date)
        
        # --- Live Gemini API Call with Fallback ---
        try:
            logger.info("Attempting to call Gemini API...")
            model = genai.GenerativeModel('gemini-1.5-flash')
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
                ticket_data = cleaned_json
            else:
                ticket_data = json.loads(raw_text) # Fallback to original response if cleaning fails 
            # ---------------------------------

        except Exception as e:
            logger.error(f"Gemini API call failed: {e}. Falling back to mock response.")
            # Fallback to mock response if the API call fails
            ticket_data = {
                "tickets": [{
                    "direction": "ONWARD",
                    "mode": "TRAIN",
                    "operator": "Southern Railways",
                    "route": {
                        "from": origin['name'],
                        "to": destination['name'],
                        "departureTime": "2025-09-15T10:00:00+05:30",
                        "arrivalTime": "2025-09-15T14:30:00+05:30"
                    },
                    "boardingPoint": "Tambaram Railway Station",
                    "dropPoint": "Chennai Egmore Railway Station",
                    "fare": {
                        "currency": "INR",
                        "amount": 120
                    },
                    "seatType": "Sleeper",
                    "bookingUrl": "https://mocktransport.com/book?tripId=XYZ123"
                }]
            }
        # -----------------------------------------

        return ticket_data

    except Exception as e:
        logger.error(f"An error occurred in get_primary_transport_options: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    logger.info(f"🚀 MCP server started on port {os.getenv('PORT', 8082)}")
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=os.getenv("PORT", 8082),
        )
    )