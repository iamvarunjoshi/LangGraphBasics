from langgraph.graph import END
from langgraph.types import interrupt
from langchain_ollama import ChatOllama
from chatbot.state import State


llm = ChatOllama(model="gpt-oss:120b-cloud")


def make_chatbot_node(tools):
    llm_with_tools = llm.bind_tools(tools)

    def chatbot_node(state: State) -> State:
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    return chatbot_node


def should_use_tool(state: State) -> str:
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "human_approval"
    return END


def human_approval(state: State) -> State:
    last_message = state["messages"][-1]
    tool_name = last_message.tool_calls[0]["name"]
    tool_args = last_message.tool_calls[0]["args"]

    decision = interrupt(f"LLM wants to call tool {tool_name} with args {tool_args}. Approve? (yes/no)")
    if decision.lower() != "yes":
        return {"messages": [{"role": "tool", "content": "Tool call denied by user.", "tool_call_id": last_message.tool_calls[0]["id"]}]}
    return state
