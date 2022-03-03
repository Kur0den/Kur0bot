import discord
from discord.ext import commands
import add_socket_response_event

bot = commands.Bot(command_prefix="c/")

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def test(self,ctx):
        await ctx.send("test!")

bot.add_cog(Greetings(bot))