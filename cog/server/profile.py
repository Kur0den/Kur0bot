import discord
from discord.ext import commands
from discord import app_commands

class set_(discord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="プロフィールの変更",
            timeout=None,
        )

        self.read = discord.ui.TextInput(
            label="名前の読み方",
            style=discord.TextStyle.short,
            placeholder="たなか",
            max_length=20,
            required=True,
        )
        self.add_item(self.read)
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
        await interaction.response.send_message('設定しました', ephemeral=True)


class profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    group = app_commands.Group(name="profile", description="プロフィール", guild_ids=[733707710784340100], guild_only=True)


    @group.command(name='set', description='プロフィールを登録します')
    async def p_set(self, interaction: discord.Interaction):
        modal = set_()
        await interaction.response.send_modal(modal)
        await modal.wait()
        new_data = {
            "userid":   interaction.user.id,
            "read":     modal.read.value,
            "gender":   modal.gender.value,
            "place":    modal.place.value,
            "tastes":   modal.tastes.value,
            "free":     modal.free.value
        }
        await self.bot.profiles_collection.replace_one({
            "userid": interaction.user.id  # useridで条件を指定
        }, new_data, upsert=True)


    @group.command(name='show', description='プロフィールを閲覧します')
    async def p_show(self, interaction, target: discord.User, show: bool =False):  # ユーザーを指定
        profile = await self.bot.profiles_collection.find_one({
            "userid": target.id
        }, {
            "_id": False  # 内部IDを取得しないように
        })
        if profile is None:
            return await interaction.response.send_message("見付かりませんでした。")
        embed = discord.Embed(title=f"`{target}`のプロフィール")  # 埋め込みを作成
        embed.add_field(name='読み方', value=profile['read'])
        embed.add_field(name='性別', value=profile['gender'])
        embed.add_field(name='居住地', value=profile['place'])
        embed.add_field(name='趣味', value=profile['tastes'])
        embed.add_field(name='一言', value=profile['free'])
        if show == True:
            show = False
        else:
            show = True
        return await interaction.response.send_message(embed=embed, ephemeral=show)  # 埋め込みを送信


    @group.command(name='delete', description='プロフィールを削除します')
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

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.bot.profiles_collection.delete_one({
                "userid": member.id  # useridで条件を指定
            })

async def setup(bot):
    await bot.add_cog(profile(bot))
