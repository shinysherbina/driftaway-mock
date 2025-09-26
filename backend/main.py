from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any

# ONLY import the weather route for now
from mcps.weather import weather_route

# Remove other imports for now
from mcps.hotel import hotels_route
from mcps.food import food_route
from mcps.local_transport import local_transport_route
from mcps.activities import activities_route
from mcps import itinerary
from mcps.budget import budget_route
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
# ONLY include the weather router for now
app.include_router(weather_route.router, prefix="/api/weather")

# Remove other app.include_router calls for now
app.include_router(hotels_route.router, prefix="/api/hotel")
app.include_router(food_route.router, prefix="/api/food")
app.include_router(activities_route.router, prefix="/api/activities")
app.include_router(local_transport_route.router, prefix="/api/transport")
app.include_router(budget_route.router, prefix="/api/budget")
app.include_router(itinerary.router, prefix="/api/itinerary")

# --- Static Files ---
app.mount("/assets", StaticFiles(directory="static_build/assets"), name="assets")

# --- Endpoints ---
# Comment out the chat endpoint for now
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

@app.get("/{catchall:path}")
async def serve_frontend(catchall: str):
    return FileResponse("static_build/index.html")