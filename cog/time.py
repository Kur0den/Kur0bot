import discord
from discord.ext import commands
import datetime

class Time(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def time(self,ctx,sub = None):
        jst_date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y/%m/%d")
        jst_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%H:%M:%S")
        est_date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5))).strftime("%Y/%m/%d")
        est_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5))).strftime("%H:%M:%S")
        tst_date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime("%Y/%m/%d")
        tst_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime("%H:%M:%S")
        utc_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y/%m/%d")
        utc_time = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")
        if sub == 'date':
            embed = discord.Embed(title='📅Date', description=f'UTC `{utc_date}`\n\nTST `{tst_date}`JST `{jst_date}`\n\nEST `{est_date}`')
            await ctx.send(embed=embed)
        elif sub == 'time':
            embed = discord.Embed(title='⏲Time', description=f'UTC `{utc_time}`\n\nTST: `{tst_time}`\n\nJST `{jst_time}`\n\nEST `{est_time}`')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='📅Date&Time⏲', description=f'UTC `{utc_date} {utc_time}`\n\nTST: `{tst_date} {tst_time}`\n\nJST `{jst_date} {jst_time}`\n\nEST `{est_date} {est_time}`')
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Time(bot))
