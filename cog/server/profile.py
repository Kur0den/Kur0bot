import discord
from discord.ext import commands
from discord import app_commands

class set_2(discord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="自己紹介文の変更(2/2)",
            timeout=None,
        )

        self.work = discord.ui.TextInput(
            label="職業",
            style=discord.TextStyle.short,
            placeholder="自宅警備員",
            max_length=20,
            required=False,
        )
        self.add_item(self.work)
        self.tastes = discord.ui.TextInput(
            label="趣味",
            style=discord.TextStyle.short,
            placeholder="睡眠",
            max_length=20,
            required=False,
        )
        self.add_item(self.tastes)
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


class set_1(discord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="自己紹介文の変更(1/2)",
            timeout=None,
        )

        self.name = discord.ui.TextInput(
            label="名前",
            style=discord.TextStyle.short,
            placeholder="田中",
            max_length=20,
            required=True,
        )
        self.add_item(self.name)
        self.read = discord.ui.TextInput(
            label="読み方",
            style=discord.TextStyle.short,
            placeholder="たなか",
            max_length=20,
            required=True,
        )
        self.add_item(self.read)
        self.dob = discord.ui.TextInput(
            label="生年月日",
            style=discord.TextStyle.short,
            placeholder="yyyy/mm/dd",
            max_length=10,
            required=False,
        )
        self.add_item(self.dob)
        self.gender = discord.ui.TextInput(
            label="性別",
            style=discord.TextStyle.short,
            placeholder="男性/女性/その他",
            max_length=3,
            required=False,
        )
        self.add_item(self.gender)
        self.place = discord.ui.TextInput(
            label="居住地",
            style=discord.TextStyle.short,
            placeholder="日本",
            max_length=5,
            required=False,
        )
        self.add_item(self.place)

    async def on_submit(self, interaction) -> None:
        modal = set_2()
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

class profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    group = app_commands.Group(name="profile", description="プロファイル", guild_ids=[733707710784340100], guild_only=True)


    @group.command(name='set', description='プロファイルを登録します')
    async def p_set(self, interaction: discord.Interaction):
        modal = set_1()
        await interaction.response.send_modal(modal)


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
