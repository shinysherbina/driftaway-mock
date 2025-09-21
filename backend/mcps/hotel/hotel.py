import os
import json
import asyncio
import logging
import requests
from typing import Dict, Any
from dotenv import load_dotenv
from fastmcp import FastMCP
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

# Initialize FastMCP
mcp = FastMCP("Hotel MCP Server 🏨")

def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)
    logger.info("Gemini API configured successfully.")

# ✅ Core logic exposed for FastAPI
def fetch_hotels(trip_details: dict) -> Dict[str, Any]:
    try:
        configure_gemini()

        location = trip_details.get('destination', {}).get('name', 'Unknown')
        guests = trip_details.get('guests', 1)
        max_budget = trip_details.get('budget', {}).get('allocation', {}).get('hotel', {}).get('amount')
        hotel_preference = trip_details.get('preferences', {}).get('hotel')
        checkin_date = trip_details.get('startDate', 'Unknown')
        checkout_date = trip_details.get('endDate', 'Unknown')

        logger.info(f"Trip details extracted: Location={location}, Budget={max_budget}, Preference={hotel_preference}, Checkin={checkin_date}, Checkout={checkout_date}")

        budget_guidance = f"Prioritize hotels with prices within a budget of {max_budget} INR. " if max_budget else "Generate varied hotel options across different price ranges. "
        preference_guidance = f"The user prefers hotels that are {hotel_preference}. " if hotel_preference else ""

        prompt = f"""
        Generate a list of hotel options for {location} for {guests} guests, checking in on {checkin_date} and checking out on {checkout_date}.
        {budget_guidance}{preference_guidance}

        The response must be a single, valid JSON object with the following structure. Do not include any explanatory text or markdown formatting.

        Schema:
        {{
        "hotels": [
            {{
            "id": "<hotel_id>",
            "name": "<hotel_name>",
            "price": <total_price_for_stay>,
            "rating": <rating_out_of_5>,
            "location": "<Area or landmark>",
            "amenities": ["<Amenity 1>", "<Amenity 2>", ...],
            "reason": "<Why it's recommended>",
            "bookingUrl": "<Direct booking URL>"
            }}
        ],
        "topPicks": [
            {{
            "id": "<hotel_id>",
            "name": "<hotel_name>",
            "reason": "<Why it's a top pick>",
            "price": <total_price_for_stay>,
            "rating": <rating_out_of_5>,
            "location": "<Area or landmark>",
            "amenities": ["<Amenity 1>", "<Amenity 2>", ...],
            "bookingUrl": "<Direct booking URL>"
            }},
            ...
        ],
        "summary": "<2–3 sentence summary of hotel options in {location}>"
        }}

        Instructions:
        - Use real hotel data available for {location}.
        - Filter or prioritize hotels based on the user's budget and preferences.
        - Include direct booking URLs where available.
        - All fields must be filled with accurate, context-appropriate information.
        - {budget_guidance}
        - {preference_guidance}
        - Ensure the JSON is well-formed and parsable.
                """

        try:
            logger.info("Sending hotel data to Gemini for enrichment.")
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            raw_text = response.text.strip()
            logger.info("Successfully received response from Gemini API.")

            cleaned_json = None
            try:
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

            enriched_data = cleaned_json if cleaned_json else json.loads(raw_text)
            return enriched_data

        except Exception as e:
            logger.error(f"Gemini enrichment failed: {e}. Falling back to mock response.")
            fallback_summary = f"Could not retrieve enriched summary for hotels in {location}. "
            if hotel_preference:
                fallback_summary += f"Considering your preference for {hotel_preference} hotels. "

            mock_hotels = [
                {"id": "H001", "name": "Luxury Grand Hotel", "price": 15000, "rating": 4.8},
                {"id": "H002", "name": "Mid-Range Comfort Inn", "price": 7000, "rating": 4.2},
                {"id": "H003", "name": "Budget Stay Lodge", "price": 3000, "rating": 3.5},
                {"id": "H004", "name": "Scenic View Resort", "price": 12000, "rating": 4.5},
                {"id": "H005", "name": "Activity Hub Hotel", "price": 8000, "rating": 4.0}
            ]

            return {
                "summary": fallback_summary,
                "topPicks": [
                    {"id": "H001", "name": "Luxury Grand Hotel", "reason": "Highest rated luxury option", "price": 15000},
                    {"id": "H002", "name": "Mid-Range Comfort Inn", "reason": "Best value for money", "price": 7000},
                    {"id": "H003", "name": "Budget Stay Lodge", "reason": "Most affordable option", "price": 3000}
                ],
                "priceRanges": {
                    "Luxury": [mock_hotels[0], mock_hotels[3]],
                    "Mid-Range": [mock_hotels[1], mock_hotels[4]],
                    "Budget": [mock_hotels[2]]
                }
            }

    except Exception as e:
        logger.error(f"An error occurred in fetch_hotels: {e}", exc_info=True)
        return {"error": "An unexpected error occurred while finding hotels."}

# ✅ FastMCP tool wrapper
@mcp.tool()
def find_hotels(trip_details: dict) -> Dict[str, Any]:
    return fetch_hotels(trip_details)

@mcp.tool()
def book_hotel(hotel_id: str, room_type: str, guests: int) -> Dict[str, Any]:
    logger.info(f"Tool 'book_hotel' called for hotel ID '{hotel_id}'")
    return {
        "hotel_id": hotel_id,
        "status": "booked",
        "confirmation_number": "123456789"
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8085))
    logger.info(f"🚀 MCP server for hotels started on port {port}")
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=port,
        )
    )