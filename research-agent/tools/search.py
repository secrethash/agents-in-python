import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()
# Get the key from https://tavily.com/
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def web_search(query: str) -> str:
    """Search the web and return top results with URLs and snippets."""
    try:
        response = client.search(
            query=query,
            max_results=5,
            include_raw_content=False
        )
        results = []
        for i, result in enumerate(response["results"], 1):
            results.append(
                f"[{i}] {result['title']}\n"
                f"    URL: {result['url']}\n"
                f"    Summary: {result['content']}\n"
            )
        
        return "\n".join(results) if results else "No results found"
    except Exception as e:
        return f"Search error: {e}"
    