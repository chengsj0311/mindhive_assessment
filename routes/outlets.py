from fastapi import APIRouter, Query
from pydantic import BaseModel
from api.outlets import write_query, execute_query

router = APIRouter()
    
class Result(BaseModel):
    response: str

@router.get("", response_model=Result)
def query_products(query: str = Query(..., description="User question")):
    sql_query = write_query(query)
    res = execute_query(sql_query)
    return {
        "response": res["result"]
    }