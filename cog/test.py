import discord
from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def test(self,ctx):
        await ctx.send("ぱあ")

def setup(bot):
    return bot.add_cog(Greetings(bot))