from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """Evaluate a basic math expression like '2 + 2' or '10 * 5'."""
    try:
        result = eval(expression)
        return str(result)
    except Exception:
        return "Invalid expression"
