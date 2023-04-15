
from fastapi import APIRouter, status
from serializers.receiver_serializer import receiver_serializer
from config.db import beacons_collection
from typing import Union
from models.beacons_model import Beacon

beacon_route = APIRouter(prefix="/beacon")

@beacon_route.post("/", status_code=status.HTTP_201_CREATED)
async def register(beacon: Beacon) -> Union[dict, None]:
    _id = beacons_collection.insert_one(beacon)

    return receiver_serializer(beacons_collection.find_one({"_id": _id.inserted_id}))