import nextcord
from nextcord.ext import commands
import json
import io
import typing
import aiohttp
import exts.config as cfg
import nextcord.utils


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

    @commands.command()
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def ubdict(self, ctx: commands.Context, *, word: str):
        """Search for a word in the Urban Dictionary"""
        params = {"term": word}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.urbandictionary.com/v0/define", params=params
            ) as response:
                data = await response.json()
        if not data["list"]:
            return await ctx.send("No results found.")
        embed = nextcord.Embed(
            title=data["list"][0]["word"],
            description=data["list"][0]["definition"],
            url=data["list"][0]["permalink"],
            color=nextcord.Color.green(),
        )
        embed.set_footer(
            text=f"👍 {data['list'][0]['thumbs_up']} | 👎 {data['list'][0]['thumbs_down']} | Powered by: Urban Dictionary"
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def dict(self, ctx: commands.Context, *, word: str):
        """Search for a word in the Oxford Dictionary"""
        app_id = self.bot.environ["OXFORD_APP_ID"]
        app_key = self.bot.environ["OXFORD_APP_KEY"]
        headers = {"app_id": app_id, "app_key": app_key}
        url = "https://od-api.oxforddictionaries.com/api/v2/entries/en-us"
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{url}/{word.lower()}", headers=headers
            ) as response:
                data = await response.json()
        if not data:
            return await ctx.send("No results found.")
        embed = nextcord.Embed(
            title=data["results"][0]["word"],
            description=data["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][
                0
            ]["definitions"][0],
            color=nextcord.Color.green(),
        )
        embed.set_footer(text=f"Powered by: Oxford Languages")
        await ctx.send(embed=embed)

    @commands.group()
    @commands.has_permissions(administrator=True)
    async def changelog(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @changelog.command()
    @commands.has_permissions(administrator=True)
    async def new(self, ctx: commands.Context, type: str, *, message: str):
        if type not in ["minecraft", "discord", "global", "website"]:
            return await ctx.send("Invalid type.")
        config = cfg.Config("config.json")
        config.load()
        if not config.data["changelog_channel"]:
            return await ctx.send("Changelog channel not set.")
        channel: nextcord.Channel = nextcord.utils.get(
            ctx.guild.channels,
            id=config.data["changelog_channel"],
        )
        if not channel:
            return await ctx.send("Changelog channel not found.")
        ping_role: nextcord.Role = nextcord.utils.get(
            ctx.guild.roles, id=config.data["ping_role"]
        )
        embed = nextcord.Embed(
            title=f"{type.title()} Changelog",
            description=message,
            color=nextcord.Color.green(),
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        if type == "minecraft":
            embed.set_thumbnail(url="https://i.ibb.co/YpKPWdS/minecraft-logo-1022.png")
        elif type == "discord":
            embed.set_thumbnail(
                url="https://i.ibb.co/fnt93Gp/discord-logo-png-7617.png"
            )
        elif type == "website":
            embed.set_thumbnail(url="https://i.ibb.co/tZGCmhx/logo-websites-31322.png")
        elif type == "global":
            embed.set_thumbnail(url="https://i.ibb.co/qWbLvbK/pumpkinsmp-bot-logo.png")
        embed.set_footer(text=f"Timestamp: {ctx.message.created_at}")
        if ctx.message.attachments:
            embed.set_image(url=ctx.message.attachments[0].url)
        if not ping_role:
            return await channel.send(embed=embed)
        await channel.send(ping_role.mention, embed=embed)

    @changelog.command()
    @commands.has_permissions(administrator=True)
    async def channel(self, ctx: commands.Context, channel: nextcord.TextChannel):
        config = cfg.Config("config.json")
        config.load()
        config.data["changelog_channel"] = channel.id
        config.save()
        await ctx.send(f"Changelog channel set to {channel.mention}.")

    @changelog.command()
    @commands.has_permissions(administrator=True)
    async def ping(self, ctx: commands.Context, role: nextcord.Role):
        config = cfg.Config("config.json")
        config.load()
        config.data["ping_role"] = role.id
        config.save()
        await ctx.send(f"Ping role set to {role.mention}.")

    @commands.Cog.listener(name="on_message")
    async def auto_publish(self, message: nextcord.Message):
        channels = [935419279963205662, 1056600527053525083, 935419748446007346]
        if message.channel.id in channels:
            await message.publish()


def setup(bot):
    bot.add_cog(Utils(bot))
