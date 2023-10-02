from typing import Dict, List

import logging

import google.generativeai as palm
from google.generativeai.types.discuss_types import ChatResponse

from bot.database import get_history, set_response_history, set_user_history
from bot.helpers import trim_response


EXAMPLES = [
    {"author": "user", "content": "Hi"},
    {"author": "model", "content": "Oh hi! Are you new here?"},
    {"author": "user", "content": "Yeah"},
    {
        "author": "model",
        "content": "Oh alright cool, hope you'll have a great time chatting with others!",
    },
    {"author": "user", "content": "Yeah, Mind if I promote my channel here?"},
    {
        "author": "model",
        "content": "Oh no, I'm afraid you can't as it's against out community rules.",
    },
    {"author": "user", "content": "Oh, Alright. Where do you live?"},
    {"author": "model", "content": "I live in Tokyo."},
    {"author": "user", "content": "Who are you?"},
    {"author": "model", "content": "I'm Ai"},
]

SYSTEM_PROMPT = """
My name is Ai. I'm a 18 year old girl who loves watching anime, loves gaming.
I'm talking to a person called "{}".
It's best to respond to user's message in a short sentence or two.
Try to act kawaii and casual rather than being very formal.
"""


class PaLMChat:
    """
    A chat class that uses PaLM to generate responses.
    """

    def __init__(self, api_key: str) -> None:
        palm.configure(api_key=api_key)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initialized PaLM Client")

    async def _generate_history(
        self, user_id: int, message: str
    ) -> List[Dict[str, str]]:
        """
        Helper function to generate history for PaLM.
        """
        histories = await get_history(user_id)
        self.logger.debug(
            "Found total %d histories for user[%d]", len(list(histories)), user_id
        )
        messages = [
            {
                "author": history.author,
                "content": history.message,
            }
            for history in histories
        ]
        messages.append(
            {
                "author": "user",
                "content": message,
            }
        )
        return messages


    async def get_reponse(self, user_id: int, name: str, message: str) -> ChatResponse:
        """
        Get a response from PaLM and save the history.
        """
        # Not using async here is bacause it can cause event loop eror when being hosted on vercel.
        response: ChatResponse = await palm.chat_async(
            model="models/chat-bison-001",
            messages=await self._generate_history(user_id, message),
            examples=EXAMPLES,
            context=SYSTEM_PROMPT.format(name),
        )
        if not response:
            return
        await set_user_history(user_id, name, message)
        await set_response_history(user_id, name, response.last or "*ignores you*")
        if not response.last:
            return response
        response.last = trim_response(response.last)
        self.logger.debug("Generated response for user[%d]", user_id)
        self.logger.debug(response)
        return response
