from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Literal

class RouteQuery(BaseModel):
    """
    Route a user query to the most relevant datasource
    """

    datasource : Literal["vectorstore","websearch"] = Field(
        ...,
        description="Given a user questions choose to route it to web search or a vectorstore"
    )

llm = ChatOpenAI(temperature=0)
structured_llm_router = llm.with_structured_output(RouteQuery)

system_prompt = """
You are an expert at routing user questions to either a vectorstore or websearch.
The vectorstore contains documents ONLY about Python programming, including syntax, libraries, data structures, algorithms, and common Python usage.
- If the question is clearly related to Python programming topics, ALWAYS route it to 'vectorstore'.
- For all other questions, ALWAYS route it to 'websearch'.
- Do not guess; use the vectorstore only for the specified topics.
- Respond ONLY with the field 'datasource' and its value, either 'vectorstore' or 'websearch'.
"""

route_prompt = ChatPromptTemplate.from_messages(
    [
    ("system" , system_prompt),
    ("human" , "{question}")
    ]
)

question_router  = route_prompt | structured_llm_router
