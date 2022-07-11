from nextcord.ext import commands
import aiohttp
from pydactyl import PterodactylClient
import nextcord


class MCServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api = PterodactylClient(
            "http://144.24.143.226:8081", self.bot.env["PTERO_API"]
        )

    @commands.command()
    async def vote(self, ctx):
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
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.display_avatar.url,
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.group()
    async def server(self, ctx):
        pass

    @server.command()
    @commands.has_role(994553004596412486)
    async def start(self, ctx):
        try:
            async with ctx.typing():
                servers = self.api.client.servers.list_servers()
                srv_id = servers[0]["attributes"]["identifier"]
                self.api.client.servers.send_power_action(srv_id, "start")
            await ctx.send("Starting server.")
        except:
            await ctx.send("Failed to start server.")

    @server.command()
    @commands.has_role(981560939415478372)
    async def stop(self, ctx):
        try:
            async with ctx.typing():
                servers = self.api.client.servers.list_servers()
                srv_id = servers[0]["attributes"]["identifier"]
                self.api.client.servers.send_power_action(srv_id, "stop")
            await ctx.send("Stopping server.")
        except:
            await ctx.send("Failed to stop server.")

    @server.command()
    @commands.has_role(981560939415478372)
    async def kill(self, ctx):
        try:
            async with ctx.typing():
                servers = self.api.client.servers.list_servers()
                srv_id = servers[0]["attributes"]["identifier"]
                self.api.client.servers.send_power_action(srv_id, "kill")
            await ctx.send("Killed server.")
        except:
            await ctx.send("Failed to kill server.")

    @server.command()
    @commands.has_role(981560939415478372)
    async def restart(self, ctx):
        try:
            async with ctx.typing():
                servers = self.api.client.servers.list_servers()
                srv_id = servers[0]["attributes"]["identifier"]
                self.api.client.servers.send_power_action(srv_id, "restart")
            await ctx.send("Restarting server.")
        except:
            await ctx.send("Failed to restart server.")


def setup(bot):
    bot.add_cog(MCServer(bot=bot))
