from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from chatbot.state import State
from chatbot.nodes import make_chatbot_node, human_approval, should_use_tool


def build_graph(tools):
    builder = StateGraph(State)

    builder.add_node("chatbot", make_chatbot_node(tools))
    builder.add_node("tool", ToolNode(tools))
    builder.add_node("human_approval", human_approval)

    builder.add_edge(START, "chatbot")
    builder.add_conditional_edges("chatbot", should_use_tool)
    builder.add_edge("human_approval", "tool")
    builder.add_edge("tool", "chatbot")

    return builder.compile(checkpointer=MemorySaver())
