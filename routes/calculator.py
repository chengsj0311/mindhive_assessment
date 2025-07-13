from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.calculator import calculate

router = APIRouter()

class Request(BaseModel):
    prompt: str

class Result(BaseModel):
    result: str

@router.post("", response_model=Result)
def chat(req: Request):
    raise HTTPException(status_code=500, detail="Simulated server error")
    res = calculate(req.prompt)
    return {
        "result": res
    }