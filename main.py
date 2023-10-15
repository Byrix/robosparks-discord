# Import modules
import os
from dotenv import load_dotenv
import disnake
from disnake.ext import commands

# Load env vars
load_dotenv()
DEV_BOT_TOKEN = os.environ["DEV_BOT_TOKEN"]
TEST_ENV = bool(os.environ['TEST_ENV'])


# Init bot
bot = commands.Bot()


@bot.event
async def on_ready():
    print("The bot is ready!")

bot.load_extension("cogs.golive")
bot.load_extension('cogs.ping')
bot.load_extension('cogs.quote')

# Run bot
if __name__ == "__main__":
    bot.run(DEV_BOT_TOKEN)
