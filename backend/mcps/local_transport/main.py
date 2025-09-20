from fastapi import FastAPI
from local_transport_route import router as local_transport_router
import uvicorn
import firebase_admin
from firebase_admin import credentials
import os
import json

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

app.include_router(local_transport_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3007)
