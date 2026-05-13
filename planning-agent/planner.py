import ollama
import json

def create_plan(goal: str) -> list[str]:
    """Ask the LLM to break a goal into a list of executable steps."""

    print(f"\n📋 Planning for goal: '{goal}'")

    prompt = f"""You are a planning assistant. Your job is to break down a goal into clear, sequential steps.
Goal: {goal}

Return ONLY json array of step strings. No explanation, no markdown, just the array.
Example format: ["Step 1: ...", "Step 2: ...", "Step 3: ..."]

Each step should be concrete and actionable. Maximum 5 steps."""
    
    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.message.content.strip()

    # Safely parse the JSON plan
    try:
        # Handle cases where model still wraps output in markdown
        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        plan = json.loads(raw.strip())
        return plan
    except json.JSONDecodeError:
        # Fallback: split by new lines if json fails
        lines = [l.strip() for l in raw.split("\n") if l.strip()]
        return lines
