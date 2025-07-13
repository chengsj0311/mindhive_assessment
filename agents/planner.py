from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import trim_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START
from langchain.chat_models import init_chat_model
from tool import calculator, rag_products, outlets_text2sql
from typing_extensions import TypedDict, Annotated, Any
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing import List
from agents.prompt_template import planner_agent_prompt_template, response_agent_prompt_template
from langgraph.prebuilt import ToolNode

# Define the state schema for the workflow
class State(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]

# initialize the chat model
model = init_chat_model("gemini-2.0-flash", model_provider="google_genai").bind(tools=[calculator, rag_products, outlets_text2sql])

# Define tool node
tool_nodes = ToolNode([calculator, rag_products, outlets_text2sql])

# setup trimmer
trimmer = trim_messages(
  strategy="last",
  max_tokens=20,
  token_counter=len,
  include_system=True,
  start_on="human",
  end_on=("human", "tool"),
  allow_partial=True
)

# call the planner agnet
def call_planner(state: State):
    trimmed_messages = trimmer.invoke(state["messages"])
    prompt = planner_agent_prompt_template.invoke({"messages": trimmed_messages})
    response = model.invoke(prompt)
    
    return {"messages": response}

# direct response without calling tools
def call_response(state: State):
    trimmed_messages = trimmer.invoke(state["messages"])
    prompt = response_agent_prompt_template.invoke({"messages": trimmed_messages})
    response = model.invoke(prompt)
    
    return {"messages": response}

# Define a new graph ``
workflow = StateGraph(state_schema=State)

# Define the node and its function
workflow.add_node("planner", call_planner)
workflow.add_node("tools", tool_nodes)
workflow.add_node("response", call_response)

# Define the edges of the workflow
workflow.add_edge(START, "planner")
workflow.add_conditional_edges(
    "planner",
    lambda state: "tools" if state["messages"][-1].tool_calls else "response",
    {"tools": "tools", "response": "response"}
)

# Add memory saver to the workflow
memory = MemorySaver()
chat_app = workflow.compile(checkpointer=memory)