
from fastapi import APIRouter, status
from serializers.receiver_serializer import receiver_serializer
from config.db import receivers_collection
from typing import Union

receiver_route = APIRouter(prefix="/receiver")

@receiver_route.post("/", status_code=status.HTTP_201_CREATED)
async def register(proposed_receiver_id: str | None = None) -> Union[dict, None]:
    if proposed_receiver_id is not None and receivers_collection.find_one({"receiver_id": proposed_receiver_id}) is None:
        
        # save receiver
        _id = receivers_collection.insert_one({
            "receiver_id": proposed_receiver_id,
            "locations": list()
        })

    else:
        _id = receivers_collection.insert_one({
            "locations": list()
        })

        # update receiver id
        receivers_collection.update_one({"_id": _id.inserted_id}, {"$set": {"receiver_id": str(_id.inserted_id)}}, True)

    receiver = receivers_collection.find_one({"_id": _id.inserted_id})
    return receiver_serializer(receiver)