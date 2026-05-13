from agent import run_planning_agent

if __name__ == "__main__":
    # Test 1: Research task
    run_planning_agent(
        "Research black holes and write a short 3-paragraph summary."
    )

    # Test 2: Multi-domain task
    run_planning_agent(
        "Calculate the area of a circle with radius 7, then explain what that number means in real life."
    )
