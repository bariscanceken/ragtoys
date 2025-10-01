from ingestion import retriever
from graph.state import GraphState
from typing import Any , Dict   

def retrieve(state : GraphState) -> Dict[str, Any]:
    print("---RETRIEVE---")
    
    question = state.question
    documents = retriever.invoke(question)
    # Normalize to list[str] to avoid Pydantic serialization issues
    normalized_documents = []
    for d in documents:
        if hasattr(d, "page_content"):
            normalized_documents.append(getattr(d, "page_content"))
        else:
            normalized_documents.append(str(d))
    
    return {"question":question , "documents":normalized_documents}