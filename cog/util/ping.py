import asyncio

import discord
from discord.ext import commands


class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self,ctx):
        embed = discord.Embed(title=f'pinging..')
        message = await ctx.send(embed=embed)
        await asyncio.sleep(1)
        pong = ':ping_pong:'
        embed = discord.Embed(title=f'{pong}Pong!', description=f'{round(self.bot.latency * 1000)}ms')
        await message.edit(embed=embed)

async def setup(bot):
    await bot.add_cog(ping(bot))
