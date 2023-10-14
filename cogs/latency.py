import disnake
from disnake.ext import commands

class LatencyCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name='latency',
        description='Returns websocket latency.',
    )
    async def latency(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message(f"Latency: {round(self.bot.latency)*1000}ms")


def setup(bot):
    bot.add_cog(LatencyCommand(bot))
