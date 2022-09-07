from discord.ext import tasks, commands
from discord import app_commands
from datetime import datetime


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
                    await self.bot.unei_ch.send(f'{self.bot.owner.mention}\nシーズンリセット')

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(season(bot))