from fastapi import APIRouter, Query
from pydantic import BaseModel
from api.product_rag import call_rag

router = APIRouter()
    
class Result(BaseModel):
    response: str
    

@router.get("", response_model=Result)
def query_products(query: str = Query(..., description="User question")):
    res = call_rag(query)
    return {
        "response": res["response"]
    }