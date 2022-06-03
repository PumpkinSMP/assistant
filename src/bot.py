import nextcord
from nextcord.ext import commands
import logging
import os


bot = commads.bot(commands_prefix=when_mentioned_or("ps "))
bot.owner_ids = {914452175839723550, 691319007579471902}

# Logging setup
logger = logging.getLogger('nextcord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='log/nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
bot.logger = logger


@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user} ({bot.user.id}")

for file in os.listdir("./src/cogs"):
    """
    Load all cogs in cogs directory.
    """
    if file.endswith(".py"):
        name = file[:-3]
        cog = f"cogs.{name}"
        cogs.append(cog)
        bot.load_extension(cog)
        logging.info(f"Loaded extension {name}.")

bot.run(os.getenv("TOKEN"))