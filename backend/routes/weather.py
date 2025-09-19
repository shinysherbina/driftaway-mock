
from fastapi import APIRouter, Query, HTTPException
import logging
from mcp_toolbox.weatherMCP import get_weather_forecast
from firebase.firebase_admin import get_trip_context  # Assuming a Python version of your Firebase admin setup

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.get("/weather")
async def get_weather_route(uid: str = Query(..., description="User ID")):
    """
    FastAPI route to get weather forecasts.
    """
    logger.info(f"Received request for weather with UID: {uid}")
    try:
        # 1. Fetch trip_details from Firebase
        trip_details = await get_trip_context(uid)
        if not trip_details:
            logger.warning(f"No trip details found for UID: {uid}")
            raise HTTPException(status_code=404, detail="Trip details not found for the given UID.")

        # 2. Call the MCP tool
        logger.info(f"Calling get_weather_forecast MCP for UID: {uid}")
        weather_data = get_weather_forecast(trip_details)

        # 3. Return the MCP's response
        logger.info(f"Successfully retrieved weather data for UID: {uid}")
        return weather_data

    except HTTPException as http_exc:
        logger.error(f"HTTP exception for UID {uid}: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"An error occurred while fetching weather for UID {uid}: {e}", exc_info=True)
        # Return a fallback JSON response
        return {
            "error": "An unexpected error occurred.",
            "details": "Could not retrieve weather information at this time. Please try again later."
        }
