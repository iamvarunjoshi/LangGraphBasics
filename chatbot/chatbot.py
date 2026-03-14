from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt,Command
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langchain_ollama import ChatOllama
from typing_extensions import TypedDict
from tools import all_tools as tools


# 1. State — list of messages (add_messages appends instead of overwriting)
class State(TypedDict):
    messages: Annotated[list, add_messages]


# 3. LLM — bind tools so it knows they exist
llm = ChatOllama(model="gpt-oss:120b-cloud")
llm_with_tools = llm.bind_tools(tools)


# 4. Nodes
def chatbot_node(state: State) -> State:
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# ToolNode automatically calls whichever tool the LLM requested
tool_node = ToolNode(tools)

# 5. Conditional edge — did the LLM call a tool or is it done?
def should_use_tool(state: State) -> str:
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tool"
    return END


def human_approval(state: State) -> State:
    last_message = state["messages"][-1]
    tool_name = last_message.tool_calls[0]["name"]
    tool_args = last_message.tool_calls[0]["args"]

    decision = interrupt(f"LLM wants to call tool {tool_name} with args {tool_args}. Approve? (yes/no)")
    if decision.lower() != "yes":
        return {"messages": [{"role": "tool", "content": "Tool call denied by user.", "tool_call_id": last_message.tool_calls[0]["id"]}]}
    return state

# 6. Build graph
builder = StateGraph(State)
builder.add_node("chatbot", chatbot_node)
builder.add_node("tool", tool_node)
builder.add_node("human_approval", human_approval)

builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", should_use_tool,{"tool":"human_approval",END:END})  # branches to "tool" or END
builder.add_edge("human_approval", "tool")
builder.add_edge("tool", "chatbot")  # after tool runs, go back to LLM


graph = builder.compile(checkpointer=MemorySaver())


# 7. Chat loop
def chat():
    print("Chatbot ready. Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        config = {"configurable": {"thread_id": "1"}}
        result = graph.invoke({"messages": [{"role": "user", "content": user_input}]}, config)
        # graph paused at interrupt — ask human
        while result.get("__interrupt__"):
            approval_prompt = result["__interrupt__"][0].value
            print(f"\n[APPROVAL NEEDED] {approval_prompt}")
            decision = input("Your decision: ")
            result = graph.invoke(Command(resume=decision), config)

        print(f"Bot: {result['messages'][-1].content}\n")

if __name__ == "__main__":
    chat()
