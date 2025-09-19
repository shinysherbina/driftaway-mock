
from fastapi import FastAPI
from backend.routes import hotels, food, primaryTransport, localTransport, activities, weather, itinerary

app = FastAPI()

# Include routers
app.include_router(hotels.router, prefix="/api")
app.include_router(food.router, prefix="/api")
app.include_router(primaryTransport.router, prefix="/api")
app.include_router(localTransport.router, prefix="/api")
app.include_router(activities.router, prefix="/api")
app.include_router(weather.router, prefix="/api")
app.include_router(itinerary.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Driftaway FastAPI Backend"}
