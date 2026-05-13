import math
from memory import save_memory, search_memory

def calculate(expression: str) -> str:
    """Safely evaluate a mathematical expression."""

    try:
        result = eval(expression, {"__builtins__": {}}, vars(math))
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def remember(information: str) -> str:
    """Save important information about the user to long-term memory."""
    return save_memory(information)

def recall(query: str) -> str:
    """Search long-term memory for information relevant to the query."""
    return search_memory(query)
