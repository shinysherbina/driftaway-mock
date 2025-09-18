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
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

# Initialize FastMCP
mcp = FastMCP("Weather MCP Server 🌤️")

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
def get_weather_forecast(uid: str) -> Dict[str, Any]:
    """
    Retrieves the weather forecast for a user's trip destination.

    Args:
        uid: The user ID to fetch trip details from Firestore.

    Returns:
        A dictionary with the weather forecast.
    """
    logger.info(f">>> 🛠️ Tool: 'get_weather_forecast' called for UID '{uid}'")

    try:
        initialize_firebase()
        configure_gemini()
        db = firestore.client()

        # Fetch trip details from 'trips' collection
        trip_ref = db.collection('trips').document(uid)
        trip_doc = trip_ref.get()

        if not trip_doc.exists:
            logger.error(f"No trip found for UID: {uid}")
            return {"error": f"No trip found for user ID: {uid}"}

        trip_details = trip_doc.to_dict()
        
        destination = trip_details.get('destination', {}).get('name', 'Unknown')
        start_date_obj = trip_details.get('startDate')
        end_date_obj = trip_details.get('endDate')

        if not all([destination, start_date_obj, end_date_obj]):
            raise ValueError("Destination or dates are missing from trip details.")

        start_date = start_date_obj.strftime('%Y-%m-%d') if start_date_obj else datetime.now().strftime('%Y-%m-%d')
        end_date = end_date_obj.strftime('%Y-%m-%d') if end_date_obj else datetime.now().strftime('%Y-%m-%d')


        prompt = f"""
        Generate a weather forecast for {destination} from {start_date} to {end_date}.
        The response must be a single, valid JSON object with the following structure:
        {{
          "location": "<City, State or Country>",
          "forecast": [
            {{
              "date": "<YYYY-MM-DD>",
              "temperature": "<e.g., 78°F>",
              "condition": "<e.g., Sunny, Rainy, Cloudy>"
            }}
          ]
        }}
        Do not include markdown, code blocks, or explanatory text. Only return the JSON.
        """

        try:
            logger.info("Sending weather forecast request to Gemini.")
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            raw_text = response.text.strip()
            logger.info("Successfully received response from Gemini API.")

            # --- SnipSmart JSON Cleaning ---
            cleaned_json = None
            source = "Gemini"
            try:
                logger.info("Sending response to snipSmart for cleaning...")
                snip_smart_url = os.getenv("SNIP_SMART_URL")
                payload = {"text": raw_text}
                snip_response = requests.post(snip_smart_url, json=payload, timeout=5)

                if snip_response.status_code == 200 and snip_response.json():
                    cleaned_json = snip_response.json()
                    source = "snipSmart"
                    logger.info("Successfully cleaned JSON with snipSmart.")
                else:
                    logger.warning(f"snipSmart returned status {snip_response.status_code}. Falling back to original response.")
            except requests.exceptions.RequestException as e:
                logger.error(f"snipSmart call failed: {e}. Falling back to original response.")

            if cleaned_json:
                forecast_data = cleaned_json
            else:
                forecast_data = json.loads(raw_text)
            # ---------------------------------

            return forecast_data

        except Exception as e:
            logger.error(f"Gemini forecast generation failed: {e}. Falling back to mock response.")
            # Fallback mock response
            return {
                "location": destination,
                "forecast": [
                    {"date": start_date, "temperature": "75°F", "condition": "Sunny"},
                    {"date": end_date, "temperature": "70°F", "condition": "Partly Cloudy"}
                ],
                "source": "mock",
                "status": "fallback"
            }

    except Exception as e:
        logger.error(f"An error occurred in get_weather_forecast: {e}", exc_info=True)
        return {"error": "An unexpected error occurred while fetching the weather forecast."}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8089))
    logger.info(f"🚀 MCP server for weather started on port {port}")
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=port,
        )
    )
