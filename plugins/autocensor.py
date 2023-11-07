import re
from loguru import logger
from disnake import Message
from disnake.ext.plugins import Plugin

plugin = Plugin()

CONFIG = dict(
    delete_after_seconds=120,
    default_warning="You attempted to post a message that violates our DIMEs policy. For more information, please reach out to a board member.",
    triggers={
        "venmo": None,
        "shady": None,
        "funds": None,
        "alcohol": None,
        "pregame": None,
        "beer": None,
        "vodka": None,
        "binge": None,
        "fakes": None,
        "fake id": None,
    },
)

# Precompile trigger regexes
CONFIG["triggers"]: dict[re.Pattern, str] = {
    re.compile(pattern, re.IGNORECASE): (
        response if response else CONFIG["default_warning"]
    )
    for pattern, response in CONFIG["triggers"].items()
}


@plugin.load_hook()
async def register_intents():
    plugin.bot._connection._intents.message_content = True


@plugin.listener("on_message")
async def on_message(message: Message):
    if message.author.bot:
        return
    for pattern, response in CONFIG["triggers"].items():
        match = pattern.search(message.content)
        if match:
            await message.author.send(
                response,
                delete_after=CONFIG["delete_after_seconds"],
            )
            await message.delete()
            logger.success(f"Censored message from {message.author}")
            break


setup, teardown = plugin.create_extension_handlers()
