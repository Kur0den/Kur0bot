import discord
from discord.ext import commands
import asyncio

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self,ctx):
        pong = ':ping_pong:'
        embed = discord.Embed(title=f'{pong}Pong!', description=f'{round(self.bot.latency * 1000)}ms')
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ping(bot))