import re
import json
from common import logger, bot_intents
from disnake import Message
from disnake.ext.commands import Bot
from disnake.ext.commands.cog import Cog

CONFIG_PATH = "/app/data/autoresponder.json"


class AutoResponder(Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            with open(CONFIG_PATH) as configfile:
                config = json.load(configfile)
        except FileNotFoundError:
            # Create empty config file if missing
            with open(CONFIG_PATH) as configfile:
                config = dict(delete_after_seconds=120, triggers={})
                json.dump(config, configfile)
        self.delete_after_seconds = config["delete_after_seconds"]
        self.triggers: dict[re.Pattern, str] = {
            re.compile(pattern, re.IGNORECASE): response
            for pattern, response in config["triggers"].items()
        }

    @Cog.listener("on_message")
    async def on_message(self, message: Message):
        if message.author.bot:
            return

        for pattern, response in self.triggers.items():
            match = pattern.search(message.content)
            if match:
                logger.info(f"Responded to {message.author}")
                await message.reply(
                    response,
                    fail_if_not_exists=False,
                    delete_after=self.delete_after_seconds,
                )
                break


def setup(bot: Bot):
    bot.add_cog(AutoResponder(bot))
    bot_intents(bot).message_content = True


def teardown(bot: Bot):
    bot.remove_cog(AutoResponder.__cog_name__)
