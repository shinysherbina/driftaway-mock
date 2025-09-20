
from fastapi import FastAPI
from backend.mcps.hotel import hotels_route
from backend.mcps.food import food_route
from backend.mcps.primary_transport import primary_transport_route
from backend.mcps.local_transport import local_transport_route
from backend.mcps.activities import activities_route
from backend.mcps.weather import weather_route
from backend.mcps import itinerary

app = FastAPI()

# Include routers
app.include_router(hotels_route.router, prefix="/api")
app.include_router(food_route.router, prefix="/api")
app.include_router(primary_transport_route.router, prefix="/api")
app.include_router(local_transport_route.router, prefix="/api")
app.include_router(activities_route.router, prefix="/api")
app.include_router(weather_route.router, prefix="/api")
app.include_router(itinerary.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Driftaway FastAPI Backend"}
