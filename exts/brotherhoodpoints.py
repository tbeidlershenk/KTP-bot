from common import logger, bot_intents
from disnake.ext.commands import Bot
from disnake.ext.commands.cog import Cog

triggers = ["brotherhood point", "brotherhood points", "brotherhood pts"]
form = r"https://forms.gle/qiJxytzr2PhuhESj7"
response = f"The brotherhood point request form can be found here: {form}"


class BrotherhoodPoints(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener("on_message")
    async def on_message(self, message):
        if message.author.bot:
            return

        for trigger in triggers:
            if trigger.lower() in message.content.lower():
                logger.info(f"Sent brotherhood form to {message.author}")
                await message.channel.send(response)
                break


def setup(bot: Bot):
    bot.add_cog(BrotherhoodPoints(bot))
    bot_intents(bot).message_content = True

def teardown(bot: Bot):
    bot.remove_cog(BrotherhoodPoints.__cog_name__)
