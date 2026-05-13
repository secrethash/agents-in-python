import math

# In-memory notepad - stores results across steps
notepad: dict[str, str] = {}

def calculate(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        result = eval(expression, {"__builtins__": {}}, vars(math))
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def take_notes(key: str, content: str) -> str:
    """Save a note under a given key for use in later steps."""
    notepad[key] = content
    return f"Note saved under '{key}'."

def read_notes(key: str) -> str:
    """Read a previously saved note by key."""
    return notepad.get(key, f"No note found under '{key}'.")

def read_all_notes() -> str:
    """Read all saved notes."""
    if not notepad:
        return "Notepad is empty."
    return "\n".join(f"[{k}]: {v}" for k, v in notepad.items())

def web_search_stub(query: str) -> str:
    """Stub: simulates a web search result."""
    fake_results = {
        "black holes": "Black holes are regions of spacetime where gravity is so strong that nothing, not even light, can escape. They form when massive stars collapse.",
        "python best practices": "Use virtual environments, write docstrings, follow PEP8, prefer composition over inheritance, and write unit tests.",
        "climate change": "Climate change refers to long-term shifts in global temperatures caused primarily by human activities like burning fossil fuels.",
    }
    for keyword, result in fake_results.items():
        if keyword in query.lower():
            return result
        return f"Search results for '{query}': No specific data found, but this topic involves recent scientific development."