import nextcord
import nextcord.ext
from nextcord.ext import commands
import nextcord.utils as utils
import asyncio


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_message")
    async def pumpkin_listen(self, message):
        """
        DMs LazyPumpkin if a message contains 'pumpkin'
        """
        await self.bot.wait_until_ready()
        ignore_channel_ids = [962053647116664953, 934836840568074240]
        lazy_pumpkin = self.bot.get_user(691319007579471902)
        if message.author.id == self.bot.user.id:
            return

        if message.channel.id in ignore_channel_ids:
            return

        if "pumpkin" in message.content.lower():
            await lazy_pumpkin.send(f"{message.author} said \"pumpkin\" in a message.\nMessage Link: {message.jump_url}")


def setup(bot):
    bot.add_cog(Events(bot))