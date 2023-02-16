from nextcord.ext import commands
import nextcord
import exts.config as config


class Reports(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = config.Config("config.json")

    @commands.command()
    async def report(
        self, ctx: commands.Context, member: nextcord.Member, *, reason: str
    ):
        """Report a member to the server staff."""
        await ctx.message.delete()
        if len(reason) < 15:
            return await ctx.send(
                "The reason must be at least 15 characters long.", delete_after=3
            )
        self.config.load()
        if "report_bans" in self.config.data:
            if ctx.author.id in self.config.data["report_bans"]:
                return await ctx.send(
                    "You are not allowed to use this command.", delete_after=3
                )
        embed = nextcord.Embed(
            title="New Member Report",
            description=f"A member has been reported.",
            color=nextcord.Color.blue(),
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(
            name="Reported Member",
            value=f"{member.mention} [{member.id}]",
            inline=False,
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(
            text=f"Reported by {ctx.author} [{ctx.author.id}]",
            icon_url=ctx.author.avatar.url,
        )
        channel = self.bot.get_channel(self.config.data["reports_channel"])
        if len(ctx.message.attachments) > 10:
            return await ctx.send("You can only send 10 attachments at a time.")
        files = [await attachment.to_file() for attachment in ctx.message.attachments]
        await channel.send(embed=embed, files=files)
        await ctx.author.send("The report has been sent.")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setreportchannel(
        self, ctx: commands.Context, channel: nextcord.TextChannel
    ):
        """Set the channel where reports will be sent."""
        self.config.load()
        self.config.data["reports_channel"] = channel.id
        self.config.save()
        await ctx.send(f"Reports will now be sent to {channel.mention}.")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def reportban(self, ctx: commands.Context, member: nextcord.Member):
        """Ban a member from using the report command."""
        self.config.load()
        if "report_bans" not in self.config.data:
            self.config.data["report_bans"] = []
        self.config.data["report_bans"].append(member.id)
        self.config.save()
        await ctx.send(f"{member.mention} can no longer use the report command.")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def reportunban(self, ctx: commands.Context, member: nextcord.Member):
        """Unban a member from using the report command."""
        self.config.load()
        if "report_bans" not in self.config.data:
            self.config.data["report_bans"] = []
        if member.id not in self.config.data["report_bans"]:
            return await ctx.send(
                f"{member.mention} is not banned from using the report command."
            )
        self.config.data["report_bans"].remove(member.id)
        self.config.save()
        await ctx.send(f"{member.mention} can now use the report command again.")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def reportbans(self, ctx: commands.Context):
        """List all members banned from using the report command."""
        self.config.load()
        if "report_bans" not in self.config.data:
            self.config.data["report_bans"] = []
        if len(self.config.data["report_bans"]) == 0:
            return await ctx.send(
                "There are no members banned from using the report command."
            )
        embed = nextcord.Embed(
            title="Report Bans",
            description="\n".join(
                [f"<@{member}>" for member in self.config.data["report_bans"]]
            ),
            color=nextcord.Color.red(),
        )
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Reports(bot))
