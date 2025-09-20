from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import logging
import os
import firebase_admin
from firebase_admin import credentials
import json
from firebase_utils import get_trip_context
from adk_agent import enrich_trip_plan

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if not firebase_admin._apps:
    cred_json = os.getenv("FIREBASE_SERVICE_ACCOUNT")
    if cred_json:
        cred_dict = json.loads(cred_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    else:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred)

app = FastAPI()

class TripRequest(BaseModel):
    uid: str

# Define the MCP services and their ports
# In a real-world scenario, this would be managed by a service discovery mechanism
mcp_services = {
    "activities": "http://activities:3001",
    "food": "http://food:3004",
    "hotel": "http://hotel:3006",
    "local_transport": "http://local_transport:3007",
    "primary_transport": "http://primary_transport:3009",
    "weather": "http://weather:3011",
}

field_to_mcp_map = {
    "destination": ["weather", "activities", "hotel", "primary_transport"],
    "travel_dates": ["hotel", "primary_transport", "local_transport"],
    "budget": ["hotel", "food", "activities"],
    "preferences": ["food", "activities"],
}

# Trigger MCPs based on field change
def run_mcps_for_field(field: str, value: str, trip_details: dict) -> dict:
    triggered_mcps = field_to_mcp_map.get(field, [])
    results = {}

    for mcp_name in triggered_mcps:
        service_url = mcp_services.get(mcp_name)
        if not service_url:
            continue
        try:
            response = requests.post(f"{service_url}/", json=trip_details)
            response.raise_for_status()
            results[mcp_name] = response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to invoke {mcp_name} MCP: {e}")
            results[mcp_name] = {"error": f"Failed to invoke {mcp_name} MCP"}

    return results

@app.post("/field-update")
def field_update(payload: dict):
    field = payload.get("field")
    value = payload.get("value")
    uid = payload.get("uid")

    trip_details = get_trip_context(uid)
    if not trip_details:
        raise HTTPException(status_code=404, detail="Trip details not found.")

    updated_results = run_mcps_for_field(field, value, trip_details)
    return updated_results


@app.post("/planTrip")
async def plan_trip(request: TripRequest):
    """
    Orchestrates the trip planning process by invoking MCPs and enriching the data.
    """
    logger.info(f"Received request to plan trip for UID: {request.uid}")

    # 1. Fetch trip context from Firebase
    trip_details = get_trip_context(request.uid)
    if not trip_details:
        raise HTTPException(status_code=404, detail="Trip details not found.")

    # 2. Invoke MCPs in parallel
    raw_mcp_data = {}
    for service_name, service_url in mcp_services.items():
        try:
            # The endpoint for each MCP is assumed to be the root of the service
            # and the service expects a POST request with the trip_details
            response = requests.post(f"{service_url}/", json=trip_details)
            response.raise_for_status()  # Raise an exception for bad status codes
            raw_mcp_data[service_name] = response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to invoke {service_name} MCP: {e}")
            raw_mcp_data[service_name] = {"error": f"Failed to invoke {service_name} MCP"}

    # 3. Enrich the data with the ADK agent
    enriched_data = enrich_trip_plan(raw_mcp_data, trip_details)

    # 4. Optionally clean the output with snipSmart
    snip_smart_url = os.getenv("SNIP_SMART_URL", "http://snipsmart:5000/clean")
    try:
        response = requests.post(snip_smart_url, json=enriched_data)
        if response.status_code == 200:
            enriched_data = response.json()
            logger.info("Successfully cleaned enriched data with snipSmart.")
        else:
            logger.warning("Failed to clean enriched data with snipSmart.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to connect to snipSmart: {e}")

    # 5. Return the raw and enriched data
    return {
        "raw_mcp_data": raw_mcp_data,
        "enriched_plan": enriched_data,
    }
