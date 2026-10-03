from fastapi import FastAPI,HTTPException,status
from scalar_fastapi import get_scalar_api_reference
from typing import Callable,Any
from schemas import ShipmentCreate,ShipmentRead,ShipmentUpdate
from database import Database

db= Database()

app=FastAPI()


# @app.get("/shipment/latest")
# def get_latest_shipment() -> dict[str,Any]:
#     id=max(shipments.keys())
#     return shipments[id]


@app.get("/shipment",response_model=ShipmentRead)
def get_shipment_id(id:int):
    shipment=db.get(id)
    
    if shipment is None:
         raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND,
              detail="given shipment id details not found"
         )
    return shipment

@app.post("/shipment",response_model=None)
def submit_response(shipment:ShipmentCreate) -> dict[str,Any]:
    new_id=db.create(shipment)
    return {"id": new_id}

@app.patch("/shipment",response_model=ShipmentUpdate)
def update_shipment(id: int,shipment:ShipmentUpdate):
    shipment=db.update(id,shipment)
    return shipment

@app.delete("/shipment")
def delete_shipment(id:int)->dict[str,str]:
    db.delete(id)
    return {"detail":f"deleted {id}"}
    
@app.get("/scalar",include_in_schema=False)
def get_scalar_docs(): 
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )


#below api is for just reference/example, not part of application

# @app.get("/shipment/{field}")
# def get_shipment_field(field:str,id:int) -> dict[Any,Any]:
#     return {
#         field:shipments[id][field]
#     }