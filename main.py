# Import modules
import os
from dotenv import load_dotenv
import disnake
from disnake.ext import commands
import json
import logging
from datetime import datetime

# Init bot
intent = disnake.Intents(
    members=True,
    reactions=True,
    guilds=True,
)
bot = commands.InteractionBot(intents=intent)

@bot.event
async def on_connect():
    logger.info('Bot connected')
    print("Connected")
    if DEBUG:
        print("RUNNING IN DEBUG")


@bot.event
async def on_ready():
    logger.info('Bot ready')
    print("The bot is ready!")


@bot.listen('on_error')
async def on_error(err):
    logChannel = await bot.fetch_channel(ids['channels']['log'])
    await logChannel.send(f"<@{ids['users']['byrix']}> | ERROR | {err}")
    logger.error(err)


@bot.listen('on_member_join')
async def on_member_join(member: disnake.Member):
    channel = await bot.fetch_channel(ids['channels']['welcome'])
    await channel.send(
        content=f"Hi hi hi <@{member.id}>, welcome to **{member.guild.name}**! So excited to have you here! <:kissy:{ids['emotes']['kissy']}> <:UwU:{ids['emotes']['uwu']}\nMake sure you head over to <#{ids['channels']['rules']}> so you can become a Forest Friend and access the server. We don't use `@everyone` tags here, so if you'd like to receive notifications make sure you grab the Notify Squad role after reading the <#{ids['channels']['rules']}>.",
    )
    logger.info(f"Member {member.name} has joined {member.guild.name}")


@bot.listen('on_raw_member_remove')
async def on_raw_member_remove(pl: disnake.RawGuildMemberRemoveEvent):
    channel = await bot.fetch_channel(ids['channels']['goodbye'])
    await channel.send(content=f"**{pl.user.name}** has left the server.")
    logger.info(f"Member {pl.user.name} has left guild {pl.user.guild.name}")

# bot.load_extension("cogs.golive")
# bot.load_extension('cogs.ping')
# bot.load_extension('cogs.reaction_roles')
# bot.load_extension('cogs.quote')
bot.load_extensions('cogs')

# Run bot
if __name__ == "__main__":
    # Load basic info
    load_dotenv()
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    DEBUG = os.environ["DEBUG"]=="TRUE"
    ID_FILE = 'ids-debug.json' if DEBUG else 'ids.json'
    with open(ID_FILE) as f:
        ids = json.load(f)

    # Setup logging
    filename = f'robosparks_discord_{datetime.now().strftime("%y%m%d")}.log'
    logger = logging.getLogger('disnake')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename=f'./logs/{filename}', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(levelname)s:%(asctime)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    # Run bot
    bot.run(BOT_TOKEN)
