import os
import disnake
from datetime import datetime
import requests
from disnake.ext import commands
from dotenv import load_dotenv
import pytz

class GoLiveCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        load_dotenv()
        self.TWITCH_TOKEN = os.environ['TWITCH_TOKEN']

    def __getinfo(self, channelName: str):
        info = requests.get(
            url=f'https://api.twitch.tv/helix/streams?user_login={channelName}',
            headers={'Authorization': f'Bearer {self.TWITCH_TOKEN}',
                     'Client-Id': '5zq2mn2cdtffjoa6ir0ie37i0wiacr'}
        )
        info = info.json()['data'][0]
        image = info['thumbnail_url'].replace('{height}', str(int(1080/5))).replace('{width}', str(int(1920/5)))

        streamerInfo = requests.get(
            url=f"https://api.twitch.tv/helix/users?login={channelName}",
            headers={'Authorization': f'Bearer {self.TWITCH_TOKEN}',
                     'Client-Id': '5zq2mn2cdtffjoa6ir0ie37i0wiacr'},
        )

        ico = streamerInfo.json()['data'][0]['profile_image_url']
        timeUTC = pytz.timezone('UTC').localize(datetime.strptime(info['started_at'], '%Y-%m-%dT%H:%M:%SZ'))

        self.streamEmbed = disnake.Embed(
            title=info['title'],
            description=info['game_name'],
            url=f'https://www.twitch.tv/{channelName}',
            colour=disnake.Colour.from_rgb(124, 4, 244),
            timestamp=timeUTC,
        )
        self.streamEmbed.set_author(name=info['user_name'], icon_url=ico)
        self.streamEmbed.set_image(url=image)
        self.streamButton = disnake.ui.Button(
            label='Watch Now!',
            style=disnake.ButtonStyle.link,
            url=f'https://www.twitch.tv/{channelName}',
        )

    @commands.slash_command(
        name="golive",
        description="Send a go live message.",
    )
    async def golive(self, inter: disnake.ApplicationCommandInteraction, channel: str = 'biosparkles'):
        # await inter.response.send_message("test")
        await inter.response.defer(ephemeral=True)
        try:
            temp = self.__getinfo(channel)
            msg_channel = await self.bot.fetch_channel(876817614305898549)
            await msg_channel.send(
                content=f"<@&877904365703290981>, {channel} just went live! <:hylian:879008055432478800> <:hylian:879008055432478800>",
                embed=self.streamEmbed,
                components=self.streamButton,
            )
            resp = 'Done.'
        except IndexError:
            resp = f'{channel} is not live!'
        await inter.edit_original_response(content=resp)

def setup(bot):
    bot.add_cog(GoLiveCommand(bot))
