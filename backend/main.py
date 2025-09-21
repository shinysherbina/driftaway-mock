from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from backend.mcps.hotel import hotels_route
from backend.mcps.food import food_route
from backend.mcps.primary_transport import primary_transport_route
from backend.mcps.local_transport import local_transport_route
from backend.mcps.activities import activities_route
from backend.mcps.weather import weather_route
from backend.mcps import itinerary
from adk import adk_agent

app = FastAPI()

# --- Pydantic Models ---
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    uid: str
    destination: str
    message: str
    session_history: List[ChatMessage]

# --- Routers ---
app.include_router(hotels_route.router, prefix="/api")
app.include_router(food_route.router, prefix="/api")
app.include_router(primary_transport_route.router, prefix="/api")
app.include_router(local_transport_route.router, prefix="/api")
app.include_router(activities_route.router, prefix="/api")
app.include_router(weather_route.router, prefix="/api")
app.include_router(itinerary.router, prefix="/api")

# --- Endpoints ---
@app.get("/")
async def root():
    return {"message": "Driftaway FastAPI Backend"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest) -> Dict[str, Any]:
    """
    Endpoint to handle chatbot conversations.
    Connects to the ADK agent to get a conversational response.
    """
    try:
        # Convert Pydantic models to simple dicts for the agent
        session_history_dicts = [msg.dict() for msg in request.session_history]

        response = adk_agent.chat(
            uid=request.uid,
            destination=request.destination,
            message=request.message,
            session_history=session_history_dicts
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))