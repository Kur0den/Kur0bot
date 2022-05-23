import discord
from discord.ext import commands


class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        QuoteBot = guild.get_member(949479338275913799)
        if message.author == QuoteBot:
            await message.channel.send('おでん')

async def setup(bot):
    await bot.add_cog(Quote(bot))
