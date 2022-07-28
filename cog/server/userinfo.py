import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone


class userinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ui'])
    async def userinfo(self, ctx, *, user: discord.User = None):
        if user == None:
            user = ctx.author
        member = discord.utils.get(self.bot.get_all_members(), id=user.id)
        e = discord.Embed(title=f'{user}の詳細', description='詳細だよ', color=discord.Color.orange())
        e.add_field(name='名前', value=user)
        e.add_field(name='Botかどうか', value=user.bot)
        e.add_field(name='ID', value=user.id)
        g_m = discord.utils.get(ctx.guild.members, id=user.id)
        e.set_thumbnail(url=user.avatar)
        dt_now_jst_aware = timezone(timedelta(hours=+9), 'JST')
        jointime = member.joined_at.astimezone(dt_now_jst_aware).strftime(
            "%Y年%m月%d日%H時%M分%S秒"
        )
        e.add_field(name="サーバー参加日", value=jointime, inline=False)
        createtime = user.created_at.astimezone(dt_now_jst_aware).strftime(
        "%Y年%m月%d日%H時%M分%S秒"
        )
        e.add_field(name="アカウント作成日", value=createtime, inline=False)
        await ctx.send(embed=e)


async def setup(bot):
    await bot.add_cog(userinfo(bot))
