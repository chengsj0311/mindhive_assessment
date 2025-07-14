import re
import httpx
import os
from langchain_core.tools import tool
import requests

api_endpoint = os.getenv("API_ENDPOINT_DEV")
client = httpx.Client(base_url=api_endpoint)

def calculator(text: str) -> str:
    """
    Use this tool to perform arithmetic calculations. 
    Input should involve a mathematical expression like '2 + 2' or '5 * 3'.
    """
    payload = {"prompt": text}
    try:
        response = client.post('/calculator', json=payload)
        response.raise_for_status()

        result = response.json().get("result", "")
        return result or "No result returned from the calculator."

    except httpx.HTTPStatusError as http_err:
        return f"HTTP error {http_err.response.status_code}: {http_err.response.text}"
    except httpx.RequestError:
        return "Calculator service is currently unavailable. Please try again later."
    except Exception as e:
        return f"Unexpected error: {str(e)}"


def rag_products(text: str) -> str:
    """
    Use this tool to query products from the RAG system.
    """
    payload = {"query": text}
    try:
        response = client.get('products', params=payload)
        response.raise_for_status()
        
        result = response.json().get("response", "")
        return result or "Sorry, no relevant product information was found."
    except httpx.HTTPStatusError as http_err:
        return f"HTTP error {http_err.response.status_code}: {http_err.response.text}"
    except httpx.RequestError:
        return "Calculator service is currently unavailable. Please try again later."
    except Exception as e:
        return f"Unexpected error: {str(e)}"
    
def outlets_text2sql(text: str) -> str:
    """
    Use this tool to query ZUS coffee outlets using text-to-SQL.
    """
    payload = {"query": text}
    try:
        response = client.get('outlets', params=payload)
        response.raise_for_status()

        result = response.json().get("response", "")
        return result or "No outlets found for your query."
    
    except httpx.HTTPStatusError as http_err:
        return f"HTTP error {http_err.response.status_code}: {http_err.response.text}"
    except httpx.RequestError:
        return "Calculator service is currently unavailable. Please try again later."
    except Exception as e:
        return f"Unexpected error: {str(e)}"