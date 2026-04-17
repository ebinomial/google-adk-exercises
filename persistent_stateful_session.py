import os
import asyncio
import logging
from google.genai import types
from uuid import uuid4

from memo_tracking_agent.agent import root_agent
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_ = load_dotenv()

db_url = "sqlite+aiosqlite:///./data/agent_memory.db"
session_service = DatabaseSessionService(db_url=db_url)


initial_state = {
    "user_name": "Erdenebileg Byambadorj",
    "reminders": ["prepare AI forecasting presentation"],
}

async def main():

    APP_NAME = "Reminder Agent"
    USER_ID = "RDNB-100100235"
    
    existing_sessions = await session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    if existing_sessions and len(existing_sessions.sessions) > 0:

        SESSION_ID = existing_sessions.sessions[0].id
        logger.info(f"Reusing the latest session: {SESSION_ID}")
    
    else:
        
        new_session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
        )

        SESSION_ID = new_session.id

        logger.info(f"No session found. Creating a new one: {new_session.id}")
    
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    logger.info(f"Getting started with conversational cycles.")
    
    while (True):
        user_query = input(">_ ")

        if user_query.lower() in ["exit", "quit"]:
            logger.info(f"Ciao Ciao.")
            break

        content = types.Content(role="user", parts=[types.Part(text=user_query)])
        
    
        async for event in runner.run_async(
            session_id=SESSION_ID,
            user_id=USER_ID,
            new_message=content
        ):
            if event.is_final_response():
                logger.info(f">_ {event.content}")

    logger.info("Shutting down...")


if __name__ == "__main__":
    asyncio.run(main())
