import discord
from discord.ext import commands
from discord import app_commands
class set_(discord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="自己紹介文の変更",
            timeout=1024,
        )

        self.name = discord.ui.TextInput(
            label="新しい自己紹介文",
            style=discord.TextStyle.short,
            placeholder="人間です",
            max_length=20,
            required=True,
        )
        self.add_item(self.name)
        self.free = discord.ui.TextInput(
            label="自由入力欄",
            style=discord.TextStyle.long,
            placeholder="人間です",
            max_length=300,
            required=False,
        )
        self.add_item(self.free)

    async def on_submit(self, interaction) -> None:
        self.stop()
        await interaction.response.send_message('設定しました')

class profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    group = app_commands.Group(name="profile", description="プロファイル", guild_ids=[733707710784340100], guild_only=True)


    @group.command(name='set', description='プロファイルを登録します')
    async def p_set(self, interaction: discord.Interaction):
        modal = set_()
        await interaction.response.send_modal(modal)
        await modal.wait()
        new_data = {
            "userid": interaction.user.id,
            "name": modal.name.value,
            "free": modal.free.value
        }
        await self.bot.profiles_collection.replace_one({
            "userid": interaction.user.id  # useridで条件を指定
        }, new_data, upsert=True)


    @group.command(name='show', description='プロファイルを閲覧します')
    async def p_show(self, interaction, target: discord.User, show: bool =True):  # ユーザーを指定
        profile = await self.bot.profiles_collection.find_one({
            "userid": target.id
        }, {
            "_id": False  # 内部IDを取得しないように
        })
        if profile is None:
            return await interaction.response.send_message("見付かりませんでした。")
        embed = discord.Embed(title=f"`{target}`のプロフィール")  # 埋め込みを作成
        embed.add_field(name='名前', value=profile['name'])
        embed.add_field(name='一言', value=profile['free'])
        if show == True:
            show = False
        else:
            show = True
        return await interaction.response.send_message(embed=embed, ephemeral=show)  # 埋め込みを送信


    @group.command(name='delete', description='プロファイルを削除します')
    async def delete_profile(self, interaction, target: discord.User=None):  # ユーザーを指定
        if target == None:
            result = await self.bot.profiles_collection.delete_one({
                "userid": interaction.user.id  # useridで条件を指定
            })
        else:
            if interaction.permissions.administrator == True:
                result = await self.bot.profiles_collection.delete_one({
                    "userid": target.id  # useridで条件を指定
                })
            else:
                await interaction.response.send_message_message('他人のプロフィールの削除はできません。')
                return
        if result.deleted_count == 0:  # 削除できなかったら
            return await interaction.response.send_message("見付かりませんでした。")
        return await interaction.response.send_message("削除しました。")

async def setup(bot):
    await bot.add_cog(profile(bot))
