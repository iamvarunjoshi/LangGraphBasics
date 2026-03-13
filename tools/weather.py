from langchain_core.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    fake_weather = {
        "delhi": "35°C, sunny",
        "mumbai": "30°C, humid",
        "london": "12°C, cloudy",
    }
    return fake_weather.get(city.lower(), f"No weather data for {city}")
