from nextcord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 15)
    async def hamsterroll(self, ctx):
        await ctx.reply("<a:hamster_roll:1006575771487322182>", mention_author=False)


def setup(bot):
    bot.add_cog(Fun(bot=bot))
