import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from firebase.firebase_admin import get_trip_context
from activities import fetch_activity_itinerary

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class TripRequest(BaseModel):
    uid: str
    destination: str  # Optional, if needed by fetch_activity_itinerary

@router.post("/", tags=["Activities"])
async def get_activities(data: TripRequest):
    """
    Provides activity suggestions based on user's trip details.
    """
    uid = data.uid
    logger.info(f"Received request for activity suggestions for UID: {uid}")

    try:
        trip_details = get_trip_context(uid)
        if not trip_details:
            logger.warning(f"No trip details found for UID: {uid}")
            raise HTTPException(status_code=404, detail="Trip details not found for the given UID.")

        logger.info(f"Fetching activity suggestions for trip: {trip_details.get('name', 'N/A')}")
        activity_data = fetch_activity_itinerary(trip_details)

        if not activity_data or "error" in activity_data:
            logger.error(f"Failed to get activity suggestions for UID: {uid}. MCP returned: {activity_data.get('error', 'No data')}")
            raise HTTPException(status_code=500, detail="Failed to fetch activity suggestions.")

        logger.info(f"Successfully fetched activity suggestions for UID: {uid}")
        return activity_data

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.exception(f"Unexpected error while fetching activity suggestions for UID: {uid}")
        return {
            "error": "An unexpected error occurred.",
            "details": str(e)
        }