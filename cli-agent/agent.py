import ollama
from tools import calculate, get_weather

# --- Tool Registry ---
# Maps tool name (string) -> actual python function
TOOL_REGISTRY = {
    "calculate": calculate,
    "get_weather": get_weather,
}

# --- Tool Schema ---
# This is what the LLM sees
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression. Use this for any arithmetic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A valid math expression e.g. '2847 * 193' or 'sqrt(144)'",
                    },
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city e.g. 'London'",
                    }
                },
                "required": ["city"],
            }
        },
    }
]

def run_agent(user_message: str) -> str:
    print(f"\n 👤 User: {user_message}")

    # Conversation history - this is the agent's short term memory
    messages = [{"role": "user", "content": user_message}]

    # --- ReAct Loop ---
    while True:
        # Step 1: Send message + tool schema to LLM
        response = ollama.chat(
            model="qwen2.5:7b",
            messages=messages,
            tools=TOOL_SCHEMAS
        )

        msg = response.message

        # Step 2: Did the LLM want to call a tool?
        if msg.tool_calls:
            # Append LLM's intent to history
            messages.append({"role": "assistant", "content": msg.content or "", "tool_calls": msg.tool_calls})

            # Step 3: Execute each tool call OUR side
            for tool_call in msg.tool_calls:
                name = tool_call.function.name
                args = tool_call.function.arguments

                print(f"\n 🔧 Tool called: {name}({args})")

                # Lookup actual python function and run it
                if name in TOOL_REGISTRY:
                    result = TOOL_REGISTRY[name](**args)
                else:
                    result = f"Error: tool '{name}' not found."
                
                print(f"📤 Tool result: {result}")

                # Step 4: Feed the result back to the LLM as a new message
                messages.append({
                    "role": "tool",
                    "content": str(result),
                })
        else:
            # LLM gave a final answer; no more tool calls
            print(f"\n🤖 Agent: {msg.content}")
            break
