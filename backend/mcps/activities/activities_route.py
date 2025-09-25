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

@router.post("/", tags=["Activities"])
async def get_activities(data: TripRequest):
    """
    Provides mock activity suggestions.
    """
    logger.info(f"Received request for mock activity suggestions for UID: {data.uid}")

    mock_activities = {
        "activities": [
            {"day": 1, "description": "Visit the Louvre Museum and see the Mona Lisa."},
            {"day": 2, "description": "Explore the Eiffel Tower and have a picnic on the Champ de Mars."},
            {"day": 3, "description": "Take a stroll along the Seine River and enjoy a boat tour."}
        ]
    }

    return mock_activities