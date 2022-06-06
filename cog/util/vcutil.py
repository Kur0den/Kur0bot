import discord
from discord.ext import commands


class vcutil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(member, before, after):
        print()

async def setup(bot):
    await bot.add_cog(vcutil(bot))
