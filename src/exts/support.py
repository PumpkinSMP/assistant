from nextcord.ext import commands
import nextcord
import aiohttp


class Support(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.url = "http://api.brainshop.ai/get"

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.channel.id not in [934852605702729748]:
            return
        if message.author.id == self.bot.user.id:
            return


def setup(bot: commands.Bot):
    bot.add_cog(Support(bot))
