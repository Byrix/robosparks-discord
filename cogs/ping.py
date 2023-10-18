import disnake
from disnake.ext import commands
import logging


class PingCommand(commands.Cog):
    """ This will be a ping command """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger('disnake.cogs.ping')
        self.logChannel = None

    @commands.slash_command()
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        self.logger.info(
            f"User {inter.user.name} used the {inter.application_command.name} command in guild {inter.guild.name}")
        await inter.response.send_message(f"Pong!")


def setup(bot: commands.Bot):
    bot.add_cog(PingCommand(bot))
