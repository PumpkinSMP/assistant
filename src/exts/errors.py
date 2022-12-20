import nextcord
from nextcord.ext import commands, application_checks


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(
        self, interaction: nextcord.Interaction, error
    ):
        """
        Error handling for the most common errors.
        """
        # Application Commands Error Handling
        if isinstance(error, application_checks.errors.ApplicationMissingPermissions):
            embed = nextcord.Embed(
                title="Missing Permissions", colour=nextcord.Colour.red()
            )
            embed.description = (
                "You do not have required permission(s) to execute this command."
            )
            for permission in error.missing_permissions:
                embed.add_field(name="Missing Permission", value=permission)
            await interaction.send(embed=embed)

        elif isinstance(
            error, application_checks.errors.ApplicationBotMissingPermissions
        ):
            embed = nextcord.Embed(
                title="Missing Permissions", colour=nextcord.Colour.red()
            )
            embed.description = (
                "I do not have required permission(s) to execute this command."
            )
            for permission in error.missing_permissions:
                embed.add_field(name="Missing Permission", value=permission)
            await interaction.send(embed=embed)

        elif isinstance(error, application_checks.errors.ApplicationCheckAnyFailure):
            errors = error.errors
            missing_permissions_errors = []
            missing_role_errors = []
            missing_permissions = []
            missing_roles = []

            for error in errors:
                if isinstance(
                    error, application_checks.errors.ApplicationMissingPermissions
                ):
                    missing_permissions_errors.append(error)
                elif isinstance(
                    error, application_checks.errors.ApplicationMissingRole
                ):
                    missing_role_errors.append(error)

            embed = nextcord.Embed(
                title="Missing Requirements", colour=nextcord.Colour.red()
            )
            embed.description = (
                "You do not meet the requirements to execute this command."
            )

            if len(missing_permissions_errors) > 0:
                for error in missing_permissions_errors:
                    missing_permissions.append(error.missing_permissions[0])

            if len(missing_permissions_errors) > 0:
                for error in missing_role_errors:
                    missing_roles.append(error.missing_role)

            if len(missing_permissions_errors) > 0:
                for permission in missing_permissions:
                    embed.add_field(name="Missing Permission", value=permission)

            if len(missing_role_errors) > 0:
                for role in missing_roles:
                    embed.add_field(name="Missing Role", value=role)
            await interaction.send(embed=embed)

        elif isinstance(error, application_checks.ApplicationPrivateMessageOnly):
            embed = nextcord.Embed(
                title="DM Only Command", colour=nextcord.Colour.red()
            )
            embed.description = "This command can only be used in private messages."
            await interaction.send(embed=embed)

        elif isinstance(error, application_checks.ApplicationNoPrivateMessage):
            embed = nextcord.Embed(
                title="Not allowed in DMs", colour=nextcord.Colour.red()
            )
            embed.description = "This command can not be used in private messages."
            await interaction.send(embed=embed)

        elif isinstance(error, application_checks.ApplicationBotMissingPermissions):
            embed = nextcord.Embed(
                title="Bot Lacking Permissions", colour=nextcord.Colour.red()
            )
            embed.description = (
                "I do not have enough permission(s) to execute this command."
            )
            for permission in error.missing_permissions:
                embed.add_field(name="Missing Permission", value=permission)
            await interaction.send(embed=embed)

        elif isinstance(error, application_checks.ApplicationNotOwner):
            embed = nextcord.Embed(
                title="Owner Only Command", colour=nextcord.Colour.red()
            )
            embed.description = (
                "This command can only be used by the owners of the bot."
            )
            await interaction.send(embed=embed)

        else:
            await interaction.send(
                "An unexpected error has occurred, please report it to the developer."
            )
            raise (error)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        # Text Based Commands Error Handling
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(f"Missing required argument(s)")
        elif isinstance(error, commands.errors.MemberNotFound):
            await ctx.reply("I coudn't find that member.")
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply("You do not have enough permissions to run this command.")
        elif isinstance(error, commands.errors.CheckAnyFailure):
            await ctx.reply("You do not have enough permissions to run this command.")
        elif isinstance(error, commands.errors.MissingRole):
            await ctx.reply("You do not have the required role to run this command.")
        elif isinstance(error, commands.errors.PrivateMessageOnly):
            await ctx.reply("This command can only be used in private messages.")
        elif isinstance(error, commands.errors.NoPrivateMessage):
            await ctx.reply("This command can not be used in private messages.")
        elif isinstance(error, commands.errors.CommandNotFound):
            pass
        elif isinstance(error, commands.errors.TooManyArguments):
            await ctx.reply("Too many arguments.")
        else:
            await ctx.reply(
                "An unexpected error has occurred, please report it to the developer."
            )
            raise (error)


def setup(bot):
    bot.add_cog(Errors(bot))
