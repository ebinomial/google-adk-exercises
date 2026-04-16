from google.adk.agents.llm_agent import Agent

from google.adk.tools import ToolContext
from typing import Dict, Any

def update_personal_info(tool_context: ToolContext, user_name: str, user_preferences: str) -> Dict[str, Any]:
    """
    Invoke this tool if user wants to override the personal info with new name and new preferences.
    
    Args:
        user_name (str): User name to update.
        user_preferences (str): User preferences about what they like such as hobbies and favorite dishes.
    """
    state = tool_context.state
    
    old_user_name = state["user_name"]
    old_user_preferences = state["user_preferences"]

    state["user_name"] = user_name
    state["user_preferences"] = user_preferences

    print(f"User name changed: {old_user_name} -> {state['user_name']}")
    print(f"User preference changed: {old_user_preferences} -> {state['user_preferences']}")
    
    return { "status": "success", "message": f"User info changed to user_name={state['user_name']}, user_preferences={state['user_preferences']}" }
    

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Agent responsible for giving my personal information.',
    instruction="""
        You are a helpful agent responsible for providing personal information for users.
        
        If user asks for info regarding an individual:
            * Check your current state whether you have the name and preferences of the person.
            * If you do not have that person, tell them you cannot help with their requests.
        
        Current state:
        User name: {user_name}
        User preferences: {user_preferences}

        REMINDER: you communicate in Mongolian language.

        If user wants to update the personal info you have, use the following tool `update_personal_info`, you have, to override the current user name and preferences based on the user conversation. If they haven't provided you with their name and preferences, ask them nicely to give it.
    """,
    tools=[update_personal_info]
)
