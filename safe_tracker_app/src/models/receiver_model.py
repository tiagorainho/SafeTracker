from pydantic import BaseModel
from models.location_model import Location

class Receiver(BaseModel):
    receiver_id: str
    locations: list[Location]