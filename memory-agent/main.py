from agent import run_agent as agent

if __name__ == "__main__":
    agent("My name is Shashwat and I'm learning to build AI agents.")
    agent("I enjoy going on a hike and I prefer veg food.")
    agent("I'm currently based in Unnao.")

    # Now test if it remembers — even across restarts
    agent("What do you know about my hobbies?")
    agent("Suggest a weekend activity for me based on what you know.")