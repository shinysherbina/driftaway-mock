import asyncio
import logging
import os
import json
from typing import Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai
from fastmcp import FastMCP
import requests

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

# Initialize FastMCP
mcp = FastMCP("Food MCP Server 🍽️")


def configure_gemini():
    """Configures the Gemini API with the key from environment variables."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)
    logger.info("Gemini API configured successfully.")

@mcp.tool()
def suggest_local_cafes(trip_details: dict) -> Dict[str, Any]:
    """
    Suggests local cafes based on user's trip details, preferences, and budget.

    Args:
        trip_details: trip details object containing the required fields.

    Returns:
        A dictionary containing suggested cafes or a fallback mock response.
    """
    logger.info(f"Tool 'suggest_local_cafes' called")

    try:
        configure_gemini()
        
        # Extract relevant information from trip details
        city = trip_details.get('destination', {}).get('name', 'Unknown')
        food_preference = trip_details.get('preferences', {}).get('food')
        max_budget_per_meal = trip_details.get('budget', {}).get('allocation', {}).get('food', {}).get('amount')
        guests = trip_details.get('guests', 1) # Default to 1 guest if not specified

        logger.info(f"Trip details extracted: City={city}, Preference={food_preference}, Budget={max_budget_per_meal}, Guests={guests}")

        # Construct Gemini prompt
        budget_guidance = ""
        if max_budget_per_meal:
            budget_guidance = f"Prioritize cafes where the average meal cost per person is around {max_budget_per_meal} INR. "
        else:
            budget_guidance = "Include cafes across various price ranges. "

        preference_guidance = ""
        if food_preference:
            preference_guidance = f"Focus on cafes offering {food_preference} cuisine. "

        prompt = f"""
        Suggest 5 to 7 cafes in {city} for {guests} people.
        {preference_guidance}{budget_guidance}
        For each cafe, include its name, cuisine, price range , rating (out of 5), location, and a brief reason for recommendation.
        Include actual booking or location URLs from known platforms (e.g., Zomato, TripAdvisor, Google Maps).

        Return a single, valid JSON object with the following structure. Do not include any text outside the JSON.
        {{
          "cafes": [
            {{
              "name": "<Cafe Name>",
              "cuisine": "<Cuisine Type>",
              "priceRange": <avg price per person for a meal>,
              "rating": <Rating out of 5 (float)>,
              "location": "<Address or Landmark>",
              "reason": "<Brief reason for recommendation>",
              "url": "<Booking or Location URL>"
            }}
          ],
          "topPicks": [
            {{"name": "<Cafe Name>", "reason": "<Why it's a top pick>"}},
            {{"name": "<Cafe Name>", "reason": "<Why it's a top pick>"}},
            {{"name": "<Cafe Name>", "reason": "<Why it's a top pick>"}}
          ],
          "summary": "<Short description of the food scene in {city}>"
        }}
        Cafe suggestions must be based on real, up-to-date internet data.
        """

        try:
            logger.info("Sending cafe suggestion request to Gemini.")
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
                suggested_cafes = cleaned_json
            else:
                suggested_cafes = json.loads(raw_text)
            # ---------------------------------
            
            logger.info("Successfully received cafe suggestions from Gemini.")
            return suggested_cafes

        except Exception as e:
            logger.error(f"Gemini cafe suggestion failed: {e}. Falling back to mock response.")
            # Fallback mock response
            fallback_summary = f"Explore the diverse food scene in {city}. "
            if food_preference:
                fallback_summary += f"You might enjoy {food_preference} options. "
            
            mock_cafes = [
                {
                    "name": "The Daily Grind",
                    "cuisine": "Continental",
                    "priceRange": "$",
                    "rating": 4.2,
                    "location": "City Center",
                    "reason": "Great for a quick coffee and light bites.",
                    "url": "https://www.mockdata.com/maps/search/The+Daily+Grind"
                },
                {
                    "name": "Spice Route Cafe",
                    "cuisine": "Indian",
                    "priceRange": "$",
                    "rating": 4.5,
                    "location": "Old Town",
                    "reason": "Authentic local flavors in a cozy setting.",
                    "url": "https://www.mockdata.com/spice-route-cafe"
                },
                {
                    "name": "Green Leaf Bistro",
                    "cuisine": "Healthy",
                    "priceRange": "$",
                    "rating": 4.0,
                    "location": "Near Park",
                    "reason": "Fresh salads and organic options.",
                    "url": "https://www.mockdata.com/GreenLeafBistro"
                },
                {
                    "name": "Cafe Amore",
                    "cuisine": "Italian",
                    "priceRange": "$$",
                    "rating": 4.7,
                    "location": "Riverside",
                    "reason": "Romantic ambiance with delicious pasta.",
                    "url": "https://www.mockdata.com/maps/search/Cafe+Amore"
                }
            ]

            mock_response = {
                "cafes": mock_cafes,
                "topPicks": [
                    {"name": "Spice Route Cafe", "reason": "Highly recommended for local cuisine."},
                    {"name": "The Daily Grind", "reason": "Popular spot for breakfast and coffee."},
                    {"name": "Cafe Amore", "reason": "Perfect for a special evening out."}
                ],
                "summary": fallback_summary
            }
            return mock_response

    except Exception as e:
        logger.error(f"An error occurred in suggest_local_cafes: {e}", exc_info=True)
        return {"error": "An unexpected error occurred while suggesting cafes."}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8086)) # Using a new port for Food MCP
    logger.info(f"🚀 MCP server for food started on port {port}")
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=port,
        )
    )
