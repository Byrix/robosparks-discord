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
    members=True,
    reactions=True,
)
bot = commands.InteractionBot(intents=intent)


@bot.event
async def on_ready():
    print("The bot is ready!")


@bot.listen('on_member_join')
async def on_member_join(member: disnake.Member):
    channel = await bot.fetch_channel(876817614305898549)
    await channel.send(
        content=f"Hi hi hi {member.display_name}, welcome to **The Biome**! So excited to have you here! emote emote.\nMake sure you head over to RULES so you can become a Forest Friend and access the server. We don't use `@everyone` tags here, so if you'd like to receive notifications make sure you grab the Notify Squad role after reading the RULES.")


@bot.listen('on_raw_member_remove')
async def on_raw_member_remove(pl: disnake.RawGuildMemberRemoveEvent):
    channel = await bot.fetch_channel(876817614305898549)
    await channel.send(content=f"**{pl.user.name}** has left the server.")


@bot.listen('on_raw_reaction_add')
async def on_raw_reaction_add(pl: disnake.RawReactionActionEvent):
    if pl.message_id == 1163437489441214604:
        guild = await bot.fetch_guild(876817614305898546)
        if pl.emoji.id == 879008055432478800:
            role = guild.get_role(877904365703290981)
            await pl.member.add_roles(role, reason='accepted-rules')
        elif pl.emoji.id == 1144086169274040331:
            role = guild.get_role(877904365703290981)
            await pl.member.add_roles(role, reason='accepted-notify')


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


@bot.listen('on_raw_reaction_remove')
async def on_raw_reaction_remove(pl: disnake.RawReactionClearEvent):
    pass


bot.load_extension("cogs.golive")
bot.load_extension('cogs.ping')
bot.load_extension('cogs.quote')

# Run bot
if __name__ == "__main__":
    bot.run(BOT_TOKEN)
