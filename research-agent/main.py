from agent import run as run_agent

if __name__ == "__main__":
    # Test 1: Current events question
    run_agent("What are the latest breakthrough in fusion energy?")

    # Test 2: Comparative Research
    run_agent("What are the pros and cons of Rust vs Go for systems programming?")

    # Test 3: Deep-dive question, requiring page scraping
    run_agent("How does RAG work in modern LLM applications and what are it's limitations?")

    # Test 4: Try scrapping a URL to get the latest data.
    run_agent("Find software engineer roles on https://www.wiz.io/careers")
