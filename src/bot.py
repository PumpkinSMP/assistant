from dotenv import dotenv_values
import os
import logging
import nextcord
from nextcord.ext import commands


prefix = commands.when_mentioned_or("!")
bot = commands.Bot(
    command_prefix=prefix,
    intents=nextcord.Intents.all(),
    owner_ids={914452175839723550, 691319007579471902},
)
bot.env = dotenv_values(".env")

# Logging setup
logger = logging.getLogger("nextcord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="log/nextcord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)
bot.logger = logger
bot.load_extension("jishaku")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")


for file in os.listdir("./src/cogs"):
    """
    Load all cogs in cogs directory.
    """
    if file.endswith(".py"):
        name = file[:-3]
        cog = f"cogs.{name}"
        bot.load_extension(cog)
        print(f"Loaded extension {name}.")

bot.run(bot.env["TOKEN"])
