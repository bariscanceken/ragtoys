from pydantic import BaseModel, Field
from typing import List, Optional, Any

class GraphState(BaseModel):
    """
    Represent the state of a graph
    Attributes:
        question: question
        generation: LLM generation
        web_search: whether to add search or not
        documents: list of documents
    """
    question: str
    generation: Optional[str] = ""
    web_search: Optional[bool] = False
    documents: Optional[List[Any]] = Field(default_factory=list)