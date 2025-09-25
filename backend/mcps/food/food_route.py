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

@router.post("/", tags=["Food"])
async def get_food_suggestions(data: TripRequest):
    """
    Provides mock food suggestions.
    """
    logger.info(f"Received request for mock food suggestions for UID: {data.uid}")

    mock_food = {
        "restaurants": [
            {"name": "Le Procope", "cuisine": "French"},
            {"name": "L'Ambroisie", "cuisine": "Haute Cuisine"},
            {"name": "Breizh Café", "cuisine": "Crêperie"}
        ]
    }

    return mock_food
