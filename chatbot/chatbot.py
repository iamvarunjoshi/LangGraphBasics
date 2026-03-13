from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama import ChatOllama
from typing_extensions import TypedDict


# 1. State — list of messages (add_messages appends instead of overwriting)
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 2. LLM
llm = ChatOllama(model="gpt-oss:120b-cloud")


# 3. Node — passes full message history to LLM
def chatbot_node(state: State) -> State:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

builder = StateGraph(State)

#define nodes, which does function
builder.add_node("chatbot",chatbot_node)

#define graph: how flow works
builder.add_edge(START,"chatbot")
builder.add_edge("chatbot",END)


graph = builder.compile(checkpointer=MemorySaver())


#5. Chat Loop
def chat():
    print("Chatbot, ready. Type quit to exit \n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        config = {"configurable": {"thread_id": "1"}}
        result = graph.invoke({"messages": [{"role": "user", "content": user_input}]}, config)
        print(f"Bot: {result['messages'][-1].content}\n")

if __name__ == "__main__":
  chat()