import re
import json
from common import logger, bot_intents
import disnake
from disnake import Message
from disnake.ext.commands import Bot
from disnake.ext.commands.cog import Cog

CONFIG_PATH = "/app/data/autocensor.json"

class AutoCensor(Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            with open(CONFIG_PATH) as configfile:
                config = json.load(configfile)
        except FileNotFoundError:
            # Create empty config file if missing
            with open(CONFIG_PATH) as configfile:
                config = dict(delete_after_seconds=120, default_warning="", triggers={})
                json.dump(config, configfile)
        self.delete_after_seconds = config["delete_after_seconds"]
        self.default_warning = config["default_warning"]
        self.triggers: dict[re.Pattern, str] = {
            re.compile(pattern, re.IGNORECASE): (
                response if response else self.default_warning
            )
            for pattern, response in config["triggers"].items()
        }

    @Cog.listener("on_message")
    async def on_message(self, message: Message):
        if message.author.bot:
            return

        for pattern, response in self.triggers.items():
            match = pattern.search(message.content)
            if match:
                await message.author.send(
                    response,
                    delete_after=self.delete_after_seconds,
                )
                await message.delete()
                logger.info(f"Censored message from {message.author}")
                break


def setup(bot: Bot):
    bot.add_cog(AutoCensor(bot))
    bot_intents(bot).message_content = True
    bot_intents(bot).moderation = True
    

def teardown(bot: Bot):
    bot.remove_cog(AutoCensor.__cog_name__)
