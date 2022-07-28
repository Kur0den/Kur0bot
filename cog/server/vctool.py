import discord
from discord.ext import commands
from datetime import datetime
import random


def purge_check(m):    return not m.embeds[0].title in ['チャンネルリセット中...'] if bool(m.embeds) else True


class owner():
    def __init__(self, bot):
        super().__init__()
        self.vcowner = None
    
    # オーナー設定
    async def setup(self, member, after):
        if len(after.channel.members) == 1:
            if after.channel == self.bot.vc1:
                self.bot.vc1_owner = member
                embed = discord.Embed(title="だっしゅぼーど", colour=discord.Colour(0x1122a6), description="いろいろできるよ(未完成)")
                embed.set_footer(text='"k/vctool"でダッシュボードを再送信できます')
                self.bot.vc1_dash = await self.bot.vc1.send(embed=embed, view=dashboard(self))
                await self.bot.vc1.send(f'{member.mention}は{after.channel}の所有権を持っています', delete_after=60)
            elif after.channel == self.bot.vc2:
                self.bot.vc2_owner = member
                embed = discord.Embed(title="だっしゅぼーど", colour=discord.Colour(0x1122a6), description="いろいろできるよ(未完成)")
                embed.set_footer(text='"k/vctool"でダッシュボードを再送信できます')
                self.bot.vc2_dash = await self.bot.vc2.send(embed=embed, view=dashboard(self))
                await self.bot.vc2.send(f'{member.mention}は{after.channel}の所有権を持っています', delete_after=60)
            elif after.channel == self.bot.vc3:
                self.bot.vc3_owner = member
                embed = discord.Embed(title="だっしゅぼーど", colour=discord.Colour(0x1122a6), description="いろいろできるよ(未完成)")
                embed.set_footer(text='"k/vctool"でダッシュボードを再送信できます')
                self.bot.vc3_dash = await self.bot.vc3.send(embed=embed, view=dashboard(self))
                await self.bot.vc3.send(f'{member.mention}は{after.channel}の所有権を持っています', delete_after=60)
    
    # オーナーチェック
    async def check(self, member, channel):
        if channel == self.bot.vc1 and member == self.bot.vc1_owner:
            result = 'vc1'
        elif channel == self.bot.vc2 and member == self.bot.vc2_owner:
            result = 'vc2'
        elif channel == self.bot.vc3 and member == self.bot.vc3_owner:
            result = 'vc3'
        else:
            result = None
        return result
    
    
    # オーナー変更
    async def change(self, channel):
        member = channel.members
        count = 0
        for user in member:
            if user.bot == True:
                member.pop(count)
            count + 1
        
        if channel == self.bot.vc1:
            await self.bot.vc1_dash.delete()
            embed = discord.Embed(title="だっしゅぼーど", colour=discord.Colour(0x1122a6), description="いろいろできるよ(未完成)")
            embed.set_footer(text='"k/vctool"でダッシュボードを再送信できます')
            self.bot.vc1_dash = await self.bot.vc1.send(embed=embed, view=dashboard(self))
            self.bot.vc1_owner = random.choice(member)
            await channel.send(f'{self.bot.vc1_owner.mention}は{channel}の所有権を持っています', delete_after=60)
        elif channel == self.bot.vc2:
            await self.bot.vc2_dash.delete()
            embed = discord.Embed(title="だっしゅぼーど", colour=discord.Colour(0x1122a6), description="いろいろできるよ(未完成)")
            embed.set_footer(text='"k/vctool"でダッシュボードを再送信できます')
            self.bot.vc2_dash = await self.bot.vc2.send(embed=embed, view=dashboard(self))
            self.bot.vc2_owner = random.choice(member)
            await channel.send(f'{self.bot.vc2_owner.mention}は{channel}の所有権を持っています', delete_after=60)
        elif channel == self.bot.vc3:
            await self.bot.vc3_dash.delete()
            embed = discord.Embed(title="だっしゅぼーど", colour=discord.Colour(0x1122a6), description="いろいろできるよ(未完成)")
            embed.set_footer(text='"k/vctool"でダッシュボードを再送信できます')
            self.bot.vc3_dash = await self.bot.vc3.send(embed=embed, view=dashboard(self))
            self.bot.vc3_owner = random.choice(member)
            await channel.send(f'{self.bot.vc3_owner.mention}は{channel}の所有権を持っています', delete_after=60)

class status():
    def __init__(self, bot):
        super().__init__()
    
    async def set(self, chanel, status):
        if chanel == self.bot.vc1:
            self.bot.vc1_status = status
        elif chanel == self.bot.vc2:
            self.bot.vc2_status = status
        elif chanel == self.bot.vc3:
            self.bot.vc3_status = status
    
    async def check(self, channel):
        if channel == self.bot.vc1:
            result = self.bot.vc1_status
        elif channel == self.bot.vc2:
            result  = self.bot.vc2_status
        elif channel == self.bot.vc3:
            result = self.bot.vc3_status
        return result


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
    def __init__(self, channel, mode):
        self.option = []
        self.channel = channel
        self.mode = mode
        for user in channel.members:
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
                        if self.channel.id == 981800095760670730:
                            await self.channel.send(f'{member.mention}は{self.channel}の所有権を持っています', delete_after=60)
                            await interaction.response.send_message(content=f"{member.name}に所有権を移動しました",ephemeral=True)
                            return member
                            view.stop()
                        if self.channel.id == 981800262165495828:
                            await self.channel.send(f'{member.mention}は{self.channel}の所有権を持っています', delete_after=60)
                            await interaction.response.send_message(content=f"{member.name}に所有権を移動しました",ephemeral=True)
                            return member
                            view.stop()
                        if self.channel.id == 981800316116803636:
                            await self.channel.send(f'{member.mention}は{self.channel}の所有権を持っています', delete_after=60)
                            await interaction.response.send_message(content=f"{member.name}に所有権を移動しました",ephemeral=True)
                            return member
                            view.stop()

class SelectView(discord.ui.View):
    def __init__(self, channel, mode, *, timeout = 180):
        super().__init__(timeout=timeout)
        member = self.add_item(select(channel, mode))
        
        






# ダッシュボード用のやつ
class dashboard(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        discord.ui.view.timeout = None # タイムアウトをなしに
        self.bot = bot.bot

    
    # 部屋関係
    @discord.ui.button(label='通常モード', style=discord.ButtonStyle.green, emoji='✅', row=1)
    async def Normal(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = await owner.check(self, interaction.user, interaction.channel)
        # VC1
        if result == 'vc1':
            if await status.check(self, self.bot.vc1) != 'Normal':
                await self.bot.vc1.edit(sync_permissions=True)
                await status.set(self, self.bot.vc1, 'Normal')
                await interaction.response.send_message('通常モードに設定しました', ephemeral=True)
            else:
                await interaction.response.send_message('すでに通常モードに設定されています', ephemeral=True)
        # VC2
        elif result == 'vc2':
            if await status.check(self, self.bot.vc2) != 'Normal':
                await self.bot.vc2.edit(sync_permissions=True)
                await status.set(self, self.bot.vc2, 'Normal')
                await interaction.response.send_message('通常モードに設定しました', ephemeral=True)
            else:
                await interaction.response.send_message('すでに通常モードに設定されています', ephemeral=True)
        # VC3
        elif result == 'vc3':
            if await status.check(self, self.bot.vc3) != 'Normal':
                await self.bot.vc3.edit(sync_permissions=True)
                await status.set(self, self.bot.vc3, 'Normal')
                await interaction.response.send_message('通常モードに設定しました', ephemeral=True)
            else:
                await interaction.response.send_message('すでに通常モードに設定されています', ephemeral=True)
        else:
            await interaction.response.send_message('VCチャンネルのオーナーではないため実行できません', ephemeral=True)


    @discord.ui.button(label='許可モード', style=discord.ButtonStyle.secondary, emoji='📩', row=1)
    async def permit(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = await owner.check(self, interaction.user, interaction.channel)
        if result == 'vc1':
                await interaction.response.send_message('やる気が出たら実装します', ephemeral=True)
        elif result == 'vc2':
                await interaction.response.send_message('やる気が出たら実装します', ephemeral=True)
        elif result == 'vc3':
                await interaction.response.send_message('やる気が出たら実装します', ephemeral=True)
        else:
            await interaction.response.send_message('VCチャンネルのオーナーではないため実行できません', ephemeral=True)


    @discord.ui.button(label='ロック', style=discord.ButtonStyle.secondary, emoji='🔒', row=1)
    async def lock(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = await owner.check(self, interaction.user, interaction.channel)
        # VC1
        if result == 'vc1':
            if await status.check(self, self.bot.vc1) != 'Lock':
                await self.bot.vc1.edit(sync_permissions=True)
                member = self.bot.vc1.members
                for user in member:
                    await self.bot.vc1.set_permissions(user, connect=True)
                await self.bot.vc1.set_permissions(self.bot.everyone, connect=False)
                await self.bot.vc1.set_permissions(self.bot.botrole, connect=True)
                await status.set(self, self.bot.vc1, 'Lock')
                await interaction.response.send_message('ロックモードに設定しました', ephemeral=True)
            else:
                await interaction.response.send_message('すでにロックモードに設定されています', ephemeral=True)
        # VC2
        elif result == 'vc2':
            if await status.check(self, self.bot.vc2) != 'Lock':
                await self.bot.vc2.edit(sync_permissions=True)
                member = self.bot.vc2.members
                for user in member:
                    await self.bot.vc2.set_permissions(user, connect=True)
                await self.bot.vc2.set_permissions(self.bot.everyone, connect=False)
                await self.bot.vc2.set_permissions(self.bot.botrole, connect=True)
                await status.set(self, self.bot.vc2, 'Lock')
                await interaction.response.send_message('ロックモードに設定しました', ephemeral=True)
            else:
                await interaction.response.send_message('すでにロックモードに設定されています', ephemeral=True)
        # VC3
        elif result == 'vc3':
            if await status.check(self, self.bot.vc3) != 'Lock':
                await self.bot.vc3.edit(sync_permissions=True)
                member = self.bot.vc3.members
                for user in member:
                    await self.bot.vc3.set_permissions(user, connect=True)
                await self.bot.vc3.set_permissions(self.bot.everyone, connect=False)
                await self.bot.vc3.set_permissions(self.bot.botrole, connect=True)
                await status.set(self, self.bot.vc3, 'Lock')
                await interaction.response.send_message('ロックモードに設定しました', ephemeral=True)
            else:
                await interaction.response.send_message('すでにロックモードに設定されています', ephemeral=True)
        else:
            await interaction.response.send_message('VCチャンネルのオーナーではないため実行できません', ephemeral=True)


    # NSFW
    @discord.ui.button(label='NSFW', style=discord.ButtonStyle.secondary, emoji='🔞', row=2)
    async def nsfw(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = await owner.check(self, interaction.user, interaction.channel)
        if result == 'vc1':
            if self.bot.vc1.nsfw == True:
                await self.bot.vc1.edit(nsfw=False)
                await interaction.response.send_message('NSFWを解除しました', ephemeral=True)
            else:
                await self.bot.vc1.edit(nsfw=True)
                await interaction.response.send_message('NSFWを設定しました', ephemeral=True)
        elif result == 'vc2':
            if self.bot.vc2.nsfw == True:
                await self.bot.vc2.edit(nsfw=False)
                await interaction.response.send_message('NSFWを解除しました', ephemeral=True)
            else:
                await self.bot.vc2.edit(nsfw=True)
                await interaction.response.send_message('NSFWを設定しました', ephemeral=True)
        elif result == 'vc3':
            if self.bot.vc3.nsfw == True:
                await self.bot.vc3.edit(nsfw=False)
                await interaction.response.send_message('NSFWを解除しました', ephemeral=True)
            else:
                await self.bot.vc3.edit(nsfw=True)
                await interaction.response.send_message('NSFWを設定しました', ephemeral=True)
        else:
            await interaction.response.send_message('VCチャンネルのオーナーではないため実行できません', ephemeral=True)


    # 名前変更
    @discord.ui.button(label='名前変更', style=discord.ButtonStyle.secondary, emoji='📝', row=2)
    async def rename(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = await owner.check(self, interaction.user, interaction.channel)
        # VC1
        if result == 'vc1':
            modal = rename()
            await interaction.response.send_modal(modal)
            await modal.wait()
            if modal.value == '':
                await self.bot.vc1.edit(name='VC-1(128Kbps)')
            else:
                await self.bot.vc1.edit(name=modal.value)
        
        # VC2
        elif result == 'vc2':
            modal = rename()
            await interaction.response.send_modal(modal)
            await modal.wait()
            if modal.value == '':
                await self.bot.vc2.edit(name='VC-2(128Kbps)')
            else:
                await self.bot.vc2.edit(name=modal.value)
        
        # VC3
        elif result == 'vc3':
            modal = rename()
            await interaction.response.send_modal(modal)
            await modal.wait()
            if modal.value == '':
                await self.bot.vc3.edit(name='VC-3(64Kbps)')
            else:
                await self.bot.vc3.edit(name=modal.value)
        else:
            await interaction.response.send_message('VCチャンネルのオーナーではないため実行できません', ephemeral=True)


    # ユーザー関係
    @discord.ui.button(label='キック', style=discord.ButtonStyle.secondary, emoji='🦵', row=3)
    async def kick(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = await owner.check(self, interaction.user, interaction.channel)
        if result == 'vc1':
            view = SelectView(self.bot.vc1,'kick')
            await interaction.response.send_message('キックするユーザーを選択してください', view=view, ephemeral=True)
        elif result == 'vc2':
            view = SelectView(self.bot.vc2,'kick')
            await interaction.response.send_message('キックするユーザーを選択してください', view=view, ephemeral=True)
        elif result == 'vc3':
            view = SelectView(self.bot.vc3,'kick')
            await interaction.response.send_message('キックするユーザーを選択してください', view=view, ephemeral=True)
        else:
            await interaction.response.send_message('VCのオーナーではないため実行できません', ephemeral=True)
    
    @discord.ui.button(label='招待作成', style=discord.ButtonStyle.secondary, emoji='🔗', row=3)
    async def invite(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = await owner.check(self, interaction.user, interaction.channel)
        if result == 'vc1':
            if await status.check(self, self.bot.vc1) == 'Lock':
                await interaction.response.send_message('VCがロックされているため招待を発行できません\nロックを解除してからもう一度行ってください', ephemeral=True)
            elif await status.check(self, self.bot.vc1) == 'Normal':
                invite = await self.bot.vc1.create_invite(max_age=600)
                await interaction.response.send_message(f'招待リンクを発行しました\n招待リンクは約10分間有効です\n{invite}', ephemeral=True)
        if result == 'vc2':
            if await status.check(self, self.bot.vc2) == 'Lock':
                await interaction.response.send_message('VCがロックされているため招待を発行できません\nロックを解除してからもう一度行ってください', ephemeral=True)
            elif await status.check(self, self.bot.vc2) == 'Normal':
                invite = await self.bot.vc2.create_invite(max_age=600)
                await interaction.response.send_message(f'招待リンクを発行しました\n招待リンクは約10分間有効です\n{invite}', ephemeral=True)
        if result == 'vc3':
            if await status.check(self, self.bot.vc3) == 'Lock':
                await interaction.response.send_message('VCがロックされているため招待を発行できません\nロックを解除してからもう一度行ってください', ephemeral=True)
            elif await status.check(self, self.bot.vc3) == 'Normal':
                invite = await self.bot.vc3.create_invite(max_age=600)
                await interaction.response.send_message(f'招待リンクを発行しました\n招待リンクは約10分間有効です\n{invite}', ephemeral=True)
        
        else:
            await interaction.response.send_message('VCチャンネルのオーナーではないため実行できません', ephemeral=True)


# 作り方がよくわからんから放置
    '''@discord.ui.button(label='オーナー変更', style=discord.ButtonStyle.secondary, emoji='🔑', row=4)
    async def change(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = await owner.check(self, interaction.user, interaction.channel)
        if result == 'vc1':
            view = SelectView(self.bot.vc1,'owner')
            member = await interaction.response.send_message('所有権を渡すユーザーを選択してください', view=view, ephemeral=True)
            await view.wait()
            await self.bot.vc1_dash.delete()
            self.bot.vc1_dash = await self.bot.vc1.send('test', view=dashboard(self))
            self.bot.vc1_owner = member
            await owner.change(self, member)
        elif result == 'vc2':
            view = SelectView(self.bot.vc2,'owner')
            member = await interaction.response.send_message('所有権を渡すユーザーを選択してください', view=view, ephemeral=True)
            await view.wait()
            await self.bot.vc2_dash.delete()
            self.bot.vc2_dash = await self.bot.vc2.send('test', view=dashboard(self))
            self.bot.vc2_owner = member
            await owner.change(self, member)
        elif result == 'vc3':
            view = SelectView(self.bot.vc3,'owner')
            member = await interaction.response.send_message('所有権を渡すユーザーを選択してください', view=view, ephemeral=True)
            await view.wait()
            await self.bot.vc3_dash.delete()
            self.bot.vc3_dash = await self.bot.vc3.send('test', view=dashboard(self))
            self.bot.vc3_owner = member
            await owner.change(self, member)
        else:
            await interaction.response.send_message('VCのオーナーではないため実行できません', ephemeral=True)'''

    @discord.ui.button(label='VCの情報', style=discord.ButtonStyle.secondary, emoji='ℹ', row=4)
    async def info(self, interaction: discord.Integration, button: discord.ui.Button):
        if interaction.channel == self.bot.vc1:
            embed = discord.Embed(title='VC1の情報', description='')
            embed.add_field(name='名前', value=self.bot.vc1.name)
            embed.add_field(name='オーナー', value=self.bot.vc1_owner)
            embed.add_field(name='状態', value=self.bot.vc1_status)
            embed.add_field(name='何人いるか(Bot再起動などで正常に取得できてない場合があります。)', value=len(self.bot.vc2_members))
            embed.add_field(name='NSFWかどうか', value=self.bot.vc1.nsfw)
            await interaction.response.send_message(embed=embed, delete_after=60)
        elif interaction.channel == self.bot.vc2:
            embed = discord.Embed(title='VC2の情報', description='')
            embed.add_field(name='名前', value=self.bot.vc2.name)
            embed.add_field(name='オーナー', value=self.bot.vc2_owner)
            embed.add_field(name='状態', value=self.bot.vc2_status)
            embed.add_field(name='何人いるか(Bot再起動などで正常に取得できてない場合があります。)', value=len(self.bot.vc2_members))
            embed.add_field(name='NSFWかどうか', value=self.bot.vc2_nsfw)
            await interaction.response.send_message(embed=embed, delete_after=60)
        elif interaction.channel == self.bot.vc3:
            embed = discord.Embed(title='VC3の情報', description='')
            embed.add_field(name='名前', value=self.bot.vc2.name)
            embed.add_field(name='オーナー', value=self.bot.vc2_owner)
            embed.add_field(name='状態', value=self.bot.vc2_status)
            embed.add_field(name='何人いるか(Bot再起動などで正常に取得できてない場合があります。)', value=len(self.bot.vc2_members))
            embed.add_field(name='NSFWかどうか', value=self.bot.vc2_nsfw)
            await interaction.response.send_message(embed=embed, delete_after=60)



class vctool(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

#todo VCに誰もいないときはコマンドを使えないようにする
    @commands.command()
    async def vctool(self, ctx):
        if ctx.author.voice != None:
            if ctx.channel is self.bot.vc1 and ctx.author.voice.channel is self.bot.vc1:
                await self.bot.vc1_dash.delete()
                embed = discord.Embed(title="だっしゅぼーど", colour=discord.Colour(0x1122a6), description="いろいろできるよ(未完成)")
                embed.set_footer(text='"k/vctool"でダッシュボードを再送信できます')
                self.bot.vc1_dash = await ctx.send(embed=embed, view=dashboard(self))
            elif ctx.channel is self.bot.vc2 and ctx.author.voice.channel is self.bot.vc2:
                await self.bot.vc2_dash.delete()
                embed = discord.Embed(title="だっしゅぼーど", colour=discord.Colour(0x1122a6), description="いろいろできるよ(未完成)")
                embed.set_footer(text='"k/vctool"でダッシュボードを再送信できます')
                self.bot.vc2_dash = await ctx.send(embed=embed, view=dashboard(self))
            elif ctx.channel is self.bot.vc3 and ctx.author.voice.channel is self.bot.vc3:
                await self.bot.vc3_dash.delete()
                embed = discord.Embed(title="だっしゅぼーど", colour=discord.Colour(0x1122a6), description="いろいろできるよ(未完成)")
                embed.set_footer(text='"k/vctool"でダッシュボードを再送信できます')
                self.bot.vc3_dash = await ctx.send(embed=embed, view=dashboard(self))
            else:
                await ctx.send('チャンネルが違うで\n自分が参加してるVCのチャンネルで実行してな', delete_after=60)
        else:
            await ctx.send('VCに参加してないとこのコマンドは使えないで', delete_after=60)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        
        stage = self.bot.get_channel(884734698759266324)
        log1 = self.bot.get_channel(983753547705372722)
        log2 = self.bot.get_channel(983753718094766152)
        log3 = self.bot.get_channel(983753740093911090)
        
        
        # 入退出処理
        if member.bot is False:
            # 入退出以外は弾く
            if before.channel != after.channel:
                # 退出
                if before.channel is not None and before.channel != stage:


                    # 通知
                    embed = discord.Embed(title="VC退出", colour=discord.Colour(0xd0021b), description="ユーザーが退出しました", timestamp=datetime.now())

                    embed.set_author(name=member.name, icon_url=member.display_avatar.url)
                    embed.set_footer(text="VC入退出通知")

                    await before.channel.send(embed=embed)
                    
                    # ロック時等の処理
                    if before.channel == self.bot.vc1:
                        await self.bot.vc1.edit(name='VC-1(128Kbps)')
                        if self.bot.vc1_status == 'Lock' or self.bot.vc1_status == 'Permit':
                            await self.bot.vc1.set_permissions(member, connect=None)
                    elif before.channel == self.bot.vc2:
                        await self.bot.vc2.edit(name='VC-2(128Kbps)')
                        if self.bot.vc2_status == 'Lock' or self.bot.vc2_status == 'Permit':
                            await self.bot.vc2.set_permissions(member, connect=None)
                    elif before.channel == self.bot.vc3:
                        await self.bot.vc3.edit(name='VC-3(64Kbps)')
                        if self.bot.vc3_status == 'Lock' or self.bot.vc3_status == 'Permit':
                            await self.bot.vc3.set_permissions(member, connect=None)
                    
                    # チャンネル初期化
                    if len(before.channel.members) == 0:
                        msg = await before.channel.send(embed=discord.Embed(title='チャンネルリセット中...', description='VCに誰もいなくなったためチャンネルをリセットしています', color=0x00ffff))
                        await before.channel.purge(limit=None, check=purge_check)
                        await msg.delete()
                        if before.channel == self.bot.vc1:
                            await self.bot.vc1.edit(name='VC-1(128Kbps)')
                        elif before.channel == self.bot.vc2:
                            await self.bot.vc2.edit(name='VC-2(128Kbps)')
                        elif before.channel == self.bot.vc3:
                            await self.bot.vc3.edit(name='VC-3(64Kbps)')
                        await before.channel.edit(sync_permissions=True)
                        await status.set(self, before.channel, 'Normal')
                        
                        if before.channel.nsfw == True:
                            await before.channel.edit(nsfw=False)

                    # オーナー変更
                    else:
                        if await owner.check(self, member, before.channel) != None:
                            await owner.change(self, before.channel)
                    
                # 入室
                if after.channel is not None and after.channel != stage:
                    # オーナー指定
                    
                    await owner.setup(self, member, after)
                    
                    embed = discord.Embed(title = "VC入室", colour = discord.Colour(0x7ed321), description = "ユーザーが入室しました", timestamp = datetime.now())

                    embed.set_author(name=member.name, icon_url=member.display_avatar.url)
                    embed.set_footer(text="VC入退出通知")

                    await after.channel.send(embed=embed)
                    


            

async def setup(bot):
    await bot.add_cog(vctool(bot))
