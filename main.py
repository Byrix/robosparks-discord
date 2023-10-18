# Import modules
import os
from dotenv import load_dotenv
import disnake
from disnake.ext import commands
import json
import logging
from datetime import datetime

# Load basic info
load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]
with open('ids.json') as f:
    ids = json.load(f)

# Init bot
intent = disnake.Intents(
    members=True,
    reactions=True,
    guilds=True,
)
bot = commands.InteractionBot(intents=intent)

# Setup logging
filename = f'robosparks_discord_{datetime.now().strftime("%y%m%d")}.log'
logger = logging.getLogger('disnake')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=f'./logs/{filename}', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(levelname)s:%(asctime)s:%(name)s: %(message)s'))
logger.addHandler(handler)



@bot.event
async def on_connect():
    logger.info('Bot connected')
    print("Connected")


@bot.event
async def on_ready():
    logger.info('Bot ready')
    msg = f"Bot connected\nLogged in as {bot.user.name}\nConnected to guilds: "
    for guild in bot.guilds:
        msg += f"{guild.name}, "
    print("The bot is ready!")


@bot.listen('on_error')
async def on_error(err):
    logChannel = await bot.fetch_channel(ids['channels']['log'])
    await logChannel.send(f"<@{ids['users']['byrix']}> | ERROR | {err}")
    logger.warning(err)


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


@bot.listen('on_raw_reaction_add')
async def on_raw_reaction_add(pl: disnake.RawReactionActionEvent):
    if pl.message_id == ids['messages']['rules']:
        guild = await bot.fetch_guild(ids['guilds']['biome'])
        if pl.emoji.id == ids['emotes']['bupitup']:
            role = guild.get_role(ids['roles']['forest'])
            await pl.member.add_roles(role, reason='accepted-rules')
            logger.info(f"Member {pl.member.name} has been assigned role {role.name} in guild {guild.name}")
        elif pl.emoji.id == ids['emotes']['cheer']:
            role = guild.get_role(ids['roles']['notif'])
            await pl.member.add_roles(role, reason='accepted-notify')
            logger.info(f"Member {pl.member.name} has been assigned role {role.name} in guild {guild.name}")



# TODO Make work
# @bot.listen('on_reaction_remove')
# async def on_reaction_remove(reaction: disnake.Reaction, member: disnake.Member):
#     print("triggered")
#     if reaction.message.id == 1163437489441214604:
#         guild = await bot.fetch_guild(876817614305898546)
#         if reaction.emoji.id == 879008055432478800:
#             # role = guild.get_role(877904365703290981)
#             # await pl.member.remove_roles(role, reason='unaccepted-rules')
#             print('Hylian')
#         elif reaction.emoji.id == 1144086169274040331:
#             print("Aro Heart")
#             # role = guild.get_role(877904365703290981)
#             # await pl.member.remove_roles(role, reason='unaccepted-notify')
# @bot.listen('on_raw_reaction_remove')
# async def on_raw_reaction_remove(pl: disnake.RawReactionClearEvent):
#     pass


# bot.load_extension("cogs.golive")
# bot.load_extension('cogs.ping')
# bot.load_extension('cogs.quote')
bot.load_extensions('cogs')

# Run bot
if __name__ == "__main__":
    bot.run(BOT_TOKEN)
