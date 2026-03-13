from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    message: str

def greet(state:State) -> State:
    return {"message": f"Hello, {state['message']}"}

def shout(state:State) -> State:
    return {"message": state['message'].upper()}

def punjabi(state:State) -> State:
    return {"message": f"Sat Sri Akal {state['message']}"}

builder = StateGraph(State)
builder.add_node("greet",greet)
builder.add_node("shout",shout)
builder.add_node("pjb",punjabi)

builder.add_edge(START,"greet")
builder.add_edge("greet","shout")
builder.add_edge("shout","pjb")
builder.add_edge("pjb",END)

graph = builder.compile()

result = graph.invoke({"message": "Varun"})
print(result)