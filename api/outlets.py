from typing import TypedDict, Annotated
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langchain.chat_models import init_chat_model


# Initialize the chat model
llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

def get_database(db_path: str = "zus_stores.db") -> SQLDatabase:
    """Create a SQLDatabase instance from a SQLite DB."""
    return SQLDatabase.from_uri(f"sqlite:///{db_path}")


def get_prompt_template() -> ChatPromptTemplate:
    """Return a chat prompt template for generating SQL queries."""
    system_message = """
    You are an expert in generating SQL queries for the Zus outlets.
    Given an input question, create a syntactically correct sqlite3 query to
    run to help find the answer. Unless the user specifies in his question a
    specific number of examples they wish to obtain, always limit your query to
    at most 10 results. You can order the results by a relevant column to
    return the most interesting examples in the database.

    Never query for all the columns from a specific table, only ask for the
    few relevant columns given the question.

    Pay attention to use only the column names that you can see in the schema
    description. Be careful to not query for columns that do not exist. Also,
    pay attention to which column is in which table.

    Only use the following tables:
    {table_info}
    """
    user_prompt = "Question: {input}"
    return ChatPromptTemplate([("system", system_message), ("user", user_prompt)])


class QueryOutput(TypedDict):
    """Generated SQL query."""
    query: Annotated[str, ..., "Syntactically valid SQL query."]


def write_query(str_query: str) -> dict:
    """Generate a SQL query to fetch information from user input."""
    db = get_database()
    
    prompt_template = get_prompt_template()
    prompt = prompt_template.invoke({
        "table_info": db.get_table_info(),
        "input": str_query,
    })

    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return {"query": result["query"]}


def execute_query(sql_query: str) -> dict:
    """Execute a given SQL query using QuerySQLDatabaseTool."""
    db = get_database()
    
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    return {"result": execute_query_tool.invoke(sql_query)}

if __name__ == "__main__":
    user_question = "what is the address of the zus outlets at monash university"
    sql_query = write_query(user_question)

    print("Generated SQL Query:")
    print(sql_query["query"])

    query_result = execute_query(sql_query["query"])

    print("Query Result:")
    print(query_result["result"])
