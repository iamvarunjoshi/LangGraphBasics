from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from chatbot.state import State
from chatbot.nodes import chatbot_node, tool_node, human_approval, should_use_tool


def build_graph():
    builder = StateGraph(State)

    builder.add_node("chatbot", chatbot_node)
    builder.add_node("tool", tool_node)
    builder.add_node("human_approval", human_approval)

    builder.add_edge(START, "chatbot")
    builder.add_conditional_edges("chatbot", should_use_tool)
    builder.add_edge("human_approval", "tool")
    builder.add_edge("tool", "chatbot")

    return builder.compile(checkpointer=MemorySaver())


graph = build_graph()
