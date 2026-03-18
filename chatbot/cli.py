from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.types import Command
from chatbot.graph import build_graph

MCP_SERVER_URL = "http://127.0.0.1:8000/mcp/"


async def stream_response(graph, user_input: str, config: dict) -> None:
    print("Bot: ", end="", flush=True)
    async for chunk, metadata in graph.astream(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
        stream_mode="messages"
    ):
        if metadata["langgraph_node"] == "chatbot" and hasattr(chunk, "content"):
            print(chunk.content, end="", flush=True)
    print("\n")


async def handle_interrupts(graph, config: dict) -> None:
    state = await graph.aget_state(config)
    while state.tasks and any(t.interrupts for t in state.tasks):
        interrupts = [i for t in state.tasks for i in t.interrupts]
        print(f"[APPROVAL NEEDED] {interrupts[0].value}")
        decision = input("Your decision: ")
        result = await graph.ainvoke(Command(resume=decision), config)
        print(f"Bot: {result['messages'][-1].content}\n")
        state = await graph.aget_state(config)


async def chat():
    client = MultiServerMCPClient({
        "registry": {
            "url": MCP_SERVER_URL,
            "transport": "streamable_http"
        }
    })
    tools = await client.get_tools()
    graph = build_graph(tools)

    print("Chatbot ready. Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break

        config = {"configurable": {"thread_id": "1"}}
        await stream_response(graph, user_input, config)
        await handle_interrupts(graph, config)
