import discord
from discord.ext import commands
import requests


class userinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def userinfo(ctx, member : discord.Member):
        e = discord.Embed(title=f'{member}の詳細', description='詳細だよ', color=discord.Color.orange())
        e.add_field(name='名前', value=f'{member}')
        e.add_field(name='あなたはBot?', value=member.bot)
        # e.add_field(name='ID', value=member.id)
        e.add_field(name='作成時間', value=member.created_at)
        e.add_field(name='サーバーに参加した時間', value=member.joined_at)
        await ctx.send(embed=e)


async def setup(bot):
    await bot.add_cog(userinfo(bot))
