import asyncio
import logging

from uuid import uuid4
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session
from google.genai import types
from question_answering_agent.agent import root_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_ = load_dotenv()

async def main():

    session_service_stateful = InMemorySessionService()

    logger.info("Created InMemorySessionService instance!")

    initial_state = {
        "user_name": "Бямбадоржийн Эрдэнэбилэг",
        "user_preferences": """
            Би рибай стейк болон давсалсан хулд эсвэл яргай загасанд дуртай.
            Би тетрис тоглох болон World of Warcraft тоглох дуртай.
            Миний дуртай анимэ бол JoJo's Bizarre Adventure: Steel Ball Run (2026).
            Миний дуртай кино харин `Gran Torino`.
        """
    }

    APP_NAME = "ТУСЛАХ_БОТ"
    USER_ID = "RDNB0327"
    SESSION_ID = str(uuid4())

    stateful_session: Session = await session_service_stateful.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    )

    logger.info("Created stateful_session object with the following properties:")
    logger.info(f"App name:\t\t{stateful_session.app_name}")
    logger.info(f"User ID:\t\t{stateful_session.user_id}")
    logger.info(f"Session ID:\t\t{stateful_session.id}")
    logger.info(f"State:\t\t{stateful_session.state}")

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service_stateful,
    )
    
    while (True):

        user_query = input(">_ ")
        
        if user_query.lower() in ["exit", "quit"]:
            break

        new_message = types.Content(
            role="user",
            parts=[
                types.Part(
                    text=user_query.lower()
                )
            ]
        )
        
        for event in runner.run(
            user_id=USER_ID,
            session_id=stateful_session.id,
            new_message=new_message,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    logger.info(f"> [Agent]: {event.content.parts[0].text}")


    logger.info("=== Session Event Exploration ===")
    session = await session_service_stateful.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=stateful_session.id
    )

    print("=== Final Session State ===")
    for key, value in session.state.items():
        logger.info(f"{key}: {value}")
    

asyncio.run(main())
