from nextcord.ext import commands


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        Error handling for the most common errors.
        """

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
        elif isinstance(error, commands.errors.TooManyArguments):
            await ctx.reply("Too many arguments.")
        else:
            await ctx.reply(
                f"An error has occurred, if this is unexpected then please report it to the developer.\nError:\n{error}"
            )
            raise (error)


def setup(bot):
    bot.add_cog(Errors(bot))
