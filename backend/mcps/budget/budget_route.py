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

@router.post("/", tags=["Budget"])
async def get_budget_suggestions(data: TripRequest):
    """
    Provides mock budget suggestions.
    """
    logger.info(f"Received request for mock budget suggestions for UID: {data.uid}")

    mock_budget = {
        "budget": {
            "total": 2000,
            "currency": "USD",
            "breakdown": [
                {"category": "Flights", "amount": 800},
                {"category": "Accommodation", "amount": 600},
                {"category": "Food", "amount": 400},
                {"category": "Activities", "amount": 200}
            ]
        }
    }

    return mock_budget
