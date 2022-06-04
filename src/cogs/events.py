import nextcord
import nextcord.ext
from nextcord.ext import commands
import nextcord.utils as utils
import asyncio


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_message")
    async def delete_link_account(self, message):
        """
        Delete the messages sent in link-account channel.
        """
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(961640173463023646)
        target_bot = self.bot.get_user(960850854506815528)
        target_message = "I don't know of such a code, try again."

        if message.channel != channel: # Check if the channel is not link-account
            return

        if message.author.id in self.bot.owner_ids or message.author == self.bot.user: # Check if the message is by a team member
            return

        if message.author == target_bot:
            asyncio.sleep(15)
            await message.delete()
            return

        await asyncio.sleep(15)
        await message.delete()
        self.bot.logger.info(f"Deleted a message from {message.author} in {message.channel}")

    @commands.Cog.listener(name="on_message")
    async def pumpkin_listen(self, message):
        """
        DMs LazyPumpkin if a message contains 'pumpkin'
        """
        await self.bot.wait_until_ready()
        lazy_pumpkin = self.bot.get_user(691319007579471902)
        if message.author.id == self.bot.user.id:
            return

        if "pumpkin" in message.content:
            await lazy_pumpkin.send(f"{message.author} said \"pumpkin\" in a message.\nMessage Link: {message.jump_url}")


def setup(bot):
    bot.add_cog(Events(bot))