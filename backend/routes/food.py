
from fastapi import APIRouter, Query, HTTPException
import logging
from mcp_toolbox.foodMCP import suggest_local_cafes
from firebase.firebase_admin import get_trip_context  # Assuming a Python version of your Firebase admin setup

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.get("/food")
async def get_food_route(uid: str = Query(..., description="User ID")):
    """
    FastAPI route to get food suggestions.
    """
    logger.info(f"Received request for food with UID: {uid}")
    try:
        # 1. Fetch trip_details from Firebase
        trip_details = await get_trip_context(uid)
        if not trip_details:
            logger.warning(f"No trip details found for UID: {uid}")
            raise HTTPException(status_code=404, detail="Trip details not found for the given UID.")

        # 2. Call the MCP tool
        logger.info(f"Calling suggest_local_cafes MCP for UID: {uid}")
        food_data = suggest_local_cafes(trip_details)

        # 3. Return the MCP's response
        logger.info(f"Successfully retrieved food data for UID: {uid}")
        return food_data

    except HTTPException as http_exc:
        logger.error(f"HTTP exception for UID {uid}: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"An error occurred while fetching food for UID {uid}: {e}", exc_info=True)
        # Return a fallback JSON response
        return {
            "error": "An unexpected error occurred.",
            "details": "Could not retrieve food information at this time. Please try again later."
        }
