import logging
from fastapi import APIRouter, HTTPException, Query
from firebase.firebase_admin import get_trip_context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# TODO: Implement the itinerary orchestrator that calls other MCPs to generate a full itinerary.
def generate_full_itinerary(trip_details: dict):
    """
    Placeholder function for the itinerary orchestrator.
    """
    logger.warning("Itinerary orchestrator is not implemented yet. Returning mock data.")
    return {
        "message": "Itinerary generation is not yet implemented. This is a placeholder response.",
        "trip_details": trip_details
    }

@router.get("/itinerary/", tags=["Itinerary"])
async def get_full_itinerary(uid: str = Query(..., description="User ID to fetch trip details")):
    """
    Provides a full itinerary by orchestrating other services.
    """
    logger.info(f"Received request for full itinerary for UID: {uid}")

    try:
        # Fetch trip details from Firebase
        trip_details = get_trip_context(uid)
        if not trip_details:
            logger.warning(f"No trip details found for UID: {uid}")
            raise HTTPException(status_code=404, detail="Trip details not found for the given UID.")

        # Call the placeholder orchestrator
        logger.info(f"Generating full itinerary for trip: {trip_details.get('name', 'N/A')}")
        itinerary_data = generate_full_itinerary(trip_details)

        logger.info(f"Successfully generated full itinerary for UID: {uid}")
        return itinerary_data

    except HTTPException as http_exc:
        # Re-raise HTTPException to let FastAPI handle it
        raise http_exc
    except Exception as e:
        logger.exception(f"An unexpected error occurred while generating the full itinerary for UID: {uid}")
        # Return a fallback JSON response for any other exceptions
        return {
            "error": "An unexpected error occurred.",
            "details": str(e)
        }