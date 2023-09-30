from common import logger
from typing import Optional
from disnake import Intents, client
from disnake import Member
from disnake import Message
from disnake.ext.commands import slash_command, Bot
from disnake.ext.commands.cog import Cog

triggers = ["brotherhood", "point", "form"]
form = "https://forms.gle/qiJxytzr2PhuhESj7"

class BrotherhoodPoints(Cog):

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener("on_message")
    async def on_message(self, message):
        if message.author.bot:
            return

        for keyword in triggers:
            if keyword in message.content:
                logger.info("Sent brotherhood form")
                await message.ctx.send(form)
                break
    
        
def setup(bot: Bot):
    bot.add_cog(BrotherhoodPoints(bot))

def teardown(bot: Bot):
    bot.remove_cog(BrotherhoodPoints.__cog_name__)