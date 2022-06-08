import discord
from discord import app_commands
from discord.ext import commands

from typing import Optional
import datetime


class joining(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot

    
    @app_commands.command()
    # @app_commands.describe(member='指定したメンバーの参加してからの時間を表示します')
    async def joined(self, interaction: discord.Interaction): #, member: Optional[discord.Member] = None
         
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        # if member == None:
        #ここインテントする
        member = ctx.author
        joined = member.joined_at
        delta = now - joined
        t = trans(delta)
        embed = discord.Embed(
            title=str(member),
            description=f'{t.day}日 {t.hour}時間 {t.min}分 {t.sec}秒 {t.milli}ミリ秒 {t.micro}マイクロ秒',
            color=member.color
        )
        embed.add_field(name="参加日時", value=discord.utils.format_dt(member.joined_at))
        await ctx.send(embed=embed)
        return

        joined = member.joined_at
        delta = now - joined
        t = trans(delta)
        embed = discord.Embed(
            title=str(member),
            description=f'{t.day}日 {t.hour}時間 {t.min}分 {t.sec}秒 {t.milli}ミリ秒 {t.micro}マイクロ秒',
            color=member.color
        )
        await ctx.send(embeds=[embed])
        return


class Delta_to:
    def __init__(self, day, hour, min, sec, milli, micro):
        self.day = day
        self.hour = hour
        self.min = min
        self.sec = sec
        self.milli = milli
        self.micro = micro
    def __str__(self):
        return f"Delta_to(day={self.day}, hour={self.hour}, min={self.min}, sec={self.sec}, milli={self.milli}, micro={self.micro})"

def trans(delta):
    day = delta.days

    hour = delta.seconds // 3600

    min = (delta.seconds - hour * 3600) // 60

    sec = delta.seconds - (hour * 3600) - (min * 60)

    milli = int(delta.microseconds / 1000)
    micro = int(delta.microseconds - milli * 1000)
    return Delta_to(day, hour, min, sec, milli, micro)


async def setup(bot):
    await bot.add_cog(joining(bot), guilds=[discord.Object(id=733707710784340100)])