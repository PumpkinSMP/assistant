from pydactyl import PterodactylClient
from nextcord.ext import commands


class Pterodactyl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pterodactyl = PterodactylClient(
            self.bot.environ["PTERODACTYL_URL"],
            self.bot.environ["PTERODACTYL_KEY"],
        )

    @commands.command()
    @commands.cooldown(3, 5, commands.BucketType.user)
    async def list(self, ctx: commands.Context):
        server_id = self.bot.environ["M_ID"]
        self.pterodactyl.client.servers.send_console_command(server_id, "list")
        file = self.pterodactyl.client.servers.files.get_file_contents(
            server_id, "logs/latest.log"
        )
        # get last line of file
        # line = file.splitlines()[-1]
        await ctx.send(file.text.splitlines()[-1])


def setup(bot):
    bot.add_cog(Pterodactyl(bot))
