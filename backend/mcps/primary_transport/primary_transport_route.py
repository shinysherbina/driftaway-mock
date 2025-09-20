import logging
from fastapi import APIRouter, HTTPException, Query
from firebase.firebase_admin import get_trip_context
from primary_transport import fetch_primary_transport_options


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/primary-transport/", tags=["Transport"])
async def get_primary_transport(uid: str = Query(..., description="User ID to fetch trip details")):
    """
    Provides primary transport options based on user's trip details.
    """
    logger.info(f"Received request for primary transport options for UID: {uid}")

    try:
        # Fetch trip details from Firebase
        trip_details = get_trip_context(uid)
        if not trip_details:
            logger.warning(f"No trip details found for UID: {uid}")
            raise HTTPException(status_code=404, detail="Trip details not found for the given UID.")

        # Call the MCP to get primary transport options
        logger.info(f"Fetching primary transport options for trip: {trip_details.get('name', 'N/A')}")
        transport_data = fetch_primary_transport_options(trip_details)

        if not transport_data or "error" in transport_data:
            logger.error(f"Failed to get primary transport options for UID: {uid}. MCP returned: {transport_data.get('error', 'No data')}")
            raise HTTPException(status_code=500, detail="Failed to fetch primary transport options.")

        logger.info(f"Successfully fetched primary transport options for UID: {uid}")
        return transport_data

    except HTTPException as http_exc:
        # Re-raise HTTPException to let FastAPI handle it
        raise http_exc
    except Exception as e:
        logger.exception(f"An unexpected error occurred while fetching primary transport options for UID: {uid}")
        # Return a fallback JSON response for any other exceptions
        return {
            "error": "An unexpected error occurred.",
            "details": str(e)
        }