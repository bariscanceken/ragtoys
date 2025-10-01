from typing import Any,Dict
from graph.chains.retrieval_grader import retrieval_grader
from graph.state import GraphState

def grade_documents(state: GraphState) -> Dict[str , Any]:
    """
    Determeines whether the retrieved documents are relevant to the question
    If any document is not relevant, we will set a flag to run web search

    Args:
        State (dict): The current state of the graph

    Returns:
        State (dict): Filtered out irrelevant documents and updated web_search state 
    """
    print("---CHECK DOCUMENT RELEVANT  TO QUESTİON")

    question = state.question
    documents = state.documents

    filtered_docs = []

    web_search = False

    for d in documents:
        score = retrieval_grader.invoke(
            {"question": question, "document": d}
        )

        grade = score.binary_score

        if grade.lower() == 'yes':
            print("---GRADE: DOCUMENT RELEVANT")
            filtered_docs.append(d)
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT")
            web_search = True
            continue
    
    return{"question":question , "documents":filtered_docs , "web_search":web_search}
        