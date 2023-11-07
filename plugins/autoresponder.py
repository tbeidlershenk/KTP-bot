import re
from loguru import logger
from disnake import Message
from disnake.ext.commands import Bot
from disnake.ext.commands.cog import Cog
from disnake.ext.plugins import Plugin

plugin = Plugin()

CONFIG = dict(
    delete_after_seconds=120,
    default_response="Hello! If you're seeing this message, I was told to respond but don't have another response!",
    triggers={
        "brotherhood p(oin)?ts?": "Hello! Make sure you fill out the formal brotherhood point request found here:\n[Brotherhood Point Request Form](<https://forms.gle/qiJxytzr2PhuhESj7>)"
    },
)

# Precompile trigger regexes
CONFIG["triggers"]: dict[re.Pattern, str] = {
    re.compile(pattern, re.IGNORECASE): (
        response if response else CONFIG["default_response"]
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
            await message.reply(
                response,
                fail_if_not_exists=False,
                delete_after=CONFIG["delete_after_seconds"],
            )
            logger.success(f"Responded to {message.author}")
            break


setup, teardown = plugin.create_extension_handlers()
