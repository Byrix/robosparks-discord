import disnake
from disnake.ext import commands
import mariadb


class Quote(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        conn = mariadb.connect(
            user='root',
            password='Ae^7GwXF#Z5Taeo',
            host='localhost',
            database='robosparkles_db'
        )
        self.db = conn.cursor()

    @commands.slash_command(
        name='quote',
        description='get a quote from stream',
    )
    async def quote(self, inter: disnake.ApplicationCommandInteraction, query=None):
        await inter.response.defer()
        if query is not None and query.isdigit():
            # Get ref
            print('Ref')
            self.db.execute(f'SELECT * FROM quotes ORDER BY id LIMIT 1 OFFSET {int(query)-1}')
        elif type(query) is str:
            # Search
            print('search')
            self.db.execute(f"SELECT * FROM quotes WHERE quote LIKE '%{query}%' ORDER BY RAND() LIMIT 1")
        else:
            # Get random
            print('random')
            print(type(query))
            print(query)
            self.db.execute('SELECT * FROM quotes ORDER BY RAND() LIMIT 1')

        for obj in self.db:
            quote = obj
            break

        quoteEmbed = disnake.Embed(
            title=quote[1],
            description=quote[3],
            timestamp=quote[4],
            colour=disnake.Colour.from_rgb(124, 4, 244)
        )
        await inter.edit_original_response(embed=quoteEmbed)

def setup(bot):
    bot.add_cog(Quote(bot))
