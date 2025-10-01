from graph.node_constans import RETRIEVE,GENERATE,WEBSEARCH,GRADE_DOCUMENTS
from graph.nodes import generate , grade_documents , web_search , retrieve
from graph.chains.router import question_router, RouteQuery 
from graph.state import GraphState
from graph.chains.hallucination_grader import hallucination_grader
from graph.chains.answer_grader import answer_grader
from langgraph.graph import END, StateGraph
from dotenv import load_dotenv

load_dotenv()

def decide_to_generate(state:GraphState):
    print("---ASSES GRADED DOCUMENTS---")
    if state.web_search:
        print("WEBSEARCH")
        return WEBSEARCH
    else:
        return GENERATE

def grade_generation_grounded_in_document_and_question(state: GraphState) -> str:
    print("CHECK HALLUCINATION")
    question = state.question
    documents = state.documents
    generation = state.generation

    score = hallucination_grader.invoke({"documents": documents, "generation": generation})

    if score.binary_score:
        print("GENERATION IS GROUNDED IN DOCUMENTS")
        score = answer_grader.invoke({"question": question, "generation": generation})
        if score.binary_score:                                                                 
            print("GENERATION ADRESSES QUESTION")
            return "useful"
        else:
            print("GENERATION DOES NOT ADDRESS THE QUESTION")
            return "not useful"
    else:
        print("GENERATION IS NOT GROUNDED IN DOCUMENTS")
        return "not supported"
        
def route_question(state: GraphState) -> str:
    print("ROUTE QUESTION")
    question = state.question
    source = question_router.invoke({"question": question})

    if source.datasource == "websearch":
        return WEBSEARCH
    else:
        return RETRIEVE

workflow = StateGraph(GraphState)

workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEBSEARCH, web_search)

workflow.set_conditional_entry_point(
    route_question,
    {
        WEBSEARCH:WEBSEARCH,
        RETRIEVE:RETRIEVE
    }
)

workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_to_generate,
    {
    WEBSEARCH:WEBSEARCH,
    GENERATE:GENERATE
    } 
)

workflow.add_conditional_edges(
    GENERATE,
    grade_generation_grounded_in_document_and_question,
    {
        "not supported": GENERATE,
        "useful": END,
        "not useful": END
     }
)

workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)

workflow.add_edge(WEBSEARCH,GENERATE)
workflow.add_edge(GENERATE,END)

app = workflow.compile()
app.get_graph().draw_mermaid_png(output_file_path="graph.png")