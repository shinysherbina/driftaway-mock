# from fastapi import FastAPI, HTTPException, Query, Request
# from pydantic import BaseModel
# import requests
# import logging
# import os
# import json
# import firebase_admin
# from firebase_admin import credentials
# from firebase_utils import get_trip_context
# from adk_agent import chat  # renamed enrichment function
# from cache_utils import get_cached_response, set_cached_response
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Logging setup
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Firebase initialization
# if not firebase_admin._apps:
#     cred_json = os.getenv("FIREBASE_SERVICE_ACCOUNT")
#     if cred_json:
#         cred_dict = json.loads(cred_json)
#         cred = credentials.Certificate(cred_dict)
#     else:
#         cred = credentials.ApplicationDefault()
#     firebase_admin.initialize_app(cred)

# # MCP service registry
# mcp_services = {
#     "activities": "http://activities:3001",
#     "food": "http://food:3004",
#     "hotel": "http://hotel:3006",
#     "local_transport": "http://local_transport:3007",
#     "primary_transport": "http://primary_transport:3009",
#     "weather": "http://weather:3011",
# }

# field_to_mcp_map = {
#     "destination": ["weather", "activities", "hotel", "primary_transport"],
#     "travel_dates": ["hotel", "primary_transport", "local_transport"],
#     "budget": ["hotel", "food", "activities"],
#     "preferences": ["food", "activities"],
# }

# class TripRequest(BaseModel):
#     uid: str

# def run_mcps_for_field(field: str, value: str, trip_details: dict, force_enrich: bool = False) -> dict:
#     """Trigger relevant MCPs based on a field update."""
#     triggered_mcps = field_to_mcp_map.get(field, [])
#     results = {}

#     for mcp_name in triggered_mcps:
#         if not force_enrich:
#             cached = get_cached_response(mcp_name, trip_details)
#             if cached:
#                 logger.info(f"Cache hit for {mcp_name}")
#                 results[mcp_name] = cached
#                 continue

#         service_url = mcp_services.get(mcp_name)
#         if not service_url:
#             logger.warning(f"No service URL for MCP: {mcp_name}")
#             continue

#         try:
#             response = requests.post(f"{service_url}/", json=trip_details)
#             response.raise_for_status()
#             mcp_response = response.json()
#             set_cached_response(mcp_name, trip_details, mcp_response)
#             results[mcp_name] = mcp_response
#         except requests.exceptions.RequestException as e:
#             logger.error(f"Failed to invoke {mcp_name}: {e}")
#             results[mcp_name] = {"error": f"Failed to invoke {mcp_name}"}

#     return results


# @app.post("/chat")
# async def handle_chat(request: Request):
#     """Handles conversational chat with Gemini."""
#     body = await request.json()
#     uid = body["uid"]
#     destination = body["destination"]
#     message = body["message"]
#     session_history = body["session_history"]

#     response = chat(uid, destination, message, session_history)
#     return response


# @app.post("/field-update")
# def field_update(payload: dict, force_enrich: bool = Query(False)):
#     """Handles field updates and triggers relevant MCPs."""
#     field = payload.get("field")
#     value = payload.get("value")
#     uid = payload.get("uid")

#     trip_details = get_trip_context(uid)
#     if not trip_details:
#         raise HTTPException(status_code=404, detail="Trip details not found.")

#     return run_mcps_for_field(field, value, trip_details, force_enrich)

# @app.post("/mcp/{mcp_name}")
# async def run_single_mcp(mcp_name: str, request: Request):
#     """Invokes a single MCP by name."""
#     if mcp_name not in mcp_services:
#         raise HTTPException(status_code=404, detail="MCP not found")

#     trip_details = await request.json()
#     service_url = mcp_services[mcp_name]

#     try:
#         uid = trip_details.get("uid")
#         response = requests.post(f"{service_url}/?uid={uid}", json=trip_details)
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         logger.error(f"Failed to invoke {mcp_name}: {e}")
#         raise HTTPException(status_code=500, detail=f"Failed to invoke {mcp_name}")

# @app.post("/planTrip")
# async def plan_trip(request: TripRequest):
#     """Orchestrates trip planning by invoking MCPs and returning raw data."""
#     logger.info(f"Planning trip for UID: {request.uid}")
#     trip_details = get_trip_context(request.uid)
#     if not trip_details:
#         raise HTTPException(status_code=404, detail="Trip details not found.")

#     raw_mcp_data = {}
#     for service_name, service_url in mcp_services.items():
#         cached = get_cached_response(service_name, trip_details)
#         if cached:
#             logger.info(f"Cache hit for {service_name}")
#             raw_mcp_data[service_name] = cached
#             continue

#         try:
#             response = requests.post(f"{service_url}/", json=trip_details)
#             response.raise_for_status()
#             mcp_response = response.json()
#             set_cached_response(service_name, trip_details, mcp_response)
#             raw_mcp_data[service_name] = mcp_response
#         except requests.exceptions.RequestException as e:
#             logger.error(f"Failed to invoke {service_name}: {e}")
#             raw_mcp_data[service_name] = {"error": f"Failed to invoke {service_name}"}

#     return {
#         "raw_mcp_data": raw_mcp_data
#     }
