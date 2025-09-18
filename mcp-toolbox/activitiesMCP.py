import asyncio
import logging
import os
import json
from typing import Dict, Any
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import google.generativeai as genai
from fastmcp import FastMCP
import requests
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

# Initialize FastMCP
mcp = FastMCP("Activities MCP Server 🎭")

def initialize_firebase():
    """Initializes the Firebase Admin SDK, preventing re-initialization."""
    if not firebase_admin._apps:
        cred_path = os.path.join(os.path.dirname(__file__), '../firebase/serviceAccountKey.json')
        if not os.path.exists(cred_path):
            raise FileNotFoundError(f"Firebase service account key not found at {cred_path}")
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        logger.info("Firebase initialized successfully.")

def configure_gemini():
    """Configures the Gemini API with the key from environment variables."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)
    logger.info("Gemini API configured successfully.")

@mcp.tool()
def get_activity_itinerary(uid: str) -> Dict[str, Any]:
    """
    Generates a personalized activity itinerary for a user's trip.

    Args:
        uid: The user ID to fetch trip details from Firestore.

    Returns:
        A dictionary containing the activity itinerary.
    """
    logger.info(f">>> 🛠️ Tool: 'get_activity_itinerary' called for UID '{uid}'")

    try:
        initialize_firebase()
        configure_gemini()
        db = firestore.client()

        trip_ref = db.collection('trips').document(uid)
        trip_doc = trip_ref.get()

        if not trip_doc.exists:
            logger.error(f"No trip found for UID: {uid}")
            return {"error": f"No trip found for user ID: {uid}"}

        trip_details = trip_doc.to_dict()
        
        destination = trip_details.get('destination', {}).get('name', 'Unknown')
        start_date_obj = trip_details.get('startDate')
        end_date_obj = trip_details.get('endDate')
        budget = trip_details.get('budget', {}).get('allocation', {}).get('activities', {}).get('amount')
        preferences = trip_details.get('preferences', {}).get('activities')

        if not all([destination, start_date_obj, end_date_obj]):
            raise ValueError("Destination or dates are missing from trip details.")

        start_date = start_date_obj.strftime('%Y-%m-%d') if start_date_obj else datetime.now().strftime('%Y-%m-%d')
        end_date = end_date_obj.strftime('%Y-%m-%d') if end_date_obj else datetime.now().strftime('%Y-%m-%d')
        num_days = (end_date_obj - start_date_obj).days + 1

        prompt = f"""
        Generate a day-wise itinerary of activities in {destination} for a {num_days}-day trip from {start_date} to {end_date}.
        The user has a budget of {budget} for activities and prefers {preferences}.
        
        The response must be a single, valid JSON object with the following structure:
        {{
          "location": "<City, State or Country>",
          "itinerary": [
            {{
              "day": "<Day 1, Day 2, etc.>",
              "date": "<YYYY-MM-DD>",
              "activities": [
                {{
                  "id": "<unique_activity_id>",
                  "name": "<activity_name>",
                  "type": "<e.g., Museum, Park, Beach>",
                  "location": "<City>",
                  "rating": <float between 1.0 and 5.0>,
                  "reviewCount": <integer>,
                  "imageUrl": "<image URL>",
                  "tags": ["<tag1>", "<tag2>", ...],
                  "reason": "<Why it's recommended>"
                }}
              ]
            }}
          ],
          "summary": "<2–3 sentence summary of the itinerary>",
          "budgetUsed": <estimated total activity cost>,
          "preferenceMatch": "<summary of how preferences were applied>"
        }}
        Do not include markdown, code blocks, or explanatory text. Only return the JSON.
        """

        try:
            logger.info("Sending activity itinerary request to Gemini.")
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
                itinerary_data = cleaned_json
            else:
                itinerary_data = json.loads(raw_text)
            # ---------------------------------

            return itinerary_data

        except Exception as e:
            logger.error(f"Gemini itinerary generation failed: {e}. Falling back to mock response.")
            # Fallback mock response
            return {
                "location": destination,
                "itinerary": [],
                "summary": "Could not generate a personalized itinerary. Please try again.",
                "budgetUsed": 0,
                "preferenceMatch": "N/A"
            }

    except Exception as e:
        logger.error(f"An error occurred in get_activity_itinerary: {e}", exc_info=True)
        return {"error": "An unexpected error occurred while generating the itinerary."}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8081))
    logger.info(f"🚀 MCP server for activities started on port {port}")
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=port,
        )
    )
