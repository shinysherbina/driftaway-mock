
from fastapi import APIRouter, Query, HTTPException
import logging
# from mcp_toolbox.itinerary_orchestrator import generate_full_itinerary  # To be created
from firebase.firebase_admin import get_trip_context  # Assuming a Python version of your Firebase admin setup

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.get("/itinerary")
async def get_itinerary_route(uid: str = Query(..., description="User ID")):
    """
    FastAPI route to get the full itinerary.
    """
    logger.info(f"Received request for itinerary with UID: {uid}")
    try:
        # 1. Fetch trip_details from Firebase
        trip_details = await get_trip_context(uid)
        if not trip_details:
            logger.warning(f"No trip details found for UID: {uid}")
            raise HTTPException(status_code=404, detail="Trip details not found for the given UID.")

        # 2. Call the Itinerary Orchestrator (to be created)
        # logger.info(f"Calling generate_full_itinerary MCP for UID: {uid}")
        # itinerary_data = generate_full_itinerary(trip_details)

        # 3. Return the MCP's response
        # logger.info(f"Successfully retrieved itinerary data for UID: {uid}")
        # return itinerary_data

        # Placeholder response
        return {"message": "Itinerary generation is not yet implemented."}

    except HTTPException as http_exc:
        logger.error(f"HTTP exception for UID {uid}: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"An error occurred while fetching itinerary for UID {uid}: {e}", exc_info=True)
        # Return a fallback JSON response
        return {
            "error": "An unexpected error occurred.",
            "details": "Could not retrieve itinerary information at this time. Please try again later."
        }
