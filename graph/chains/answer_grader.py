from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate

llm = ChatOpenAI(temperature=0)

class GraderAnswer(BaseModel):
    binary_score: bool = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )

structured_llm_grader = llm.with_structured_output(GraderAnswer)

system_prompt = """
You are a grader assesing whether an answer addresses / resolves a question
Give a binary score 'yes' or 'no'. 'Yes' means that the answer resolves the question.
"""

answer_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "User question:\n\n{question}")
])

answer_grader = answer_prompt | structured_llm_grader