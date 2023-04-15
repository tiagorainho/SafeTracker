
from fastapi import APIRouter, status, Response
from models.receiver_model import Receiver
from models.signal_model import Signal
from models.location_model import Location
from serializers.location_serializer import location_serializer, locations_serializer
from config.db import receivers_collection
from bson.objectid import ObjectId

location_route = APIRouter(prefix="/location")


@location_route.post("/register/{receiver_id}", status_code=status.HTTP_201_CREATED)
async def register(receiver_id: str, signals: list[Signal], response: Response) -> Location | None:
    collection = database.receiver
    receiver = collection.find_one({"_id": receiver_id})

    if receiver is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    new_location = []
    
    res = collection.update_one(filter={"_id": receiver_id}, update={"locations": new_location})

    return {"status": "Ok","data": res}
