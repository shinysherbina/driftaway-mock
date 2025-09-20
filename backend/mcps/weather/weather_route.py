import logging
from fastapi import APIRouter, HTTPException, Query
from firebase.firebase_admin import get_trip_context
from weather import fetch_weather_forecast


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/weather/", tags=["Weather"])
async def get_weather(uid: str = Query(..., description="User ID to fetch trip details")):
    """
    Provides weather forecast based on user's trip details.
    """
    logger.info(f"Received request for weather forecast for UID: {uid}")

    try:
        # Fetch trip details from Firebase
        trip_details = get_trip_context(uid)
        if not trip_details:
            logger.warning(f"No trip details found for UID: {uid}")
            raise HTTPException(status_code=404, detail="Trip details not found for the given UID.")

        # Call the MCP to get weather forecast
        logger.info(f"Fetching weather forecast for trip: {trip_details.get('name', 'N/A')}")
        weather_data = fetch_weather_forecast(trip_details)


        if not weather_data or "error" in weather_data:
            logger.error(f"Failed to get weather forecast for UID: {uid}. MCP returned: {weather_data.get('error', 'No data')}")
            raise HTTPException(status_code=500, detail="Failed to fetch weather forecast.")

        logger.info(f"Successfully fetched weather forecast for UID: {uid}")
        return weather_data

    except HTTPException as http_exc:
        # Re-raise HTTPException to let FastAPI handle it
        raise http_exc
    except Exception as e:
        logger.exception(f"An unexpected error occurred while fetching weather forecast for UID: {uid}")
        # Return a fallback JSON response for any other exceptions
        return {
            "error": "An unexpected error occurred.",
            "details": str(e)
        }