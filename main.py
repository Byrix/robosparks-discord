# Import modules
import os
from dotenv import load_dotenv
import disnake
from disnake.ext import commands

# Load env vars
load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]

# Init bot
intent = disnake.Intents(
    members=True
)
bot = commands.InteractionBot(intents=intent)


@bot.event
async def on_ready():
    print("The bot is ready!")


@bot.listen('on_member_join')
async def on_member_join(member: disnake.Member):
    channel = await bot.fetch_channel(876817614305898549)
    await channel.send(content=f"Hi hi hi {member.display_name}, welcome to **The Biome**! So excited to have you here! emote emote.\nMake sure you head over to RULES so you can become a Forest Friend and access the server. We don't use `@everyone` tags here, so if you'd like to receive notifications make sure you grab the Notify Squad role after reading the RULES.")

@bot.listen('on_raw_member_remove')
async def on_raw_member_remove(pl: disnake.RawGuildMemberRemoveEvent):
    channel = await bot.fetch_channel(876817614305898549)
    await channel.send(content=f"**{pl.user.name}** has left the server.")

bot.load_extension("cogs.golive")
bot.load_extension('cogs.ping')
bot.load_extension('cogs.quote')

# Run bot
if __name__ == "__main__":
    bot.run(BOT_TOKEN)
