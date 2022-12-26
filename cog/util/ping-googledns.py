import asyncio

import discord
from discord.ext import commands
from ping3 import ping
from discord import app_commands

class pinggoogledns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def hoge(ctx:discord.Interaction):
        target = '8.8.8.8'#pingを取得するIPまたはドメインを入力
        result = int(ping(target, unit="ms")) 
        embed = discord.Embed(title="ServerStatus",description=str(result) + "ms", color=discord.Colour.from_rgb(128,255,0))
        await ctx.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(pinggoogledns(bot))
