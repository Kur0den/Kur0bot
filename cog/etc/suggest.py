import discord
from discord.ext import commands


class discordissue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def request(ctx, mode):
        
        await ctx.send("")

async def setup(bot):
    await bot.add_cog(discordissue(bot))