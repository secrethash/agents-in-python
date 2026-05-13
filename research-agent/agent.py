import ollama
from tools import web_search, scrape_page

TOOL_REGISTRY = {
    "web_search": web_search,
    "scrape_page": scrape_page,
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information on a topic. Returns titles, URLs, and summaries. Use this first before scraping.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query e.g. 'latest developments in fusion energy 2024'"
                    }
                },
                "required": ["query"]
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "scrape_page",
            "description": """Fetch and read the full content of a webpage by URL.
Use this tool when:
- The user provides a specific URL to read
- Search snippets are too brief to answer the question
- You need to find specific items on a page (jobs, products, prices, docs)
- The question requires detail that only the full page would have""",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Full URL of the page to scrape e.g. 'https://example.com/article'"
                    }
                },
                "required": ["url"]
            }
        }
    }
]

SYSTEM_PROMPT = """You are a through research assistant. When given a question:
1. Search the web to find relevant sources
2. Scrape pages when you need more details than the snippet provides
3. Synthesize findings into a clear, well-structured answer
4. Always cite your sources at the end with [1], [2], etc. referencing the URLs you used

IMPORTANT: Always use web_search first before giving any answer. Never answer from memory alone.
Be through but concise. Prefer recent sources."""

def run(question: str):
    print(f"\n🔎 Research Question: {question}")
    print("="*60)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    # Source tracing for citation
    sources_used = []

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

            for tool in msg.tool_calls:
                name = tool.function.name
                args = tool.function.arguments

                print(f"\n🔧 {name}({args})")

                result = TOOL_REGISTRY[name](**args) if name in TOOL_REGISTRY else f"Error: unknown tool '{name}'"
                
                # track sources
                if name == "scrape_page":
                    # Truncate and use
                    display = result if len(result) < 300 else result[:300] + "..."
                    print(f"📤 {display}")

                    messages.append({"role": "tool", "content": str(result), "name": name})
        else:
            # If model returns empty content, explicitly ask it to synthesize
            if not msg.content or not msg.content.strip():
                print("\n⚠️  Empty response detected - forcing synthesis...")
                messages.append({
                    "role": "user",
                    "content": "Based on the search results above, please write a thorough and well-structured answer to the original question. Cite the sources you used.",
                })

                # One final call to get the actual answer
                synthesis = ollama.chat(
                    model="qwen2.5:7b",
                    messages=messages
                )
                print(f"\n📝 Final Answer:\n{synthesis.message.content}")
            else:
                print(f"\n📝 Final Answer:\n{msg.content}")

            if sources_used:
                print(f"\n📚 Pages scrapped during research:")
                for url in sources_used:
                    print(f"  • {url}")
            break