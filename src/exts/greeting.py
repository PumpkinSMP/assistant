import nextcord
from nextcord.ext import commands
import exts.config as config


class Greeting(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = config.Config("config.json")
        self.config.load()
        if "greeting" not in self.config.data:
            self.config.data["greeting"] = {}
            self.config.save()
        if "welcome" not in self.config.data["greeting"]:
            self.config.data["greeting"]["welcome"] = {}
            self.config.save()
        if "farewell" not in self.config.data["greeting"]:
            self.config.data["greeting"]["farewell"] = {}
            self.config.save()

    async def greet(self, member: nextcord.Member, type: str):
        """
        Greets a new member or says farewell to a departing member.
        """
        if type == "join":
            channel = self.bot.get_channel(
                self.config.data["greeting"]["welcome"]["channel"]
            )
            message = self.config.data["greeting"]["welcome"]["message"]
        elif type == "leave":
            channel = self.bot.get_channel(
                self.config.data["greeting"]["farewell"]["channel"]
            )
            message = self.config.data["greeting"]["farewell"]["message"]
        else:
            return
        placeholders = {
            "{member}": member.mention,
            "{username}": member.name,
            "{discriminator}": member.discriminator,
            "{id}": member.id,
            "{guild}": member.guild.name,
            "{membercount}": member.guild.member_count,
        }
        for placeholder, value in placeholders.items():
            message = message.replace(str(placeholder), str(value))
        await channel.send(message)

    @commands.group()
    @commands.has_permissions(manage_guild=True)
    async def welcome(self, ctx: commands.Context):
        """
        Group command for setting up the welcome message.
        """
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @welcome.command()
    @commands.has_permissions(manage_guild=True)
    async def wchannel(self, ctx: commands.Context, channel: nextcord.TextChannel):
        """
        Sets the channel for the welcome message.
        """
        self.config.data["greeting"]["welcome"]["channel"] = channel.id
        self.config.save()
        await ctx.send("Welcome channel set.")

    @welcome.command()
    @commands.has_permissions(manage_guild=True)
    async def wmessage(self, ctx: commands.Context, *, message: str):
        """
        Sets the message for the welcome message.
        """
        self.config.data["greeting"]["welcome"]["message"] = message
        self.config.save()
        await ctx.send("Welcome message set.")

    @welcome.command()
    @commands.has_permissions(manage_guild=True)
    async def wsimulate(self, ctx: commands.Context):
        """
        Simulates the welcome message.
        """
        await self.greet(ctx.author, "join")

    @commands.group()
    @commands.has_permissions(manage_guild=True)
    async def farewell(self, ctx: commands.Context):
        """
        Group command for setting up the farewell message.
        """
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @farewell.command()
    @commands.has_permissions(manage_guild=True)
    async def fchannel(self, ctx: commands.Context, channel: nextcord.TextChannel):
        """
        Sets the channel for the farewell message.
        """
        self.config.data["greeting"]["farewell"]["channel"] = channel.id
        self.config.save()
        await ctx.send("Farewell channel set.")

    @farewell.command()
    @commands.has_permissions(manage_guild=True)
    async def fmessage(self, ctx: commands.Context, *, message: str):
        """
        Sets the message for the farewell message.
        """
        self.config.data["greeting"]["farewell"]["message"] = message
        self.config.save()
        await ctx.send("Farewell message set.")

    @farewell.command()
    @commands.has_permissions(manage_guild=True)
    async def fsimulate(self, ctx: commands.Context):
        """
        Simulates the farewell message.
        """
        await self.greet(ctx.author, "leave")

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        await self.greet(member, "join")

    @commands.Cog.listener()
    async def on_member_remove(self, member: nextcord.Member):
        await self.greet(member, "leave")


def setup(bot: commands.Bot):
    bot.add_cog(Greeting(bot))
