import nextcord
from nextcord.ext import commands
import exts.config as config
import nextcord.utils


class ReactRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = config.Config("reactroles.json")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return
        self.config.load()
        if str(payload.message_id) in self.config.data:
            if str(payload.emoji) in self.config.data[str(payload.message_id)]:
                role = nextcord.utils.get(
                    payload.member.guild.roles,
                    id=self.config.data[str(payload.message_id)][str(payload.emoji)],
                )
                await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild: nextcord.Guild = nextcord.utils.get(self.bot.guilds, id=payload.guild_id)
        member: nextcord.Member = nextcord.utils.get(guild.members, id=payload.user_id)
        if member.bot:
            return
        self.config.load()
        if str(payload.message_id) in self.config.data:
            if str(payload.emoji) in self.config.data[str(payload.message_id)]:
                role = nextcord.utils.get(
                    guild.roles,
                    id=self.config.data[str(payload.message_id)][str(payload.emoji)],
                )
                await member.remove_roles(role)

    @commands.group()
    @commands.has_permissions(manage_roles=True)
    async def rr(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @rr.command()
    @commands.has_permissions(manage_roles=True)
    async def add(
        self,
        ctx: commands.Context,
        message: nextcord.Message,
        emoji: str,
        role: nextcord.Role,
    ):
        self.config.load()
        if str(message.id) not in self.config.data:
            self.config.data[str(message.id)] = {}
        self.config.data[str(message.id)][emoji] = role.id
        self.config.save()
        await message.add_reaction(emoji)
        await ctx.send(
            f"Added reaction role {role.mention} to {message.jump_url}",
            allowed_mentions=nextcord.AllowedMentions.none(),
        )

    @rr.command()
    @commands.has_permissions(manage_roles=True)
    async def delete(
        self, ctx: commands.Context, message: nextcord.Message, emoji: str
    ):
        self.config.load()
        if str(message.id) in self.config.data:
            if emoji in self.config.data[str(message.id)]:
                del self.config.data[str(message.id)][emoji]
                self.config.save()
                await message.clear_reaction(emoji)
                await ctx.send(f"Deleted reaction role {emoji} from {message.jump_url}")
            else:
                await ctx.send(f"Emoji {emoji} not found")
        else:
            await ctx.send(f"Message {message.jump_url} not found")

    @rr.command()
    @commands.has_permissions(manage_roles=True)
    async def deleteall(self, ctx: commands.Context, message: nextcord.Message):
        self.config.load()
        if str(message.id) in self.config.data:
            del self.config.data[str(message.id)]
            self.config.save()
            await message.clear_reactions()
            await ctx.send(f"Deleted all reaction roles from {message.jump_url}")
        else:
            await ctx.send(f"Message {message.jump_url} not found")

    @rr.command()
    @commands.has_permissions(manage_roles=True)
    async def list(self, ctx: commands.Context, message: nextcord.Message):
        self.config.load()
        if str(message.id) in self.config.data:
            embed = nextcord.Embed(
                title=f"Reaction Roles for {message.id}", color=nextcord.Color.blurple()
            )
            for emoji, role_id in self.config.data[str(message.id)].items():
                role: nextcord.Role = nextcord.utils.get(ctx.guild.roles, id=role_id)
                print(emoji, role_id)
                embed.add_field(name=emoji, value=role.mention, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Message {message.jump_url} not found")

    @rr.command()
    @commands.has_permissions(manage_roles=True)
    async def listall(self, ctx: commands.Context):
        self.config.load()
        embed = nextcord.Embed(
            title="All Reaction Roles", color=nextcord.Color.blurple()
        )
        uknnown_messages = []
        for message_id, data in self.config.data.items():
            try:
                message = await ctx.fetch_message(message_id)
                embed.add_field(
                    name=message.jump_url, value=", ".join(data.keys()), inline=False
                )
            except nextcord.errors.NotFound:
                uknnown_messages.append(message_id)
        if len(uknnown_messages) != 0:
            embed.description = (
                f"Some messages were unable to be fetched:\n{uknnown_messages}"
            )
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(ReactRoles(bot))
