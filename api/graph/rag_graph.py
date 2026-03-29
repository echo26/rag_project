from langgraph.graph import END, START, StateGraph

from graph.nodes.retriever import retrieve
from graph.state import RAGState

_builder = StateGraph(RAGState)
_builder.add_node("retriever", retrieve)
_builder.add_edge(START, "retriever")
_builder.add_edge("retriever", END)

rag_graph = _builder.compile()
