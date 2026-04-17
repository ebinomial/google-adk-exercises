from google.adk.agents.llm_agent import Agent

from typing import List, Dict, Any
from google.adk.tools import ToolContext

def operate_todo_list(
        context: ToolContext,
        new_todo_items: List[str] | None,
        operation: int
    ) -> Dict[str, Any]:
    
    """
    Tool responsible for managing user todo list.
    With this function, a new subset of todo items can
    be added to the current state, overwrite or empty 
    the user todo list.
    
    Args:
        - new_todo_items (List[str] | None): a list of string representing new user todo items. It can be empty or none when operation argument is 3 (delete) or 4 (view).
        - operation (int): It can either be 1 to extend with a new subset of todo items, 2 to replace with a new subset of todo items, 3 to empty the todo list, or 4 to view the current todo list.

    Returns:
        Dict[str, Any]: Result of operation on the todo items and the current user state.
    """

    if operation == 1:
        if len(new_todo_items) <= 0:
            return {
                "status": "failed",
                "message": "No items to add passed."
            }

        context.state["reminders"] += new_todo_items

    elif operation == 2:
        context.state["reminders"] = new_todo_items

    elif operation == 3:
        context.state["reminders"] = []
        return {
            "status": "success",
            "message": "Emptied the user todo list to nothing."
        }

    elif operation == 4:
        return {
            "status": "success",
            "results": {
                "user_name": context.state["user_name"],
                "user_todo_list": context.state["reminders"]
            }
        }
    
    else:
        return {
            "status": "failed",
            "message": f"Unsupported operation {operation}."
        }

    return {
        "status": "success",
        "results": {
            "user_name": context.state["user_name"],
            "user_todo_list": context.state["reminders"]
        }
    }

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="A memo agent responsible for keeping track of user todo list.",
    instruction="""
    You are in charge of tracing the todo list of user {user_name}. Use `operate_todo_list` tool to observe and update the user memo. User may request you to carry out the following functions and you are to interpret their intent based off of user queries and execute it:
        
        - Add a new todo list (i.e. "buy a salmon" and "cook lunch" in addition to the current todo list of "make a sandwich")
        - Overwrite with a new todo list (i.e. replacing the current "buy a salmon" with "buy a tenderloin steak")
        - Delete or empty the current todo list if user wants to get rid of the memo.
        - View the current todo list when user wishes to keep track of it themselves.

    For a specific choice of arguments, I want you to read the tool description carefully and configure the parameters accordingly.
    """,
    tools=[operate_todo_list]
)
