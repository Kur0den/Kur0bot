import discord
from discord.ext import commands

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @bot.command()
    async def ping(ctx):
        pong = ':ping_pong:'
        embed = discord.Embed(title=f'{pong}Pong!', description=f'{round(bot.latency * 1000)}ms')
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ping(bot))