import random
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands


def purge_check(m):    return not m.embeds[0].title in ['チャンネルリセット中...'] if bool(m.embeds) else True

#名前変更用のやつ
class rename(discord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="チャンネル名変更",
            timeout=60,
        )
        self.value = None

        self.name = discord.ui.TextInput(
            label="新しいチャンネル名(空白でリセット)",
            style=discord.TextStyle.short,
            placeholder="VC-xx",
            required=False,
        )
        self.add_item(self.name)

    async def on_submit(self, interaction) -> None:
        self.value = self.name.value
        self.stop()
        if self.value != '':
            await interaction.response.send_message(f'チャンネル名を`{self.value}`に設定しました', ephemeral=True)
        else:
            await interaction.response.send_message('チャンネル名をリセットしました', ephemeral=True)


class select(discord.ui.Select):
    def __init__(self, vc_info, channel, owmerid, mode):
        self.option = []
        self.channel = channel
        self.mode = mode
        self.vc_info = vc_info


        for user in channel.members: # 全ユーザー分の選択できる要素追加
            if user.bot is False:
                if user.id != owmerid:
                    self.option.append(discord.SelectOption(label=user.name, value=user.id))
        super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=self.option)
    async def callback(self, interaction: discord.Interaction):
            for member in self.channel.members:
                if str(member.id) == str(self.values[0]):
                    if self.mode =='kick':
                        try:
                            await member.move_to(None)
                            await interaction.response.send_message(content=f"{member.name}をVCからキックしました",ephemeral=True)
                        except:
                            await interaction.response.send_message(content=f"{member.name}をVCからキックできませんでした",ephemeral=True)
                        break
                    elif self.mode =='owner':
                        vcinfo = await self.vc_info.find_one({
                            'channel_id': interaction.channel.id
                        }, {
                            "_id": False  # 内部IDを取得しないように
                        })
                        newinfo = {
                            'channel': vcinfo['channel'],
                            'channel_id': interaction.channel.id,
                            'owner_id': member.id,
                            'tts': vcinfo['tts'],
                            'joincall':vcinfo['joincall'],
                            'radio': vcinfo['radio'],
                            'radioURL': vcinfo['radioURL'],
                            'mode': vcinfo['mode'],
                            'dashboard_id': vcinfo['dashboard_id']
                        }
                        await self.vc_info.replace_one({
                            'channel_id': interaction.channel.id
                        }, newinfo, upsert=True)
                        await interaction.channel.send(f'{member.mention}は{interaction.channel}の所有権を持っています', delete_after=60)
                        await interaction.response.send_message(content=f"{member.name}に所有権を移動しました",ephemeral=True)

class SelectView(discord.ui.View): # view追加用のクラス
    def __init__(self, vcinfo, channel, ownerid, mode, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(select(vcinfo, channel, ownerid, mode))







# ダッシュボード用のやつ
class dashboard(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        discord.ui.view.timeout = None # タイムアウトをなしに
        self.bot = bot.bot

    
    # 部屋関係
    @discord.ui.button(label='通常モード', style=discord.ButtonStyle.green, emoji='✅', row=1)
    async def Normal(self, interaction: discord.Interaction, button: discord.ui.Button):
        vcinfo = await self.bot.vc_info.find_one({
            'channel_id': interaction.channel.id
        }, {
            "_id": False  # 内部IDを取得しないように
        })
        if vcinfo['owner_id'] == interaction.user.id:
            if vcinfo['mode'] != 'Normal':
                await interaction.channel.edit(sync_permissions=True)
                newinfo = {
                    'channel': vcinfo['channel'],
                    'channel_id': interaction.channel.id,
                    'owner_id': vcinfo['owner_id'],
                    'tts': vcinfo['tts'],
                    'joincall':vcinfo['joincall'],
                    'radio': vcinfo['radio'],
                    'radioURL': vcinfo['radioURL'],
                    'mode': 'Normal',
                    'dashboard_id': vcinfo['dashboard_id']
                }
                await self.bot.vc_info.replace_one({
                    'channel_id': interaction.channel.id
                }, newinfo, upsert=True)
                await interaction.response.send_message('通常モードに設定しました', ephemeral=True)
            else:
                await interaction.response.send_message('すでに通常モードに設定されています', ephemeral=True)
        else:
            await interaction.response.send_message('VCチャンネルのオーナーではないため実行できません', ephemeral=True)


    @discord.ui.button(label='許可モード', style=discord.ButtonStyle.secondary, emoji='📩', row=1)
    async def permit(self, interaction: discord.Interaction, button: discord.ui.Button):
        vcinfo = await self.bot.vc_info.find_one({
            'channel_id': interaction.channel.id
        }, {
            "_id": False  # 内部IDを取得しないように
        })
        if vcinfo['owner_id'] == interaction.user.id:
            await interaction.response.send_message('やる気が出たら実装するかもしれません', ephemeral=True)
        else:
            await interaction.response.send_message('VCチャンネルのオーナーではないため実行できません', ephemeral=True)


    @discord.ui.button(label='ロック', style=discord.ButtonStyle.secondary, emoji='🔒', row=1)
    async def lock(self, interaction: discord.Interaction, button: discord.ui.Button):
        vcinfo = await self.bot.vc_info.find_one({
            'channel_id': interaction.channel.id
        }, {
            "_id": False  # 内部IDを取得しないように
        })
        if vcinfo['owner_id'] == interaction.user.id:
            if vcinfo['mode'] != 'Lock':
                await interaction.channel.edit(sync_permissions=True)
                member = interaction.channel.members
                for user in member:
                    await interaction.channel.set_permissions(user, connect=True)
                await interaction.channel.set_permissions(self.bot.everyone, connect=False)
                await interaction.channel.set_permissions(self.bot.botrole, connect=True)
                newinfo = {
                    'channel': vcinfo['channel'],
                    'channel_id': interaction.channel.id,
                    'owner_id': vcinfo['owner_id'],
                    'tts': vcinfo['tts'],
                    'joincall':vcinfo['joincall'],
                    'radio': vcinfo['radio'],
                    'radioURL': vcinfo['radioURL'],
                    'mode': 'Lock',
                    'dashboard_id': vcinfo['dashboard_id']
                }
                await self.bot.vc_info.replace_one({
                    'channel_id': interaction.channel.id
                }, newinfo, upsert=True)
                await interaction.response.send_message('ロックモードに設定しました', ephemeral=True)
            else:
                await interaction.response.send_message('すでにロックモードに設定されています', ephemeral=True)
        else:
            await interaction.response.send_message('VCチャンネルのオーナーではないため実行できません', ephemeral=True)


    # NSFW
    @discord.ui.button(label='NSFW', style=discord.ButtonStyle.secondary, emoji='🔞', row=2)
    async def nsfw(self, interaction: discord.Interaction, button: discord.ui.Button):
        vcinfo = await self.bot.vc_info.find_one({
            'channel_id': interaction.channel.id
        }, {
            "_id": False  # 内部IDを取得しないように
        })
        if vcinfo['owner_id'] == interaction.user.id:
            if interaction.channel.nsfw == False:
                await interaction.channel.edit(nsfw=True)
                await interaction.response.send_message('NSFWを設定しました', ephemeral=True)
            else:
                await interaction.channel.edit(nsfw=False)
                await interaction.response.send_message('NSFWを解除しました', ephemeral=True)
        else:
            await interaction.response.send_message('VCチャンネルのオーナーではないため実行できません', ephemeral=True)


    # 名前変更
    @discord.ui.button(label='名前変更', style=discord.ButtonStyle.secondary, emoji='📝', row=2)
    async def rename(self, interaction: discord.Interaction, button: discord.ui.Button):
        vcinfo = await self.bot.vc_info.find_one({
            'channel_id': interaction.channel.id
        }, {
            "_id": False  # 内部IDを取得しないように
        })
        if vcinfo['owner_id'] == interaction.user.id:
            modal = rename()
            await interaction.response.send_modal(modal)
            await modal.wait()
            if modal.value == '':
                match vcinfo['channel']:
                    case 1:
                        await interaction.channel.edit(name=self.bot.config['vc1_name'])
                    case 2:
                        await interaction.channel.edit(name=self.bot.config['vc2_name'])
                    case 3:
                        await interaction.channel.edit(name=self.bot.config['vc3_name'])
            else:
                await interaction.channel.edit(name=modal.value)
        else:
            await interaction.response.send_message('VCチャンネルのオーナーではないため実行できません', ephemeral=True)


    # ユーザー関係
    @discord.ui.button(label='キック', style=discord.ButtonStyle.secondary, emoji='🦵', row=3)
    async def kick(self, interaction: discord.Interaction, button: discord.ui.Button):
        vcinfo = await self.bot.vc_info.find_one({
            'channel_id': interaction.channel.id
        }, {
            "_id": False  # 内部IDを取得しないように
        })
        if vcinfo['owner_id'] == interaction.user.id:
            view = SelectView(self.bot.vc_info, interaction.channel, vcinfo['owner_id'], 'kick')
            await interaction.response.send_message('VCからキックするユーザーを選択してください', view=view, ephemeral=True)
        else:
            await interaction.response.send_message('VCのオーナーではないため実行できません', ephemeral=True)
    
    @discord.ui.button(label='招待作成', style=discord.ButtonStyle.secondary, emoji='🔗', row=3)
    async def invite(self, interaction: discord.Interaction, button: discord.ui.Button):
        vcinfo = await self.bot.vc_info.find_one({
            'channel_id': interaction.channel.id
        }, {
            "_id": False  # 内部IDを取得しないように
        })
        if vcinfo['owner_id'] == interaction.user.id:
            if vcinfo['mode'] != 'Normal':
                await interaction.response.send_message('VCがロックされているため招待を発行できません\nロックを解除してからもう一度行ってください', ephemeral=True)
            else:
                invite = await interaction.channel.create_invite(max_age=600)
                await interaction.response.send_message(f'招待リンクを発行しました\n招待リンクは約10分間有効です\n{invite}', ephemeral=True)
        
        else:
            await interaction.response.send_message('VCチャンネルのオーナーではないため実行できません', ephemeral=True)


# 作り方がよくわからんから放置
    @discord.ui.button(label='オーナー変更', style=discord.ButtonStyle.secondary, emoji='🔑', row=4)
    async def change(self, interaction: discord.Interaction, button: discord.ui.Button):
        vcinfo = await self.bot.vc_info.find_one({
            'channel_id': interaction.channel.id
        }, {
            "_id": False  # 内部IDを取得しないように
        })
        if vcinfo['owner_id'] == interaction.user.id:
            view = SelectView(self.bot.vc_info, interaction.channel, vcinfo['owner_id'], 'owner')
            await interaction.response.send_message('所有権を渡すユーザーを選択してください', view=view, ephemeral=True)
        else:
            await interaction.response.send_message('VCのオーナーではないため実行できません', ephemeral=True)

    @discord.ui.button(label='VCの情報', style=discord.ButtonStyle.secondary, emoji='ℹ', row=4)
    async def info(self, interaction: discord.Integration, button: discord.ui.Button):
        vcinfo = await self.bot.vc_info.find_one({
            'channel_id': interaction.channel.id
        }, {
            "_id": False  # 内部IDを取得しないように
        })
        embed = discord.Embed(title='VCの情報', description='', color=self.bot.guild.get_member(vcinfo['owner_id']).top_role.color)
        embed.add_field(name='名前', value=interaction.channel.name)
        embed.add_field(name='オーナー', value=self.bot.guild.get_member(vcinfo['owner_id']).mention)
        embed.add_field(name='状態', value=vcinfo['mode'])
        embed.add_field(name='参加人数', value=len(interaction.channel.members))
        embed.add_field(name='NSFWかどうか', value=interaction.channel.nsfw)
        await interaction.response.send_message('送信したで', ephemeral=True)
        await interaction.channel.send(embed=embed, delete_after=60)




class vctool(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    group = app_commands.Group(name="vctool", description="VC tool", guild_ids=[733707710784340100], guild_only=True)

    @group.command(description='ダッシュボードを再送信します')
    async def dashboard(self, interaction):
        if interaction.user.voice != None:
            if interaction.user.voice.channel == interaction.channel:
                vcinfo = await self.bot.vc_info.find_one({
                    'channel_id': interaction.channel.id
                }, {
                    "_id": False  # 内部IDを取得しないように
                })
                message = await interaction.channel.fetch_message(vcinfo['dashboard_id'])
                await message.delete()
                embed = discord.Embed(title="だっしゅぼーど", colour=discord.Colour(0x1122a6), description="いろいろできるよ(未完成)")
                embed.add_field(name='現在のVCオーナー :', value=self.bot.guild.get_member(vcinfo['owner_id']).mention)
                embed.set_footer(text='"/vctool dashboard"でダッシュボードを再送信できます')
                newdash = await interaction.channel.send(embed=embed, view=dashboard(self))
                await interaction.response.send_message('送信しました',  ephemeral=True)
                newinfo = {
                    'channel': vcinfo['channel'],
                    'channel_id': interaction.channel.id,
                    'owner_id': vcinfo['owner_id'],
                    'tts': vcinfo['tts'],
                    'joincall':vcinfo['joincall'],
                    'radio': vcinfo['radio'],
                    'radioURL': vcinfo['radioURL'],
                    'mode': vcinfo['mode'],
                    'dashboard_id': newdash.id
                }
                await self.bot.vc_info.replace_one({
                    'channel_id': interaction.channel.id
                }, newinfo, upsert=True)
            else:
                await interaction.response.send_message('チャンネルが違うで\n自分が参加してるVCのチャンネルで実行してな', ephemeral=True)
        else:
            await interaction.response.send_message('VCに参加してないとこのコマンドは使えないで', ephemeral=True)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        stage = self.bot.get_channel(884734698759266324)

        # 入退出処理
        if member.bot is False:
            # 入退出以外は弾く
            if before.channel != after.channel:
                # 退出
                if before.channel is not None and before.channel != stage and before.channel.afk is False:


                    # 通知
                    embed = discord.Embed(title="VC退出", colour=discord.Colour(0xd0021b), description="ユーザーが退出しました", timestamp=datetime.now())

                    embed.set_author(name=member.name, icon_url=member.display_avatar.url)
                    embed.set_footer(text="VC入退出通知")

                    await before.channel.send(embed=embed)

                    vcinfo = await self.bot.vc_info.find_one({
                        'channel_id': before.channel.id
                    }, {
                        "_id": False  # 内部IDを取得しないように
                    })

                    # ロック時等の処理
                    if vcinfo['mode'] is 'Lock' or vcinfo['mode'] is  'Permit':
                            await self.bot.vc1.set_permissions(member, connect=None)

                    vcmembers = before.channel.members
                    count = 0
                    for m in before.channel.members:
                        if m.bot == True:
                            vcmembers.pop(count)
                            count -= 1
                        count += 1

                    # チャンネル初期化
                    if len(vcmembers) == 0:
                        if len(before.channel.members) != 0:
                            for bot in before.channel.members:
                                await bot.move_to(None)
                        msg = await before.channel.send(embed=discord.Embed(title='チャンネルリセット中...', description='VCに誰もいなくなったためチャンネルをリセットしています', color=0x00ffff))
                        await before.channel.purge(limit=None, check=purge_check)
                        await msg.delete()
                        match vcinfo['channel']:
                            case 1:
                                await before.channel.edit(name=self.bot.config['vc1_name'])
                            case 2:
                                await before.channel.edit(name=self.bot.config['vc2_name'])
                            case 3:
                                await before.channel.edit(name=self.bot.config['vc3_name'])

                        await before.channel.edit(sync_permissions=True) # 権限をカテゴリに同期

                        newinfo = {
                            'channel': vcinfo['channel'],
                            'channel_id': before.channel.id,
                            'owner_id': None,
                            'tts': False,
                            'joincall':False,
                            'radio': False,
                            'radioURL': None,
                            'mode': 'Nomal',
                            'dashboard_id': None
                        }
                        await self.bot.vc_info.replace_one({
                            'channel_id': before.channel.id
                        }, newinfo, upsert=True)

                        if before.channel.nsfw == True:
                            await before.channel.edit(nsfw=False)


                    # オーナー変更
                    else:
                        if vcinfo['owner_id'] is member.id: # 抜けた人がオーナーだったら
                            newowner = random.choice(vcmembers)
                            await vcinfo['dashboard_id'].delete()
                            embed = discord.Embed(title="だっしゅぼーど", colour=discord.Colour(0x1122a6), description="いろいろできるよ(未完成)")
                            embed.add_field(name='現在のVCオーナー :',value=newowner.mention)
                            embed.set_footer(text='"k/vctool"でダッシュボードを再送信できます')
                            newdash = await self.bot.vc1.send(embed=embed, view=dashboard(self))
                            await after.channel.send(f'{newowner.mention}は{after.channel}の所有権を持っています', delete_after=60)

                            newinfo = {
                                'channel': vcinfo['channel'],
                                'channel_id': after.channel.id,
                                'owner_id': newowner.id,
                                'tts': vcinfo['tts'],
                                'joincall':vcinfo['joincall'],
                                'radio': vcinfo['radio'],
                                'radioURL': vcinfo['radioURL'],
                                'mode': vcinfo['mode'],
                                'dashboard_id': newdash.id
                            }
                            await self.bot.vc_info.replace_one({
                                'channel_id': after.channel.id
                            }, newinfo, upsert=True)

                # 入室
                if after.channel is not None and after.channel != stage and after.channel.afk is False:
                    # オーナー指定
                    vcinfo = await self.bot.vc_info.find_one({
                        'channel_id': after.channel.id
                    }, {
                        "_id": False  # 内部IDを取得しないように
                    })
                    if vcinfo['owner_id'] is None:
                        embed = discord.Embed(title="だっしゅぼーど", colour=discord.Colour(0x1122a6), description="いろいろできるよ(未完成)")
                        embed.add_field(name='現在のVCオーナー :',value=member.mention)
                        embed.set_footer(text='"k/vctool"でダッシュボードを再送信できます')
                        message = await after.channel.send(embed=embed, view=dashboard(self))
                        await after.channel.send(f'{member.mention}は{after.channel}の所有権を持っています', delete_after=60)
                        newinfo = {
                            'channel': vcinfo['channel'],
                            'channel_id': after.channel.id,
                            'owner_id': member.id,
                            'tts': vcinfo['tts'],
                            'joincall':vcinfo['joincall'],
                            'radio': vcinfo['radio'],
                            'radioURL': vcinfo['radioURL'],
                            'mode': 'Nomal',
                            'dashboard_id': message.id
                        }
                        await self.bot.vc_info.replace_one({
                            'channel_id': after.channel.id
                        }, newinfo, upsert=True)
                    embed = discord.Embed(title = "VC入室", colour = discord.Colour(0x7ed321), description = "ユーザーが入室しました", timestamp = datetime.now())

                    embed.set_author(name=member.name, icon_url=member.display_avatar.url)
                    embed.set_footer(text="VC入退出通知")

                    await after.channel.send(embed=embed)
                    


            

async def setup(bot):
    await bot.add_cog(vctool(bot))
