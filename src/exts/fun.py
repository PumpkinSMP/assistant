import asyncio
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

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def spamping(
        self,
        ctx: commands.Context,
        member: nextcord.Member,
        times: int,
        *,
        message: str = None,
    ):
        for i in range(times):
            if message:
                await ctx.send(f"{member.mention}: {message}")
                await asyncio.sleep(1)
            else:
                await ctx.send(member.mention)
                await asyncio.sleep(1)


def setup(bot):
    bot.add_cog(Fun(bot))
