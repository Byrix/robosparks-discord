import disnake
from disnake.ext import commands 
import logging
from dotenv import load_dotenv
import json
import os

class ReactionRoles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger('disnake.cogs.reactionroles')

        load_dotenv()
        DEBUG = os.environ['DEBUG'] == "TRUE"
        ID_FILE = "ids-debug.json" if DEBUG else "ids.json"
        with open(ID_FILE) as f:
            self.ids = json.load(f)
        self.EMOJI_TO_ROLE = {
            'hylian': self.ids['roles']['forest'],
            'l2': self.ids['roles']['notif'] 
        } if DEBUG else {
            'BupItUp': self.ids['roles']['forest'],
            'cheer': self.ids['roles']['notif'] 
        }

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, pl: disnake.RawReactionActionEvent):
        if pl.guild_id is None or pl.member is None:
            return

        role = self.__verify_payload(pl)
        if role is None:
            return

        try:
            await pl.member.add_roles(role)
            self.logger.info(f"Member {pl.member.name} has been assigned role {role.name} in guild {pl.member.guild.name}")
        except disnake.HTTPException as E:
            self.logger.error(f"An error occured assigning member {pl.member.name} the role {role.name} : {E}")
            self.__error_ping(E)
            # TODO Let user know an error occured 

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, pl: disnake.RawReactionActionEvent):
        if pl.guild_id is None:
            return

        role = self.__verify_payload(pl)
        if role is None:
            print("!")
            return

        guild = self.bot.get_guild(pl.guild_id)
        member = guild.get_member(pl.user_id)
        if member is None:
            print("2")
            return

        try:
            await member.remove_roles(role)
            self.logger.info(f"Member {member.name} has been be unassigned the {role.name} role in guild {guild.name}")
        except disnake.HTTPException as E:
            self.logger.error(f"An error occured unassigning member {member.name} the role {role.name} : {E}")
            self.__error_ping(E)

    def __error_ping(self, err):
        guild = self.bot.get_guild(self.ids['guilds']['test'])
        channel = guild.get_channel(self.ids['channels']['log'])

        channel.send(f"<@{self.ids['users']['byrix']}>, an error occured in Reaction Roles:\n{err}")

    def __verify_payload(self, pl: disnake.RawReactionActionEvent):
        if pl.message_id != self.ids['messages']['rules']:
            return None
        
        guild = self.bot.get_guild(pl.guild_id)
        if guild is None:
            return None
        
        try:
            role_id = self.EMOJI_TO_ROLE[pl.emoji.name]
        except KeyError:
            return None

        role = guild.get_role(role_id)
        if role is None:
            self.logger.error(f"Member {pl.member.name} attempted to receive role {role} (ID: {role_id}) but the role could not be found")
            self.__error_ping(f"Role {role} not found")
            # TODO Let the user know that an error occured somehow 
            return None
        return role

def setup(bot):
    bot.add_cog(ReactionRoles(bot))
