from nextcord.ext import commands
import nextcord


class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def suggest(self, ctx: commands.Context, *, suggestion: str):
        suggestion_channel = ctx.guild.get_channel(934852695385337866)
        new_id = self.bot.db.get_new_suggestion_id()
        embed = nextcord.Embed(
            title=f"Suggestion #{new_id}", colour=nextcord.Colour.yellow()
        )
        embed.description = suggestion
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        embed.set_footer(text=f"User ID: {ctx.author.id} | Suggestion ID: #{new_id}")
        message = await suggestion_channel.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        await message.add_reaction("💬")
        self.bot.db.insert_suggestion(
            ctx.author.id, suggestion, "pending", message.jump_url
        )
        await ctx.send("Your suggestion has been sent!", delete_after=10)

    @commands.group()
    async def suggestion(self, ctx: commands.Context):
        pass

    @suggestion.command()
    async def info(self, ctx: commands.Context, suggestion_id: int):

        suggestion_info = self.bot.db.get_suggestion(suggestion_id)
        if suggestion_info is None:
            await ctx.send("That suggestion does not exist!", delete_after=10)
            return
        embed = nextcord.Embed(title=f"Suggestion #{suggestion_id}")
        if suggestion_info[3] == "approved":
            embed.colour = nextcord.Colour.green()
        elif suggestion_info[3] == "rejected":
            embed.colour = nextcord.Colour.red()
        else:
            embed.colour = nextcord.Colour.yellow()
        embed.set_author(
            name=ctx.guild.get_member(suggestion_info[1]),
            icon_url=ctx.guild.get_member(suggestion_info[1]).avatar.url,
        )
        embed.set_footer(
            text=f"User ID: {suggestion_info[1]} | Suggestion ID: #{suggestion_id}"
        )
        embed.description = suggestion_info[2]
        embed.add_field(name="Status", value=suggestion_info[3].capitalize())
        embed.add_field(name="Link", value=f"[Jump]({suggestion_info[4]})")
        if suggestion_info[5] is not None:
            embed.add_field(name="Note", value=suggestion_info[5])
        await ctx.send(embed=embed)

    @suggestion.command()
    @commands.has_guild_permissions(administrator=True)
    async def approve(
        self, ctx: commands.Context, suggestion_id: int, *, note: str = None
    ):

        suggestion_info = self.bot.db.get_suggestion(suggestion_id)
        if suggestion_info is None:
            await ctx.send("That suggestion does not exist!", delete_after=10)
            return
        if suggestion_info[3] != "pending":
            await ctx.send("That suggestion is not pending!", delete_after=10)
            return
        suggestion_msg = await ctx.guild.get_channel(934852695385337866).fetch_message(
            suggestion_info[4].split("/")[-1]
        )
        embed = suggestion_msg.embeds[0]
        embed.colour = nextcord.Colour.green()
        embed.add_field(name="Status", value="Approved")
        if note is not None:
            embed.add_field(name="Note", value=note)
        self.bot.db.update_suggestion(suggestion_id, "approved", note)
        await suggestion_msg.edit(embed=embed)
        await suggestion_msg.remove_reaction("💬", self.bot.user)
        if suggestion_msg.thread is not None:
            await suggestion_msg.thread.send(
                "Locking thread as the suggestion has been rejected! Please create a new thread if you have any questions!"
            )
            await suggestion_msg.thread.edit(locked=True)
        await ctx.send("Suggestion approved!")

    @suggestion.command()
    @commands.has_guild_permissions(administrator=True)
    async def reject(self, ctx: commands.Context, suggestion_id: int, *, note: str = None):

        suggestion_info = self.bot.db.get_suggestion(suggestion_id)
        if suggestion_info is None:
            await ctx.send("That suggestion does not exist!", delete_after=10)
            return
        if suggestion_info[3] != "pending":
            await ctx.send("That suggestion is not pending!", delete_after=10)
            return
        suggestion_msg = await ctx.guild.get_channel(934852695385337866).fetch_message(
            suggestion_info[4].split("/")[-1]
        )
        embed = suggestion_msg.embeds[0]
        embed.colour = nextcord.Colour.red()
        embed.add_field(name="Status", value="Rejected")
        if note is not None:
            embed.add_field(name="Note", value=note)
        self.bot.db.update_suggestion(suggestion_id, "rejected", note)
        await suggestion_msg.edit(embed=embed)
        await suggestion_msg.remove_reaction("💬", self.bot.user)
        if suggestion_msg.thread is not None:
            await suggestion_msg.thread.send(
                "Locking thread as the suggestion has been rejected! Please create a new thread if you have any questions!"
            )
            await suggestion_msg.thread.edit(locked=True)
        await ctx.send("Suggestion rejected!")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: nextcord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return
        if payload.channel_id != 934852695385337866:
            return
        if payload.emoji.name != "💬":
            return

        message = await self.bot.get_channel(payload.channel_id).fetch_message(
            payload.message_id
        )
        if message.author.id != self.bot.user.id:
            return
        if message.thread is not None:
            await message.remove_reaction(payload.emoji, payload.member)
            return
        suggestion_info = self.bot.db.get_suggestion(
            int(message.embeds[0].title.split("#")[1])
        )
        if suggestion_info[3] != "pending":
            return
        thread = await message.create_thread(name=f"Suggestion #{suggestion_info[0]}")
        await thread.send(
            f"{message.guild.get_member(payload.user_id).mention} has started a thread for this suggestion!"
        )
        await thread.add_user(message.guild.get_member(suggestion_info[1]))
        await message.remove_reaction(payload.emoji, payload.member)


def setup(bot):
    bot.add_cog(Suggestions(bot))
