# 🧠 Mindhive AI Chatbot Assessment

---

## 🚀 Demo

🟢 Frontend Live Demo: https://mindhive-chatbot-frontend.vercel.app/
🟢 Backend Live Demo: https://mindhive-fastapi-app.onrender.com/

---

## 📦 Setup & Run Instructions

### 1. Clone the repo
```bash
git clone https://github.com/chengsj0311/mindhive_assessment.git
cd mindhive-assessment # if required
```

### 2. Install the dependency
```bash
python3 -m venv .venv
source .venv/bin/activate # MacOS
.\.venv\Scripts\Activate.ps1 # Windows
pip install -r requirements.txt
```

### 3. Add .env file
```bash
GOOGLE_API_KEY=xxx
API_ENDPOINT_DEV=http://127.0.0.1:8000
LANGSMITH_API_KEY=xxx # for debug and can remove the line 14 - line 15 in main if needed
```

### 3. start the backend server
```bash
uvicorn main:app --reload
```

Once running, the server are available on http://127.0.0.1:8000 locally

## Architecture used

### 1. Backend
- LangChain + LangGraph: Used to implement agentic workflows
- FastAPI: Serves as the API layer to expose endpoints (/chat, /products, /outlets, /calculator).
- FAISS Vector Store: Handles semantic search for product knowledge base (RAG).
- SQLite: Stores structured outlet data for Text2SQL queries.

### 1. Frontend
- Next.js: Deployed on Vercel, provides a simple chat interface for interacting with the bot.

## API specification

### 1. /chat
- Method: POST
- URL: https://mindhive-fastapi-app.onrender.com/chat
- Content-Type: application/json
- Request body: 
    {
        "message": string
        "session_id": string
    }
- Response body:
    {
        "response": string
    }

### 2. /calculator
- Method: POST
- URL (Local): https://mindhive-fastapi-app.onrender.com/chat
- Content-Type: application/json
- Request body: 
    {
        "prompt": string
    }
- Response body:
    {
        "result": string
    }

### 3. /products
- Method: GET
- URL: https://mindhive-fastapi-app.onrender.com/chat/products?query=<user_question>
- Content-Type: application/json
- Response body:
    {
        "response": string
    }

### 4. /outlets
- Method: GET
- URL: https://mindhive-fastapi-app.onrender.com/chat/outlets?query=<user_question>
- Content-Type: application/json
- Response body:
    {
        "response": string
    }

## Chatbot flow and trede off

### 1. The model chosen is Google Gemini 2.0 flash

### 2. Architeecture
         [ Start Node ]
               |
         [ Planner Node ]
            /       \
   [ Tool Node ]   [ Response Node ]

- Start Node: Entry point for each user message.

- Planner Node: using models to determines the intent of the user message and selects the next action:
  a. if the action for the message required by an available tools, then it would route to Tool Node
  b. if the messages received by the planner is ready to response to the user, it would route to response node

- Tool Node: Invokes external tools (e.g., calculator, product API, outlet DB) and returns results to the planner. The node used the description of the function to determine which tools to be used

- Response Node: based on the message from user or tools and using model to generate the response and it may ask follow-up question if required.

### 3. Trade-off 
- most of the node need the model to determine, thus the prompts need to be clear and well-engineered, as ambiguous or imprecise prompts can lead the model to select the wrong node

