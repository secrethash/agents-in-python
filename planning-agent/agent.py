from planner import create_plan
from executor import execute_step
from tools import read_all_notes
import ollama

def run_planning_agent(goal: str) -> str:
    print(f"\n🎯 Goal: {goal}")
    print(f"{'='*60}")

    # Phase 1: Plan
    plan = create_plan(goal)
    print(f"\n📋 Plan ({len(plan)} steps):")
    for i, step in enumerate(plan, 1):
        print(f"  {i}. {step}")

    # Phase 2: Execute each step
    results = []
    for i, step in enumerate(plan, 1):
        result = execute_step(step, i)
        results.append(f"Step {i}: {result}")

    # Phase 3: Synthesize into a final answer
    print(f"\n{'='*60}")
    print("🧩 Synthesizing final answer...")

    all_notes = read_all_notes()
    synthesis_prompt = f"""You completed a multi-step task. Here is the goal and everything gathered:
Goal: {goal}

Notes collected during execution:
{all_notes}

Step results:
{chr(10).join(results)}

Now write a clear, well-structured final response that fully addresses the goal."""
    
    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[{"role": "user", "content": synthesis_prompt}]
    )

    print(f"\n🤖 Final Answer:\n{response.message.content}")
