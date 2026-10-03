from fastapi import FastAPI,HTTPException,status
from scalar_fastapi import get_scalar_api_reference
from typing import Callable,Any
from schemas import ShipmentCreate,ShipmentRead,ShipmentUpdate
from database import shipments,save

app=FastAPI()


@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str,Any]:
    id=max(shipments.keys())
    return shipments[id]


@app.get("/shipment",response_model=ShipmentRead)
def get_shipment_id(id:int):
    # if not id:
    #         id=max(shipments.keys())
    #         return shipments[id]
    if id not in shipments:
         raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND,
              detail="given shipment id details not found"
         )
    return shipments[id]

@app.post("/shipment",response_model=None)
def submit_response(shipment:ShipmentCreate) -> dict[str,Any]:
    # content = data["content"]
    # weight = data["weight"]
    #below validation not required after pydanctic validation
    # if weight > 25:
    #     raise HTTPException(
    #         status_code=status.HTTP_406_NOT_ACCEPTABLE,
    #         detail="weight > 25"
    #     ) 
    new_id = max(shipments.keys())+1
    shipments[new_id]={
        **shipment.model_dump(),
        "status":"placed"
    }
    save()
    return {"id": new_id}

@app.patch("/shipment",response_model=ShipmentUpdate)
def update_shipment(id: int,body:dict[str,ShipmentUpdate]):
    shipments[id].update(body)
    save()
    return shipments[id]

@app.delete("/shipment")
def delete_shipment(id:int)->dict[str,str]:
    shipments.pop(id)
    return{
        "detail":f"shipment with {id} deleted"
    }
@app.get("/scalar",include_in_schema=False)
def get_scalar_docs(): 
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )


#below api is for just reference/example, not part of application

@app.get("/shipment/{field}")
def get_shipment_field(field:str,id:int) -> dict[Any,Any]:
    return {
        field:shipments[id][field]
    }