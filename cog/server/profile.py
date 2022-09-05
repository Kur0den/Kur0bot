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

    @commands.command(name="pdelete", aliases=["pdel"])
    async def delete_profile(self, ctx, target: discord.User=None):  # ユーザーを指定
        if target == None:
            result = await self.bot.profiles_collection.delete_one({
                "userid": ctx.author.id  # useridで条件を指定
            })
        else:
            if ctx.permissions.administrator == True:
                result = await self.bot.profiles_collection.delete_one({
                    "userid": target.id  # useridで条件を指定
                })
            else:
                await ctx.send('他人のプロフィールの削除はできません。')
                return
        if result.deleted_count == 0:  # 削除できなかったら
            return await ctx.reply("見付かりませんでした。")
        return await ctx.reply("削除しました。")

async def setup(bot):
    await bot.add_cog(profile(bot))
