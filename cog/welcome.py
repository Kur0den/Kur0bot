import discord
from discord.ext import commands


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        self.bot.owner.send('あああ')

async def setup(bot):
    await bot.add_cog(Welcome(bot))
