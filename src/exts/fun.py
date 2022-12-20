import nextcord
from nextcord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ban(self, ctx, member: nextcord.Member, *, reason: str = None):
        await ctx.reply(f'Banned {member} for "{reason}".', mention_author=False)

    @commands.command()
    async def kick(self, ctx, member: nextcord.Member, *, reason: str = None):
        await ctx.reply(f'Kicked {member} for "{reason}".', mention_author=False)


def setup(bot):
    bot.add_cog(Fun(bot))
