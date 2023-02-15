import nextcord
from nextcord.ext import commands
import nextcord.utils
import exts.config as config


class Tickets(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = config.Config("config.json")
        self.config.load()
        if "tickets" not in self.config.data:
            self.config.data["tickets"] = {}
            self.config.save()

    async def new_ticket(self, member: nextcord.Member):
        self.config.load()
        category_id = self.config.data[str(member.guild.id)]["category_id"]
        if category_id is None:
            return
        category = self.bot.get_channel(category_id)
        if category is None:
            return
        ticket = await category.create_text_channel(f"{type}-{member.name}")
        await ticket.set_permissions(member, read_messages=True, send_messages=True)
        await ticket.set_permissions(member.guild.default_role, read_messages=False)
        support_role = self.config.data[str(member.guild.id)]["support_role"]
        await ticket.set_permissions(
            member.guild.get_role(support_role), read_messages=True
        )
        message = self.config.data[str(member.guild.id)]["message"]
        placeholders = {
            "member": member.mention,
            "support_role": member.guild.get_role(support_role).mention,
        }
        for placeholder, value in placeholders.items():
            message = message.replace(f"{{{placeholder}}}", value)
        if message is None:
            return
        await ticket.send(message)

    @commands.group()
    async def ticketm(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    # @ticket.command()
    # async def new(self, ctx: commands.Context, type: str):
    #     await ctx.send("Done.")

    @ticketm.command()
    @commands.has_permissions(manage_guild=True)
    async def category(self, ctx: commands.Context, category: nextcord.CategoryChannel):
        self.config.load()
        self.config.data["tickets"]["category_id"] = category.id
        self.config.save()
        await ctx.send(f"Ticket category set to {category.mention}")

    @ticketm.command()
    @commands.has_permissions(manage_guild=True)
    async def closedcategory(
        self, ctx: commands.Context, category: nextcord.CategoryChannel
    ):
        self.config.load()
        self.config.data["tickets"]["closed_category_id"] = category.id
        self.config.save()
        await ctx.send(f"Ticket closed category set to {category.mention}")

    @ticketm.command()
    @commands.has_permissions(manage_guild=True)
    async def message(self, ctx: commands.Context, *, message: str):
        self.config.load()
        self.config.data["tickets"]["message"] = message
        self.config.save()
        await ctx.send(f"Ticket message set to {message}")

    @ticketm.command()
    @commands.has_permissions(manage_guild=True)
    async def role(self, ctx: commands.Context, role: nextcord.Role):
        self.config.load()
        if ctx.guild.id not in self.config.data:
            self.config.data["tickets"] = {}
        self.config.data["tickets"]["support_role"] = role.id
        self.config.save()
        await ctx.send(f"Ticket support role set to {role.mention}.")

    @commands.command()
    async def ticket(self, ctx: commands.Context):
        await self.new_ticket(ctx.author)
        await ctx.send("Done.")

    @commands.command()
    async def close(self, ctx: commands.Context):
        if ctx.channel.id in self.config.data["tickets"]["tickets"]:
            support_role = nextcord.utils.get(
                ctx.guild.roles, id=self.config.data["tickets"]["support_role"]
            )
            closed_category = nextcord.utils.get(
                ctx.guild.categories,
                id=self.config.data["tickets"]["closed_category_id"],
            )
            await ctx.send("Closing ticket...")
            await ctx.channel.move(closed_category)
            await ctx.channel.set_permissions(support_role, read_messages=False)


def setup(bot: commands.Bot):
    bot.add_cog(Tickets(bot))
