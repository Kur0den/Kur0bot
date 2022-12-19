import discord
from discord.ext import commands
from discord import app_commands
import chozatu
class set_(discord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="自己紹介文の変更",
            timeout=60,
        )
        self.value = None

        self.name = discord.ui.TextInput(
            label="新しい自己紹介文",
            style=discord.TextStyle.long,
            placeholder="人間です",
            max_length=300,
            required=True,
        )
        self.add_item(self.name)

    async def on_submit(self, interaction) -> None:
        self.value = self.name.value
        self.stop()
        await interaction.response.send_message('設定しました')

class profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.describe()
    @app_commands.guilds(chozatu.id)
    async def set_profile(self, interaction: discord.Interaction):
        modal = set_()
        await interaction.response.send_modal(modal)
        await modal.wait()
        new_data = {
            "userid": interaction.user.id,
            "text": modal.value
        }
        await self.bot.profiles_collection.replace_one({
            "userid": interaction.user.id  # useridで条件を指定
        }, new_data, upsert=True)



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
