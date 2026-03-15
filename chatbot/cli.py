from langgraph.types import Command
from chatbot.graph import graph


def stream_response(user_input: str, config: dict) -> None:
    print("Bot: ", end="", flush=True)
    for chunk, metadata in graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
        stream_mode="messages"
    ):
        if metadata["langgraph_node"] == "chatbot" and hasattr(chunk, "content"):
            print(chunk.content, end="", flush=True)
    print("\n")


def handle_interrupts(config: dict) -> None:
    state = graph.get_state(config)
    while state.tasks and any(t.interrupts for t in state.tasks):
        interrupts = [i for t in state.tasks for i in t.interrupts]
        print(f"[APPROVAL NEEDED] {interrupts[0].value}")
        decision = input("Your decision: ")
        result = graph.invoke(Command(resume=decision), config)
        print(f"Bot: {result['messages'][-1].content}\n")
        state = graph.get_state(config)


def chat():
    print("Chatbot ready. Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break

        config = {"configurable": {"thread_id": "1"}}
        stream_response(user_input, config)
        handle_interrupts(config)
