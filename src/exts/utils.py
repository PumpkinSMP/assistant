import nextcord
from nextcord.ext import commands
import json
import io
import typing


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def parse_embed_json(self, json_file):
        embeds_json = json.loads(json_file)["embeds"]

        for embed_json in embeds_json:
            embed = nextcord.Embed().from_dict(embed_json)
            yield embed

    async def get_embed_from_message(
        self, ctx: commands.Context, message: nextcord.Message, index: int = 0
    ):
        embeds = message.embeds
        if not embeds:
            return await ctx.send("That message has no embeds.")
        index = max(min(index, len(embeds)), 0)
        embed = message.embeds[index]
        if embed.type == "rich":
            return embed
        return await ctx.send("That is not a rich embed.")

    @commands.group()
    @commands.has_permissions(administrator=True)
    async def embed(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @embed.command()
    @commands.has_permissions(administrator=True)
    async def send(self, ctx: commands.Context, embed: str):
        with open(f"embeds/{embed}.json", "r") as file:
            embeds = self.parse_embed_json(file.read())
        embeds = list(embeds)
        await ctx.send(embeds=embeds)

    @embed.command()
    @commands.has_permissions(administrator=True)
    async def download(
        self, ctx: commands.Context, message: nextcord.Message, index: int = 0
    ):
        embed = await self.get_embed_from_message(ctx, message, index)
        data = embed.to_dict()
        data = json.dumps(data, indent=4)
        fp = io.BytesIO(bytes(data, "utf-8"))
        await ctx.send(file=nextcord.File(fp, "embed.json"))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def say(
        self,
        ctx: commands.Context,
        destination: commands.Greedy[
            typing.Union[nextcord.TextChannel, nextcord.User]
        ] = None,
        *,
        message: str,
    ):
        if destination is None:
            destination = ctx.channel
        mentions = []
        if type(destination) is list:
            for dest in destination:
                await dest.send(message)
                mentions.append(dest.mention)
        else:
            await destination.send(message)
        await ctx.reply(
            f"Message sent to {str(mentions)[1:-1]}.",
            allowed_mentions=nextcord.AllowedMentions(
                users=False, roles=False, everyone=False, replied_user=True
            ),
            delete_after=5,
        )
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Utils(bot))
