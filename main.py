# Import modules
import os
from dotenv import load_dotenv
import disnake
from disnake.ext import commands

# Load env vars
load_dotenv()
DEV_BOT_TOKEN = os.environ["DEV_BOT_TOKEN"]


# Init bot
bot = commands.Bot()


@bot.event
async def on_ready():
    print("The bot is ready!")


@bot.slash_command()
async def ping(inter):
    await inter.response.send_message("Pong!")


# Run bot
if __name__ == "__main__":
    bot.run(DEV_BOT_TOKEN)