from nextcord.ext import commands
import nextcord


class Logs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def get_logs_channel(self, channel: str = None):
        channels = {"message": 1061902227565981738}
        return channels[channel]

    @commands.Cog.listener()
    async def on_message_delete(self, message: nextcord.Message):
        if message.channel.id in [1052178682426433600] and before.author.id in [
            960850854506815528
        ]:
            return
        channel = self.bot.get_channel(self.get_logs_channel("message"))
        embed = nextcord.Embed(
            title="Message Deleted", color=nextcord.Colour.from_rgb(47, 49, 54)
        )
        embed.add_field(
            name="Author",
            value=f"Mention: {message.author.mention}\nID: {message.author.id}",
            inline=False,
        )
        embed.add_field(
            name="Channel",
            value=f"Mention: {message.channel.mention}\nID: {message.channel.id}",
            inline=False,
        )
        embed.add_field(name="Message", value=f"```{message.content}```", inline=False)
        embed.set_author(name=message.author, icon_url=message.author.avatar.url)
        embed.set_footer(text=f"Message ID: {message.id} | Time: {message.created_at}")
        if message.attachments:
            await channel.send(embed=embed, attachments=message.attachments)
            return
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before: nextcord.Message, after: nextcord.Message):
        if before.channel.id in [1052178682426433600] and before.author.id in [
            960850854506815528
        ]:
            return
        channel = self.bot.get_channel(self.get_logs_channel("message"))
        embed = nextcord.Embed(
            title="Message Edited", color=nextcord.Colour.from_rgb(47, 49, 54)
        )
        embed.add_field(
            name="Author",
            value=f"Mention: {before.author.mention}\nID: {before.author.id}",
            inline=False,
        )
        embed.add_field(
            name="Channel",
            value=f"Mention: {before.channel.mention}\nID: {before.channel.id}",
            inline=False,
        )
        embed.add_field(name="Before", value=f"```{before.content}```", inline=False)
        embed.add_field(name="After", value=f"```{after.content}```", inline=False)
        embed.set_author(name=before.author, icon_url=before.author.avatar.url)
        embed.set_footer(text=f"Message ID: {before.id} | Time: {before.created_at}")
        if before.attachments:
            await channel.send(embed=embed, attachments=before.attachments)
            return
        await channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Logs(bot))
