from discord.ext import commands
from discord import app_commands
import discord

class vcreset(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.describe()
    @app_commands.guild_only()
    @app_commands.guilds(733707710784340100)
    @app_commands.default_permissions(administrator=True)
    async def vcreset(self, interaction: discord.Interaction):
        vc1 = {
            'channelid': '981800095760670730',
            'ownerid': '',
            'tts': 'False',
            'joincall': 'False',
            'radio': 'False',
            'mode': 'Nomal'
        }
        await self.bot.vc_info.replace_one({
            "channelid": '981800095760670730'
        }, vc1, upsert=True)
        vc2 = {
            'channelid': '981800262165495828',
            'ownerid': '',
            'tts': 'False',
            'joincall': 'False',
            'radio': 'False',
            'mode': 'Nomal'
        }
        await self.bot.vc_info.replace_one({
            "channelid": '981800262165495828'
        }, vc2, upsert=True)
        vc3 = {
            'channelid': '981800316116803636',
            'ownerid': '',
            'tts': 'False',
            'joincall': 'False',
            'radio': 'False',
            'mode': 'Nomal'
        }
        await self.bot.vc_info.replace_one({
            "channelid": '981800316116803636'
        }, vc3, upsert=True)
        await interaction.response.send_message('成功')

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(vcreset(bot))