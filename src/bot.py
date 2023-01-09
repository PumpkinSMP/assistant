from dotenv import dotenv_values
import exts.db
import logging
import nextcord
from nextcord.ext import commands
import sys

bot = commands.Bot(
    command_prefix="?",
    intents=nextcord.Intents.all(),
    owner_ids={914452175839723550, 691319007579471902},
)
bot.environ = dotenv_values(".env")
bot.db = exts.db
exts.db.create_table()

# Logging setup
logger = logging.getLogger("nextcord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="log/nextcord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)
bot.logger = logger


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")


exts = ["exts.errors", "exts.fun", "exts.suggestions", "exts.utils", "exts.logs"]

for ext in exts:
    bot.load_extension(ext)
    print(f"Loaded extension {ext}.")
    logger.info(f"Loaded extension {ext}.")

if "--ci" in sys.argv:
    sys.exit(0)
bot.run(bot.environ["TOKEN"])
