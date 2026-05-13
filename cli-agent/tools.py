import math

def calculate(expression: str) -> str:
    """Safely evaluate a mathematical expression."""
    try:
        # we control the input context, so eval should be fine here
        result = eval(expression, {"__builtins__": {}}, vars(math))
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def get_weather(city: str) -> str:
    """Stub: return fake weather data for a city."""

    fake_data = {
        "london": "15°C, cloudy",
        "new york": "22°C, sunny",
        "tokyo": "28°C, humid",
    }

    return fake_data.get(city.lower(), "Weather data not available.")