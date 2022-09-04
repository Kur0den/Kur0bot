import discord
from discord.ext import commands


class profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="set")
    async def set_profile(ctx, *, text):  # setだと変数名がかぶるので変更、*,で空白を無視
        await profiles_collection.insert_one({
            "userid": ctx.author.id,
        "text": text
        })
        await ctx.reply("設定が完了しました。")

async def setup(bot):
    await bot.add_cog(profile(bot))
