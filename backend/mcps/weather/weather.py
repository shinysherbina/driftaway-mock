import os
import json
import asyncio
import logging
import requests
from typing import Dict, Any
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

# Initialize FastMCP
mcp = FastMCP("Weather MCP Server 🌤️")

def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)
    logger.info("Gemini API configured successfully.")

def parse_date(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        return datetime.now()

# ✅ Core logic exposed for FastAPI
def fetch_weather_forecast(trip_details: dict) -> Dict[str, Any]:
    logger.info(">>> Fetching weather forecast")

    try:
        configure_gemini()

        destination = trip_details.get('destination', {}).get('name', 'Unknown')
        start_date = trip_details.get('startDate')
        end_date = trip_details.get('endDate')

        if not all([destination, start_date, end_date]):
            raise ValueError("Destination or dates are missing from trip details.")

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

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        logger.info("Successfully received response from Gemini API.")

        # --- SnipSmart JSON Cleaning ---
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

        forecast_data = cleaned_json if cleaned_json else json.loads(raw_text)
        return forecast_data

    except Exception as e:
        logger.error(f"Gemini forecast generation failed: {e}. Falling back to mock response.")
        return {
            "location": destination,
            "forecast": [
                {"date": start_date, "temperature": "75°F", "condition": "Sunny"},
                {"date": end_date, "temperature": "70°F", "condition": "Partly Cloudy"}
            ],
            "source": "mock",
            "status": "fallback"
        }

# ✅ FastMCP tool wrapper
@mcp.tool()
def get_weather_forecast(trip_details: dict) -> Dict[str, Any]:
    return fetch_weather_forecast(trip_details)

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