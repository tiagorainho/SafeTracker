from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.location_routes import location_route
from routes.receiver_routes import receiver_route
from routes.beacons_routes import beacon_route

app = FastAPI()

# CORS configuration
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(location_route)
app.include_router(receiver_route)
app.include_router(beacon_route)


@app.get("/health")
async def health():
    return {"status": "OK"}