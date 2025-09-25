
from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI()

# --- Mock Data for Kyoto ---

mock_hotel_data = {
    "hotels": [
        {
            "name": "Ryokan Genhouin",
            "rating": 4.8,
            "price_per_night": 350,
            "amenities": ["Onsen", "Kaiseki dinner", "Free Wi-Fi"],
            "booking_url": "http://example.com/ryokan-genhouin"
        },
        {
            "name": "Kyoto Grand Hotel",
            "rating": 4.5,
            "price_per_night": 250,
            "amenities": ["Pool", "Gym", "City view"],
            "booking_url": "http://example.com/kyoto-grand-hotel"
        }
    ]
}

mock_food_data = {
    "restaurants": [
        {
            "name": "Kikunoi Roan",
            "cuisine": "Kaiseki",
            "rating": 4.9,
            "price_range": "$$$$",
            "reservation_url": "http://example.com/kikunoi-roan"
        },
        {
            "name": "Ichiran Ramen",
            "cuisine": "Ramen",
            "rating": 4.6,
            "price_range": "$$",
            "reservation_url": None
        }
    ]
}

mock_activities_data = {
    "activities": [
        {
            "name": "Visit Kinkaku-ji (Golden Pavilion)",
            "category": "Sightseeing",
            "duration_hours": 2,
            "ticket_price": 400
        },
        {
            "name": "Walk through Arashiyama Bamboo Grove",
            "category": "Nature",
            "duration_hours": 1.5,
            "ticket_price": 0
        }
    ]
}

mock_transport_data = {
    "primary_transport": {
        "type": "Flight",
        "details": "Non-stop from SFO to KIX",
        "price": 1200,
        "booking_url": "http://example.com/flight-to-kix"
    },
    "local_transport": {
        "options": ["Subway", "Bus", "Taxi"],
        "recommendation": "Purchase a 2-day subway and bus pass for unlimited travel."
    }
}

mock_budget_data = {
    "budget_summary": {
        "total_estimated_cost": 4500,
        "currency": "USD",
        "breakdown": {
            "flights": 1200,
            "accommodation": 1400,
            "food": 800,
            "activities": 300,
            "local_transport": 100,
            "miscellaneous": 700
        }
    }
}

mock_chat_response = {
    "response": "Here is a summary of your trip to Kyoto. I've gathered some initial options for hotels, food, and activities based on your preferences for a cultural and relaxing experience."
}

# --- Pydantic Models (copied from main.py for compatibility) ---

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    uid: str
    destination: str
    message: str
    session_history: List[ChatMessage]

# --- Mock Endpoints ---

@app.get("/")
async def root():
    return {"message": "Driftaway MOCK Backend"}

@app.post("/chat")
async def mock_chat_endpoint(request: ChatRequest) -> Dict[str, Any]:
    """
    Mock endpoint for the chatbot. Returns a static, friendly response.
    """
    return mock_chat_response

@app.post("/api/hotel")
async def mock_hotel_mcp(uid: str = Body(..., embed=True)):
    return mock_hotel_data

@app.post("/api/food")
async def mock_food_mcp(uid: str = Body(..., embed=True)):
    return mock_food_data

@app.post("/api/activities")
async def mock_activities_mcp(uid: str = Body(..., embed=True)):
    return mock_activities_data

@app.post("/api/transport")
async def mock_transport_mcp(uid: str = Body(..., embed=True)):
    return mock_transport_data

@app.post("/api/budget")
async def mock_budget_mcp(uid: str = Body(..., embed=True)):
    return mock_budget_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
