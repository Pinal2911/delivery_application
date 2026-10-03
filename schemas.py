from random import randint
from pydantic import BaseModel,Field
from enum import Enum

#here at this point different model responses are created where requried model either
#imports Base Shipment model or pydanctic model based upon model response requried
def random_destination():
    return randint(11000,11999)

class ShipmentStatus(str,Enum):
    placed="placed"
    in_transit="in_transit"
    out_for_delivery="out_for_delivery"
    delivered="delivered"
    
class BaseShipment(BaseModel):
    content: str
    weight:float = Field(le=25)
    destination: int |None = None
    
class ShipmentRead(BaseShipment):
    status: ShipmentStatus
    
class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus
    
    