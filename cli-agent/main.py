from agent import run_agent

if __name__ == "__main__":
    # Test 1: Maths
    run_agent("What is 2847 multiplied by 193?")

    # Test 2: Weather
    run_agent("What's the weather like in tokyo?")

    # Test 3: Multi-step
    run_agent("What's the square root of 256 and what's the weather in London?")
