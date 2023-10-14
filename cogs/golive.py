import disnake
from disnake.ext import commands

class GoLiveCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.live_message = "Test"

    @commands.slash_command(
        name='go_live',
        description='Send a go live message'
    )
    async def go_live(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=True)
        await self.bot.fetch_channel(876817614305898549).send(self.live_message)
        await inter.edit_original_response(content="Done!", ephemeral=True)

def setup(bot):
    bot.add_cog(GoLiveCommand(bot))
