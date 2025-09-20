import os
import google.generativeai as genai
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")
genai.configure(api_key=api_key)

def enrich_trip_plan(raw_mcp_data: dict, trip_details: dict) -> dict:
    """
    Enriches the raw MCP data using a Google ADK agent.

    Args:
        raw_mcp_data: A dictionary containing the raw responses from all MCPs.
        trip_details: The user's trip details.

    Returns:
        A dictionary containing the enriched trip plan.
    """
    logger.info("Starting trip plan enrichment with ADK agent.")

    try:
        # Construct a prompt for the ADK agent
        prompt = f"""
        You are a travel planning assistant. Based on the following raw data from various travel services and the user's trip details, create a comprehensive and engaging travel plan.

        User's Trip Details:
        {trip_details}

        Raw Data from Travel Services:
        {raw_mcp_data}

        Your task is to:
        1.  Create a day-by-day itinerary that combines the activities, food, and transport options.
        2.  Provide a summary of the trip, including the overall budget and weather forecast.
        3.  Offer tips and recommendations based on the user's preferences.
        4.  Ensure the final output is a single, valid JSON object.

        The response must be a single, valid JSON object with the following structure. Do not include any explanatory text or markdown formatting.

        Schema:
        {{
          "enriched_plan": {{
            "summary": "<A brief, engaging summary of the trip>",
            "daily_itinerary": [
              {{
                "day": <Day number>,
                "date": "<Date>",
                "theme": "<A theme for the day, e.g., 'Cultural Exploration'>",
                "activities": [
                  {{
                    "name": "<Activity name>",
                    "time": "<Suggested time>",
                    "details": "<Brief details>"
                  }}
                ],
                "dining_suggestions": [
                  {{
                    "name": "<Restaurant name>",
                    "meal": "<e.g., Lunch, Dinner>",
                    "details": "<Brief details>"
                  }}
                ]
              }}
            ],
            "budget_overview": {{
              "total_estimated_cost": <Total cost>,
              "breakdown": [
                {{
                  "category": "<e.g., Hotels, Food>",
                  "cost": <Cost>
                }}
              ]
            }},
            "weather_forecast": "<A summary of the weather forecast>",
            "travel_tips": [
              "<A useful travel tip>"
            ]
          }}
        }}
        """

        # Call the Gemini API to enrich the data
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        enriched_data = response.text.strip()

        logger.info("Successfully enriched trip plan with ADK agent.")
        return {"enriched_plan": enriched_data}

    except Exception as e:
        logger.error(f"An error occurred during trip plan enrichment: {e}")
        return {"error": "Failed to enrich trip plan.", "details": str(e)}
