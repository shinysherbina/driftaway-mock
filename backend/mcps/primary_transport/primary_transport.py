import os
import json
import asyncio
import logging
import requests
from dotenv import load_dotenv
from datetime import datetime
import google.generativeai as genai
from fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

# Initialize FastMCP
mcp = FastMCP("Primary Transport MCP Server 🚌")

def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)

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

# ✅ Core logic exposed for FastAPI
def fetch_primary_transport_options(trip_details: dict) -> dict:
    try:
        configure_gemini()

        origin = trip_details.get('origin')
        destination = trip_details.get('destination')
        start_date = trip_details.get('startDate')
        end_date = trip_details.get('endDate')

        if not all([origin, destination, start_date, end_date]):
            raise ValueError("origin, destination, or travel date is missing from trip details.")

        prompt = generate_gemini_prompt(origin, destination, start_date, end_date)

        try:
            logger.info("Attempting to call Gemini API...")
            model = genai.GenerativeModel('gemini-1.5-flash')
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

            ticket_data = cleaned_json if cleaned_json else json.loads(raw_text)

        except Exception as e:
            logger.error(f"Gemini API call failed: {e}. Falling back to mock response.")
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
                    "fare": {"currency": "INR", "amount": 120},
                    "seatType": "Sleeper",
                    "bookingUrl": "https://mocktransport.com/book?tripId=XYZ123"
                }]
            }

        return ticket_data

    except Exception as e:
        logger.error(f"An error occurred in fetch_primary_transport_options: {e}")
        return {"error": str(e)}

# ✅ FastMCP tool wrapper
@mcp.tool()
def get_primary_transport_options(trip_details: dict) -> dict:
    return fetch_primary_transport_options(trip_details)

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8082))
    logger.info(f"🚀 MCP server started on port {port}")
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=port,
        )
    )