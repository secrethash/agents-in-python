import requests
from bs4 import BeautifulSoup

# Cache scrapped pages for the session
_cache: dict[str, str] = {}

def scrape_page(url: str, max_chars: int = 4000) -> str:
    """Fetch a webpage and return clean readable text."""

    if url in _cache:
        print(f"  📦 Cache hit: {url}")
        return _cache[url]

    try:
        headers = {"User-Agent": "Mozilla/5.0 (research agent)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # remove noise like scripts, styles, nav, footers
        tagsToRemove = ["script", "style", "nav", "footer", "header", "aside"]
        for tag in soup(tagsToRemove):
            tag.decompose()

        # Extract text
        text = soup.get_text(separator="\n")

        # Clean up excessive whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        clean_text = "\n".join(lines)

        # Truncate to max_chars to stay within the LLM context limit
        if len(clean_text) > max_chars:
            clean_text = clean_text[:max_chars] + "\n\n[Page Truncated...]"
        
        return clean_text
    
    except requests.exceptions.Timeout:
        return f"Error: Request timed out for {url}"
    except requests.exceptions.HTTPError as e:
        return f"Error: HTTP {e.response.status_code}"
    except Exception as e:
        return f"Error scraping page: {e}"
