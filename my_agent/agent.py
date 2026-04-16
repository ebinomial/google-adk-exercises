import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.agents.llm_agent import Agent

from typing import Dict, Any

def get_weather(city: str) -> Dict[str, Any]:
    """Fetch the current weather for a specified city.
    
    Args:
        city (str): The name of the city to fetch the weather for.

    Returns:
        Dict[str, Any]: A dictionary containing the status, city, and weather information.

    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": "The weather in New York is sunny with a temperature of 25 degrees Celsius (77 degrees Fahrenheit)."
        }
    
    else:
        return {
            "status": "error", 
            "report": f"Weather information for {city} is not available."
        }

def get_current_time(city: str) -> Dict[str, Any]:
    """Fetch the current time for a specified city.
    
    Args:
        city (str): The name of the city to fetch the current time for.

    Returns:
        Dict[str, Any]: A dictionary containing the status, city, and current time information.

    """
    
    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "report": f"Sorry, I don't have the current timezone information for {city}."
        }
    
    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return {
        "status": "success",
        "report": f"The current time in {city} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}."
    }

root_agent = Agent(
    model='gemini-2.5-flash',
    name='my_agent',
    tools=[google_search],
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
