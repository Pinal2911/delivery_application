from fastapi import FastAPI,HTTPException,status
from scalar_fastapi import get_scalar_api_reference
from typing import Callable,Any

shipments = {
    12701 : {
        "weight": .6,
        "content":"glassware",
        "status":"placed"
    },
    12702 : {
        "weight": 1.2,
        "content":"books",
        "status":"in transit"
    },
    12703 : {
        "weight": 2.5,
        "content":"furniture",
        "status":"delivered"
    },
    12704 : {
        "weight": 0.8,
        "content":"electronics",
        "status":"packed"
    },
    12705 : {
        "weight": 3.1,
        "content":"appliances",
        "status":"out for delivery"
    },
    12706 : {
        "weight": 0.4,
        "content":"clothing",
        "status":"placed"
    },
}
app=FastAPI()

@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str,Any]:
    id=max(shipments.keys())
    return shipments[id]


@app.get("/shipment")
def get_shipment_id(id:int | None=None)->dict[str,Any]:
    # if not id:
    #         id=max(shipments.keys())
    #         return shipments[id]
    if id not in shipments:
         raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND,
              detail="given shipment id details not found"
         )
    return shipments[id]

@app.post("/shipment")
def submit_response(data: dict[str,Any]) -> dict[str,Any]:
    content = data["content"]
    weight = data["weight"]

    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="weight > 25"
        ) 
    new_id = max(shipments.keys())+1
    shipments[new_id]={
        "weight":weight,
        "content":content,
        "status":"placed"
    }
    return {"id": new_id}

@app.get("/scalar",include_in_schema=False)
def get_scalar_docs(): 
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )


#below api is for just reference/example, not part of application

@app.get("/shipment/{field}")
def get_shipment_field(field:str,id:int) -> dict[str,Any]:
    return {
        field:shipments[id][field]
    }