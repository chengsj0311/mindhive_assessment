import re
import httpx
import os
from langchain_core.tools import tool

api_endpoint = os.getenv("API_ENDPOINT_DEV")
client = httpx.Client(base_url=api_endpoint)

def calculator(text: str) -> str:
    """
    Use this tool to perform arithmetic calculations. 
    Input should involve a mathematical expression like '2 + 2' or '5 * 3'."
    """
    payload = {"prompt": text}
    try:
        response = client.post('calculator', json=payload)
        result = response.json().get("result", "")
        return result
    except Exception as e:
        return "cal"

def rag_products(text: str) -> str:
    """
    Use this tool to query products from the RAG system.
    """
    payload = {"query": text}
    try:
        response = client.get('products', params=payload)
        result = response.json().get("response", "")
        return result
    except Exception as e:
        return "error"
    
def outlets_text2sql(text: str) -> str:
    """
    Use this tool to query outlets using text-to-SQL.
    """
    payload = {"query": text}
    try:
        response = client.get('outlets', params=payload)
        result = response.json().get("response", "")
        return result
    except Exception as e:
        return "error"