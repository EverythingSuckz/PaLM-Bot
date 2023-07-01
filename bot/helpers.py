import logging
from typing import Callable
from pyrogram import types
from cachetools import TTLCache

logger = logging.getLogger(__name__)

def limiter(rate_limit_seconds: float) -> Callable:
    logger = logging.getLogger("limiter")
    # Hacky and efficient way for doing a time based cache.
    cache = TTLCache(maxsize=1_000, ttl=rate_limit_seconds)
    def decorator(func):
        async def wrapper(_, message: types.Message):
            logger.debug("Limiter was invoked for %s.", func.__name__)
            # Anon Admins
            user_id = message.from_user.id if message.from_user else message.sender_chat.id
            if user_id not in cache:
                cache[user_id] = False
                await func(_, message)
                # Added because the main message handler will pick this message update too.
                await message.stop_propagation()
            else:
                if cache[user_id] is False:
                    await message.reply("<b>You're sending messages too quickly. Please wait.</b>")
                # Another hacky and minimal implementation to make the bot not spam this message.
                cache[user_id] = True
        return wrapper
    return decorator

























                                                                   
    #  ▄▄▄▄▄▄▄     ▄ ▄   ▄▄  ▄ ▄  ▄ ▄▄     ▄   ▄▄▄▄  ▄▄  ▄▄▄▄▄▄▄     
    #  █ ▄▄▄ █ ▀███▀▀ ██▄ █ █▀▀▄█▀▀█▄▄█▄▀█▄▀▄▀▄█▄▀█ ▄▄█  █ ▄▄▄ █     
    #  █ ███ █ ▀▀█  ▀ ▀▄▀▀█ ▄▄█▄ ▄▄▄█▄▄▄▄▀▀█▄ ▄ ▄█▀ ▄ █  █ ███ █     
    #  █▄▄▄▄▄█ █▀▄ ▄ █▀█▀█ ▄▀▄▀▄▀█ ▄ █ ▄ █ █ ▄▀█▀█▀█ █ ▄ █▄▄▄▄▄█     
    #  ▄▄▄▄▄ ▄▄▄▀ ██▄▀▄█████▄▀ █ █▄▄▄█▄▀▄ █▄▄█▀   ▄▀ ▄▄▀▄ ▄ ▄ ▄      
    #  █ █  ▀▄█▀█▀▄▀ ▀   █▀ ▄██▀█▀ ▀▀██▀▄ █▄█ ▀ ▀▀▀█ ▄▄▀▀ ▄█▀██▀     
    #  █ █  ▀▄██▀▀  ▀ ▀▄█▄ ▀█▀█▄█▄▀▀█▀█ ▄▄ ▄█ ▄▀█▀▄ ▀█ ▀ ▄  ▀██▄     
    #  ▄█▀▄ ▄▄█  █ ▄█  ▄▀▄▀ ▄▀▀▀▀ █ █▀▄▄█▄▀▄▀  ▀▀█▄ ▀▄▄▀█▄▀▄▄▀█▀     
    #   ▄▄▄▀▄▄ ▀██ ▀█ ▄▄▀▄█▄▀  ▄█ ▄▀▄█▄ ▄█▀▄▄█▀▀▄▀▄▀▀  ▀▄▄▀ ▀▀█▀     
    #  ▀ ██▄▀▄ ▀▀▄▄█▄▄  ▀ ▀▄ ▀██▀  ▀▀▀▀▀█▄▀▄▀ █ ▄▀▄▄▄▄▀█▄▄  ▀██▀     
    #  ▀▀██▀▀▄ ▄▄▀▄▄▄██ ▄▄▀  ▀██▀  ▀█▀▄ ▄ ▀▄▀▀▀▀▄▀▄ ▄▄███▄▀▀▀█       
    #  ▀█▀ ▀█▄ ▀▀ ▄▀▄▄█▄ ▄▀ ▄▀▀█▀▀▄▀█▀█ ▄ ▀▄█ █ █▀▄ ▀▄▀█▀ ▀ ██▀▀     
    #  █ ▀▄▄▄▄  ▀ █▄█ ▀▄▀▄▀▄▀ ▀▄█ ▀▀▀ ▀▀▄▀▄▄▀  ▀█▀▄ ▄ ▀▄▄▄█▀▀█▄▄     
    #  █▀ ███▄██  ██ █▀▄▀ █  ▀██▀▄██▄█▀█▄▄▄▄▀▄ ▀█▀▄ ▄ ██▄▄██▀▄▄▀     
    #  █  ▄█ ▄ █▄▀▀▀█▀█▄ ▄▄▄▀  ▄▀█ ▄ █▄ ▀███▄▄▀ ▀ ▀▀▄ ▄█ ▄ ███       
    #  ▄▀▀▄█▄▄▄█▄██  ▀ ▄▀▄█▄█ ▀█▀█▄▄▄█▄ ▄ ▄▀▄▄ ▀▀█▄█▄ ▄█▄▄▄███▄▀     
    #  ▀ ▀ ▄█▄  █▄ ██▀▀▄▄██▄▀▀▀▀▀ ▀▄█▄█ ▀█▄█▄▄▄▀▄█▄▀██ ▄█▀▄ ▀█ █     
    #  ▀████▄▄▀▀▄▀ ▀▄▀▀▄█▄▀  ▀█▀▄█▀▄▄█ █▄ ██▄▄▄▀▀▀  ▄▄▄▄█▀▄ ▀▄▀▀     
    #    ▄█ █▄█ █ █ █▄█ █▄▄▄▀ ▀█▀██▄▀▀█▀▄▀▄█▄▄▄▀█▀▀▀▄    ▀ ▄██▀▀     
    #  ▀  ▀▄█▄▀▀▄ ▀  ▀ ▄▀▄ ▄  ▀█ ▄ ▄▄▄█▄  ▀ ▀▄▄▀▄▀ ▄▄ ▀██ ▄▄▄▀       
    #  █▀▄█▄▄▄█▀█ █▄▀█▄ ▄███▀ ▀█▄▀▀ ▄▄▄ ▄▄█▄█▄▀▀▀██▀▄▀ ▄▀█ ▄▄▀▀      
    #  ▀ ▀█▀▀▄▀▄▀ ▄▀█▄  ▄▄▄▄▀█▀▀ █▄ ▄█▄ ▄▄▀▀█▄▄▀███▀▄▄ ▄   ▄▄▀▀▀     
    #  █▄▀ █ ▄▄ ██▀    ▄▄█ ▄▀ █ ▄  █▄█▀▀▀▄▄█    ▄▄▄ ▄▀▀▄▀▀ ▄██▀▀     
    #  █▀█ ▀█▄▀▀█▀ █▄▄▀  █▀   █▀▄▀ ▄▄█ ▄▀▄▄█▀▄▀▄▀██▀  ▄▄▄ ▄ ▄▀▄▀     
    #  ▀▀▀▀▀ ▄ ▄▀ ▀▀ ▀█▀█▄▄█  ▀▀▄███▄█▄▀▀▄▄▄▄ ▀ ▄▄▀▀   ▄▄██▄▄▀▀█     
    #  ▄▄▄▄▄▄▄ █   ▄ ▄  ▄▄▄▄█▄██▀█ ▄ █▀ ▀▄  ▀▄  █▀▀▀▄  █ ▄ █ ▄▄      
    #  █ ▄▄▄ █ ▄ ▄ ▀▄▀  ▄█    ▄▀▄█▄▄▄█▄▀▀▄ ▄ ▀▀ ▀█▄▀▄▀▀█▄▄▄█▀▀█      
    #  █ ███ █ █▄▄▄ ▀▄▄ █▀█▄▀  ▀▄▀▀ ▄▄   ▄▄ ▄▄ █▀█▀▀  ███▄▄▀ █       
    #  █▄▄▄▄▄█ █▄▄▀    ███▀    ▄█▀  ▀▀█▀ ▄██▀ ▄▀▄▄▄▀██▄▄▄▄▀▀█▀▄      
    #          Google Tranlate is trash for this job btw                              