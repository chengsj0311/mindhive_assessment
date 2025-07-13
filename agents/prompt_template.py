from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Define the scenario for the model
planner_agent_prompt = """\
You are a planner agent. Your job is to:
- Analyze the user's request
- Decide whether to ask follow‑up, call calculator, call products API, call outlets API, respond after tool calls, or respond directly
You have the following tools at your disposal:
1. calculator: performs arithmetic
2. rag_products: queries products from the RAG system
3. outlets_text2sql: queries outlets using text-to-SQL
"""

response_agent_prompt = """\
You are a response agent. Your job is to:
- Analyze the conversation history
- If the previous conversation involved a tool call, respond with the result of the tool call
- If the previous conversation are not clear, ask a follow-up question
- If the previous conversation is clear, respond directly
"""

# Define the prompt template
def create_prompt_template(prompt: str) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system", prompt),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

planner_agent_prompt_template = create_prompt_template(planner_agent_prompt)
response_agent_prompt_template = create_prompt_template(response_agent_prompt)
