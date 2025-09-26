import logging
from fastapi import APIRouter
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class TripRequest(BaseModel):
    uid: str
    destination: str

@router.post("")
async def get_hotel_suggestions(data: TripRequest):
    """
    Provides mock hotel suggestions.
    """
    logger.info(f"Received request for mock hotel suggestions for UID: {data.uid}")

    mock_hotels = {
        "hotels": [
            {"name": "Hotel Ritz Paris", "price_level": "Luxury"},
            {"name": "Hôtel de Crillon", "price_level": "Luxury"},
            {"name": "The Peninsula Paris", "price_level": "Luxury"}
        ]
    }

    return mock_hotels
