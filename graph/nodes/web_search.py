from typing import Any, Dict
from graph.state import GraphState
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.schema import Document

web_search_tool = TavilySearchResults(k=3)

def web_search(state:GraphState) -> Dict[str,Any]:
    print("---WEB SEARCH---")

    question = state.question
    documents = state.documents

    docs = web_search_tool.invoke({"query":question})
    # Tavily may return list[dict] or list[str]; normalize to list[str]
    contents = []
    for d in docs:
        if isinstance(d, dict) and "content" in d:
            contents.append(d["content"])
        else:
            contents.append(str(d))
    web_results = "\n".join(contents)

    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]

    # Prevent repeated websearch loops
    return {"documents": documents, "question": question, "web_search": False}
