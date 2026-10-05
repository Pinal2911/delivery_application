from pydantic import Field
from sqlmodel import SQLModel
from enum import Enum
from datetime import datetime

class ShipmentStatus(str,Enum):
    placed="placed"
    in_transit="in_transit"
    out_for_delivery="out_for_delivery"
    delivered="delivered"
    
class Shipment(SQLModel,table=True):
    __tablename__="Shipment"
    id:int=Field(primary_key=True)
    content:str
    weight:float=Field(le=25)
    destination:str
    status:ShipmentStatus
    estimated_delivery=datetime