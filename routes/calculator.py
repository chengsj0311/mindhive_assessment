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
    res = calculate(req.prompt)
    return {
        "result": res
    }