import discord
from discord.ext import commands

class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self,ctx):
        testconfig = self.bot.config['test']
        await ctx.send(f"ぱあ\nTestConfig: {testconfig}")

async def setup(bot):
    await bot.add_cog(test(bot))