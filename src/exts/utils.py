import nextcord
from nextcord.ext import commands
from json import loads


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def parse_embed_json(self, json_file):
        embeds_json = loads(json_file)["embeds"]

        for embed_json in embeds_json:
            embed = nextcord.Embed().from_dict(embed_json)
            yield embed

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def esend(self, ctx, embed: str):
        with open(f"embeds/{embed}.json", "r") as file:
            embeds = self.parse_embed_json(file.read())
        embeds = list(embeds)
        if embed == "rules":
            for embed in embeds:
                embed.colour = nextcord.Colour.dark_theme()
        await ctx.send(embeds=embeds)


def setup(bot):
    bot.add_cog(Utils(bot))
