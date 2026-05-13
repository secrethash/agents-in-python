import ollama
from tools import calculate, remember, recall

TOOL_REGISTRY = {
    "calculate": calculate,
    "remember": remember,
    "recall": recall,
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
                    "expression": {
                        "type": "string",
                        "description": "Math expression e.g. '12 * 4'",
                    },
                },
                "required": ["expression"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remember",
            "description": "Save important information about the user for future reference.",
            "parameters": {
                "type": "object",
                "properties": {
                    "information": {
                        "type": "string",
                        "description": "The fact or info to remember",
                    }
                },
                "required": ["information"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "recall",
            "description": "Search memory for information relevant to the user's question.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "What to search for in memory"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

conversation_history = []


def run_agent(user_message: str):
    print(f"\n👤 User: {user_message}")

    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    while True:
        response = ollama.chat(
            model="qwen2.5:7b",
            messages=conversation_history,
            tools=TOOL_SCHEMAS
        )

        msg = response.message

        if msg.tool_calls:
            conversation_history.append({
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": msg.tool_calls
            })

            for tool_call in msg.tool_calls:
                name = tool_call.function.name
                args = tool_call.function.arguments

                print(f"\n🔧 Tool called: {name}({args})")

                result = TOOL_REGISTRY[name](**args) if name in TOOL_REGISTRY else f"Error: tool '{name}' not found."

                print(f"📤 Tool result: {result}")

                conversation_history.append({
                    "role": "tool",
                    "content": str(result)
                })
        else:
            print(f"\n🤖 Agent: {msg.content}")
            conversation_history.append({
                "role": "assistant",
                "content": msg.content
            })
            break
