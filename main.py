import os
import getpass
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes.rag import router as products_router
from routes.outlets import router as outlets_router
from routes.chat import router as chat_router
from routes.calculator import router as calculator_router
from dotenv import load_dotenv

load_dotenv()
os.environ["LANGSMITH_TRACING"] = "true"

if not os.environ.get("LANGSMITH_API_KEY"):
  os.environ["LANGSMITH_API_KEY"] = getpass.getpass("Enter API key for LangSmith: ")

# retrieve the API key from env, if env is not set, prompt the user
if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

app = FastAPI(title="Mindhive AI Chatbot Backend")

# enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # can be set to specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register routers
app.include_router(products_router, prefix="/products", tags=["Products RAG"])
app.include_router(outlets_router, prefix="/outlets", tags=["Outlets Text2SQL"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(calculator_router, prefix="/calculator", tags=["Calculator"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Mindhive AI Chatbot Backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)