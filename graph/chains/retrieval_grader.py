from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from ingestion import retriever
load_dotenv()

llm = ChatOpenAI(temperature=0)

class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved docuemnts."""

    binary_score : str = Field(
        description="binary score for relevance check, 'yes' or 'no'"
    )

structured_llm_grader = llm.with_structured_output(GradeDocuments)

system_prompt = """
You are a grader assesing whether an LLM generation is grounded in / supported by a set of retrieved facts.
If the document contains keyword or semantic meaning related to question, grade it the relevant.
Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts.
"""

grade_prompt = ChatPromptTemplate.from_messages(
    [
    ('system' , system_prompt),
    ('human' , "Retrieved document: {document} User questions: {questions}")
    ]
)

retrieval_grader = grade_prompt| structured_llm_grader


if __name__ == "__main__":
    user_question = "Akademik  Takvime  nereden  bakabilirim?"
    docs = retriever.get_relevant_documents(user_question)
    retrieved_document = docs[0].page_content
    print(retrieval_grader.invoke(
        {"questions": user_question, "document": retrieved_document}
    ))