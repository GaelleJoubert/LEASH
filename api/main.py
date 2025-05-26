from typing import List, Union
from fastapi import HTTPException
from fastapi import FastAPI
from models.webbing import Webbing, StretchCurve
from models.model_exception import WebbingException, StretchCurveException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

# Pydantic models for request validation

class WeightCalculationResponse(BaseModel):
    webbing_name: str
    length: float
    linear_weight: float
    total_weight: float
    unit: str



    
# FastAPI endpoint
async def calculate_weight_endpoint(webbing:Webbing, length : float) -> WeightCalculationResponse:
    """
    FastAPI endpoint to calculate webbing weight from JSON data
    """
    
    try:
        result = webbing.calculate_webbing_weight( length)
        return WeightCalculationResponse(**result)
        
    except WebbingException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/webbing/calculate-weight/{length}", response_model=WeightCalculationResponse)
async def calculate_webbing_total_weight(length:float, name:str, linear_weight:float, stretches: list[float],  forces: list[float]   ):
    webbing = Webbing(name=name, stretches=stretches, forces=forces, linear_weight=linear_weight)
    return await calculate_weight_endpoint(webbing,length )
