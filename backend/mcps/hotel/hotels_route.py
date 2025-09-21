import logging
from fastapi import APIRouter, HTTPException, Query
from firebase.firebase_admin import get_trip_context
from hotel import fetch_hotels

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", tags=["Hotels"])
async def get_hotel_suggestions(uid: str = Query(..., description="User ID to fetch trip details")):
    """
    Provides hotel suggestions based on user's trip details.
    """
    logger.info(f"Received request for hotel suggestions for UID: {uid}")

    try:
        # Fetch trip details from Firebase
        trip_details = get_trip_context(uid)
        if not trip_details:
            logger.warning(f"No trip details found for UID: {uid}")
            raise HTTPException(status_code=404, detail="Trip details not found for the given UID.")

        # Call the MCP to get hotel suggestions
        logger.info(f"Fetching hotel suggestions for trip: {trip_details.get('name', 'N/A')}")
        hotel_data = fetch_hotels(trip_details)

        if not hotel_data or "error" in hotel_data:
            logger.error(f"Failed to get hotel suggestions for UID: {uid}. MCP returned: {hotel_data.get('error', 'No data')}")
            raise HTTPException(status_code=500, detail="Failed to fetch hotel suggestions.")

        logger.info(f"Successfully fetched hotel suggestions for UID: {uid}")
        return hotel_data

    except HTTPException as http_exc:
        # Re-raise HTTPException to let FastAPI handle it
        raise http_exc
    except Exception as e:
        logger.exception(f"An unexpected error occurred while fetching hotel suggestions for UID: {uid}")
        # Return a fallback JSON response for any other exceptions
        return {
            "error": "An unexpected error occurred.",
            "details": str(e)
        }