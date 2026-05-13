import ollama
from tools import *

TOOL_REGISTRY = {
    "calculate": calculate,
    "take_notes": take_notes,
    "read_notes": read_notes,
    "read_all_notes": read_all_notes,
    "web_search": web_search_stub,
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression e.g. '12 * 4'"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for information on a topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "take_notes",
            "description": "Save a result or finding under a key for use in later steps.",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "A short label for this note e.g. 'research_findings'"},
                    "content": {"type": "string", "description": "The content to save"}
                },
                "required": ["key", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_notes",
            "description": "Read a previously saved note by key.",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "The key to look up"}
                },
                "required": ["key"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_all_notes",
            "description": "Read all saved notes to review what has been gathered so far.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
]

def execute_step(step: str, step_number: int) -> str:
    """Run a single plan step using a mini ReAct loop."""

    print(f"\n{'='*50}")
    print(f"⚙️  Executing step {step_number}: {step}")
    print(f"{'='*50}")

    messages = [{"role": "user", "content": f"Complete this task: {step}\nUse tools if needed. Save important results using take_notes."}]

    while True:
        response = ollama.chat(
            model="qwen2.5:7b",
            messages=messages,
            tools=TOOL_SCHEMAS
        )
        msg = response.message

        if msg.tool_calls:
            messages.append({
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": msg.tool_calls
            })

            for tool_call in msg.tool_calls:
                name = tool_call.function.name
                args = tool_call.function.arguments

                print(f"  🔧 Tool: {name}({args})")

                result = TOOL_REGISTRY[name](**args) if name in TOOL_REGISTRY else f"Error: tool '{name}' not found."

                print(f"  📤 Result: {result}")

                messages.append({
                    "role": "tool",
                    "content": str(result)
                })
            else:
                print(f"  ✅ Step result: {msg.content}")
                return msg.content
