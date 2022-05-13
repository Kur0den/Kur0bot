import discord
from discord.ext import commands

class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def test(self,ctx):
        await ctx.send("ぱあ")

async def setup(bot):
    await bot.add_cog(test(bot))