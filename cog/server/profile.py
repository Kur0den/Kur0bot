import discord
from discord.ext import commands


class profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pset")
    async def set_profile(self, ctx, text):  # setだと変数名がかぶるので変更、*,で空白を無視
        new_data = {
            "userid": ctx.author.id,
            "text": text
        }
        await self.bot.profiles_collection.replace_one({
            "userid": ctx.author.id  # useridで条件を指定
        }, new_data, upsert=True)
        await ctx.reply("設定が完了しました。")

    @commands.command(name="pshow")
    async def show_profile(self, ctx, target: discord.User):  # ユーザーを指定
        profile = await self.bot.profiles_collection.find_one({
            "userid": target.id
        }, {
            "_id": False  # 内部IDを取得しないように
        })
        if profile is None:
            return await ctx.reply("見付かりませんでした。")
        embed = discord.Embed(title=f"`{target}`のプロフィール", description=profile["text"])  # 埋め込みを作成
        return await ctx.reply(embed=embed)  # 埋め込みを送信


async def setup(bot):
    await bot.add_cog(profile(bot))
