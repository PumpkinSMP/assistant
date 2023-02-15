import nextcord
from nextcord.ext import commands


class HelpCommand(commands.HelpCommand):
    """
    Help command for bot.
    """

    def footer(self):
        """
        Footer for embeds in help command.
        """
        return f"?{self.invoked_with} [command] for more information."

    async def get_command_signature(self, command):
        """
        Get the signature of a command.
        """
        return f"```?{command.qualified_name} {command.signature}```"

    async def send_cog_help(self, cog):
        """
        Send the help for a specific cog.
        """
        embed = nextcord.Embed(
            title=f"**{cog.qualified_name}** Commands", colour=nextcord.Colour.blue()
        )
        if cog.description:
            embed.description = cog.description

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            embed.add_field(
                name=command.qualified_name,
                value=command.short_doc or "No description provided.",
            )

        embed.set_footer(text=self.footer())
        await self.context.reply(embed=embed)

    async def send_command_help(self, command):
        """
        Send the help for a specific command.
        """
        embed = nextcord.Embed(
            title=command.qualified_name, colour=nextcord.Colour.blue()
        )
        if command.help:
            embed.description = command.help

        embed.add_field(
            name="Signature", value=await self.get_command_signature(command)
        )
        embed.set_footer(text=self.footer())
        await self.context.reply(embed=embed)

    async def send_bot_help(self, mapping):
        """
        Send the help for the bot.
        """
        embed = nextcord.Embed(title="Ball Help Manual", colour=nextcord.Colour.blue())
        description = self.context.bot.description
        if description:
            embed.description = description

        for cog, commands in mapping.items():
            if not cog:
                continue
            filtered = await self.filter_commands(commands, sort=True)
            if filtered:
                value = "\t".join(f"`{i.name}`" for i in commands)
                embed.add_field(name=cog.qualified_name, value=value)
        embed.set_footer(text=self.footer())
        await self.context.reply(embed=embed)

    async def send_error_message(self, error):
        embed = nextcord.Embed(
            title="Error", description=error, colour=nextcord.Colour.blue()
        )
        await self.context.reply(embed=embed)


def setup(bot):
    bot.help_command = HelpCommand()
