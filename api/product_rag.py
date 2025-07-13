from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from typing import Optional

# constants
DEFAULT_K = 4

# initilize vector store
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector_store = FAISS.load_local(
    "zus_products_index",
    embeddings=embedding_model,
    allow_dangerous_deserialization=True
)

# initialize the chat model
model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

# define the prompt templates for rag
rag_prompt = ChatPromptTemplate.from_template(
    """You are responsible to answer the ZUS products question. Use the following context to answer the question. Be accurate and concise.

    Context:
    {context}

    Question:
    {question}
    """
)

# define the prompt template for estimating k
k_prompt = ChatPromptTemplate.from_template(
    """What is the number of items being asked for in the question: '{{question}}'? Respond with only a number. If unspecified, return {}.""".format(DEFAULT_K)
)

# estimate the number of relevant documetns (k) to retrieve
def estimate_k(question: str, default_k: int = DEFAULT_K) -> int:
    """Estimate the number of relevant documents (k) to retrieve."""
    prompt_message = k_prompt.invoke({"question": question})
    try:
        k_response = model.invoke(prompt_message).content.strip()
        return int(k_response)
    except Exception:
        return default_k  # fallback if model output is not a valid integer

# generate answer from context
def generate_answer(question: str, context: str) -> str:
    """Generate answer from context using LLM."""
    rag_message = rag_prompt.invoke({"context": context, "question": question})
    return model.invoke(rag_message).content

def call_rag(question: str) -> dict:
    """retrieves relevant docs and generates an answer."""
    k = estimate_k(question)
    docs = vector_store.similarity_search(question, k=k)
    context = "\n\n".join(doc.page_content for doc in docs)
    answer = generate_answer(question, context)
    return {"response": answer}