import nextcord
from nextcord.ext import commands
import exts.config as config


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = config.Config("config.json")
        self.config.load()
        if "moderation" not in self.config.data:
            self.config.data["moderation"] = {}
            self.config.save()
        if "softmute" not in self.config.data["moderation"]:
            self.config.data["moderation"]["softmute"] = {}
            self.config.save()

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def softmute(self, ctx: commands.Context, member: nextcord.Member):
        self.config.load()
        if str(member.id) not in self.config.data["moderation"]["softmute"]:
            self.config.data["moderation"]["softmute"][str(member.id)] = {}
        self.config.data["moderation"]["softmute"][str(member.id)]["softmute"] = True
        self.config.save()
        await ctx.send(
            f"Soft-muted {member.mention}",
            allowed_mentions=nextcord.AllowedMentions.none(),
        )

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def softunmute(self, ctx: commands.Context, member: nextcord.Member):
        self.config.load()
        if str(member.id) in self.config.data["moderation"]["softmute"]:
            if "softmute" in self.config.data["moderation"]["softmute"][str(member.id)]:
                del self.config.data["moderation"]["softmute"][str(member.id)][
                    "softmute"
                ]
                self.config.save()
                await ctx.send(
                    f"Soft-unmuted {member.mention}",
                    allowed_mentions=nextcord.AllowedMentions.none(),
                )
            else:
                await ctx.send(f"{member.mention} is not soft-muted")
        else:
            await ctx.send(f"{member.mention} is not soft-muted")

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.author.bot:
            return
        self.config.load()
        if str(message.author.id) in self.config.data["moderation"]["softmute"]:
            if (
                "softmute"
                in self.config.data["moderation"]["softmute"][str(message.author.id)]
            ):
                await message.delete()
                await message.author.send(
                    "We are having some issues processing your message. Please try again later."
                )

    @commands.Cog.listener()
    async def on_message_edit(self, before: nextcord.Message, after: nextcord.Message):
        if before.author.bot:
            return
        self.config.load()
        if str(before.author.id) in self.config.data["moderation"]["softmute"]:
            if (
                "softmute"
                in self.config.data["moderation"]["softmute"][str(before.author.id)]
            ):
                await after.delete()
                await before.author.send(
                    "We are having some issues processing your message. Please try again later."
                )


def setup(bot):
    bot.add_cog(Moderation(bot))
