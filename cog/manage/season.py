from discord.ext import tasks, commands
from discord import app_commands
from datetime import datetime
import discord
import chozatu
from typing import Literal


class season(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot):
        self.bot = bot
    
    @tasks.loop(hours=24)
    async def season_notice(self):
        reset_m=['03','06','09','12']
        if datetime.now().strftime('%d') == '01':
            for m in reset_m:
                if datetime.now().strftime('%m') == reset_m:
                    await self.bot.unei_ch.send(f'{self.bot.owner.mention}\nシーズンリセット\nメンバーへの通知等忘れずに')
    
    
    @app_commands.command(name='seasonset')
    @app_commands.describe(season='変更するシーズンを選択')
    @app_commands.guilds(chozatu.id)
    async def set(self, interaction: discord.Interaction, season: Literal['Spring', 'Summer', 'Autumn', 'Winter']):
        season_channel = self.bot.get_channel(793424836080566312)
        if season == 'Spring':
            await season_channel.edit(name='🌸春シーズン|3~5🍡', reason='シーズン変更')
        elif season == 'Summer':
            await season_channel.edit(name='🍉夏シーズン|6~8🌊', reason='シーズン変更')
        elif season == 'Autumn':
            await season_channel.edit(name='🍁秋シーズン|9~11🥔', reason='シーズン変更')
        elif season == 'Winter':
            await season_channel.edit(name='❄️冬シーズン|12~2⛄', reason='シーズン変更')
        await interaction.response.send_message('シーズン表記を変更しました',ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(season(bot))