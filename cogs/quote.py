import disnake
from disnake.ext import commands
import mariadb
import re
import logging
from dotenv import load_dotenv
import os


class Quote(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        load_dotenv()
        DB_PASSWORD = os.environ['DB_PASSWORD']
        conn = mariadb.connect(
            user='robosparkles',
            password=DB_PASSWORD,
            host='localhost',
            database='robosparkles_db'
        )
        self.db = conn.cursor()
        self.logger = logging.getLogger('disnake.cogs.quote')

    @commands.slash_command(
        name='quote',
        description='get a quote from stream',
    )
    async def quote(self, inter: disnake.ApplicationCommandInteraction, query=None):
        await inter.response.defer()
        self.logger.info(f"User {inter.user.name} used the {inter.application_command.name} command in guild {inter.guild.name}")
        if query is not None and query.isdigit():
            # Get ref
            self.db.execute(f'SELECT * FROM quotes ORDER BY id LIMIT 1 OFFSET {int(query)-1}')
        elif type(query) is str:
            # Search
            self.db.execute(f"SELECT * FROM quotes WHERE quote LIKE '%{query}%' ORDER BY RAND() LIMIT 1")
        else:
            # Get random
            self.db.execute('SELECT * FROM quotes ORDER BY RAND() LIMIT 1')

        quote = None
        for obj in self.db:
            quote = obj
            break

        if quote is None:
            await inter.edit_original_response(content='No quote found!')
            return

        quote_split = quote[1].split("\"")
        quoteEmbed = disnake.Embed(
            title=quote_split[1],
            timestamp=quote[4],
            colour=disnake.Colour.from_rgb(124, 4, 244)
        )
        quoteEmbed.add_field(name='Game', value=quote[3], inline=True)

        if quote_split[2] != "":
            quote_author = re.sub('[^A-z]', '', quote_split[2])
            quoteEmbed.add_field(name='Said By', value=quote_author, inline=True)

        await inter.edit_original_response(embed=quoteEmbed)

def setup(bot):
    bot.add_cog(Quote(bot))
