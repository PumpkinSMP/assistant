import nextcord
from nextcord.ext import commands
from nextcord import SlashOption


class FakeMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[981510059181883402])
    async def bon(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(
            required=True, description="Member to ban"
        ),
        reason: str = SlashOption(required=False),
    ):
        await interaction.send(f'Banned {member} for "{reason}".')

    @nextcord.slash_command(guild_ids=[981510059181883402])
    async def kock(
        self,
        interaction,
        member: nextcord.Member = SlashOption(
            required=True, description="Member to kick"
        ),
        reason: str = SlashOption(required=False),
    ):
        await interaction.send(f'Kicked {member} for "{reason}".')


def setup(bot):
    bot.add_cog(FakeMod(bot=bot))
