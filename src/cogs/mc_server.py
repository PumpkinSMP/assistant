import nextcord
from nextcord import SlashOption
from nextcord.ext import commands
import aiohttp


class MCServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command()
    async def vote(self, interaction: nextcord.Interaction):
        voting_links = [
            "https://bit.ly/PumpkinVote1",
            "https://bit.ly/PumpkinVote2",
            "https://bit.ly/PumpkinVote3",
            "https://bit.ly/PumpkinVote4",
            "https://bit.ly/PumpkinVote5",
        ]
        embed = nextcord.Embed(
            title="Vote for PumpkinSMP", color=nextcord.Color.green()
        )
        embed.description = "Vote for PumpkinSMP to get awesome rewards like a special rank and voting crate keys!"
        embed.add_field(name="Voting Link 1", value=voting_links[0])
        embed.add_field(name="Voting Link 2", value=voting_links[1])
        embed.add_field(name="Voting Link 3", value=voting_links[2])
        embed.add_field(name="Voting Link 4", value=voting_links[3])
        embed.add_field(name="Voting Link 5", value=voting_links[4])
        embed.set_footer(
            text=f"Requested by {interaction.user}",
            icon_url=interaction.user.display_avatar.url,
        )
        await interaction.send(embed=embed)

    @nextcord.slash_command()
    async def server(self, interaction: nextcord.Interaction):
        pass

    @server.subcommand()
    async def status(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.mcsrvstat.us/2/play.pumpkinsmp.gq"
            ) as response:
                data = await response.json()
                status = ""
                if data["online"] == True:
                    status = "Online"
                else:
                    status = "Offline"
                color = ""
                if status == "Online":
                    color = nextcord.Color.green()
                else:
                    color = nextcord.Color.red()

                embed = nextcord.Embed(
                    title=f"PumpkinSMP Status | {status}", color=color
                )
                embed.add_field(name="Status", value=status)
                embed.add_field(name="MOTD", value=data["motd"]["clean"][0])
                embed.add_field(name="Online Players", value=data["players"]["online"])
                embed.add_field(name="Max Players", value=data["players"]["max"])
                await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(MCServer(bot=bot))
