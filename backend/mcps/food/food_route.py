import logging
from fastapi import APIRouter, HTTPException, Query
from firebase.firebase_admin import get_trip_context
from food import fetch_local_cafes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", tags=["Food"])
async def get_food_suggestions(uid: str = Query(..., description="User ID to fetch trip details")):
    """
    Provides food suggestions based on user's trip details.
    """
    logger.info(f"Received request for food suggestions for UID: {uid}")

    try:
        # Fetch trip details from Firebase
        trip_details = get_trip_context(uid)
        if not trip_details:
            logger.warning(f"No trip details found for UID: {uid}")
            raise HTTPException(status_code=404, detail="Trip details not found for the given UID.")

        # Call the MCP to get food suggestions
        logger.info(f"Fetching food suggestions for trip: {trip_details.get('name', 'N/A')}")
        food_data = fetch_local_cafes(trip_details)


        if not food_data or "error" in food_data:
            logger.error(f"Failed to get food suggestions for UID: {uid}. MCP returned: {food_data.get('error', 'No data')}")
            raise HTTPException(status_code=500, detail="Failed to fetch food suggestions.")

        logger.info(f"Successfully fetched food suggestions for UID: {uid}")
        return food_data

    except HTTPException as http_exc:
        # Re-raise HTTPException to let FastAPI handle it
        raise http_exc
    except Exception as e:
        logger.exception(f"An unexpected error occurred while fetching food suggestions for UID: {uid}")
        # Return a fallback JSON response for any other exceptions
        return {
            "error": "An unexpected error occurred.",
            "details": str(e)
        }