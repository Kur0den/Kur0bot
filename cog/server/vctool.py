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
                self.bot.vc1_dash = await self.bot.vc1.send('test', view=dashboard(self))
                await self.bot.vc1.send(f'{member.mention}は{after.channel}の所有権を持っています', delete_after=60)
            elif after.channel == self.bot.vc2:
                self.bot.vc2_owner = member
                self.bot.vc2_dash = await self.bot.vc2.send('test', view=dashboard(self))
                await self.bot.vc2.send(f'{member.mention}は{after.channel}の所有権を持っています', delete_after=60)
            elif after.channel == self.bot.vc3:
                self.bot.vc3_owner = member
                self.bot.vc3_dash = await self.bot.vc3.send('test', view=dashboard(self))
                await self.bot.vc3.send(f'{member.mention}は{after.channel}の所有権を持っています', delete_after=60)
    
    # オーナーチェック
    async def check(self, member, channel):
        try:
            if channel == self.bot.vc1 and member == self.bot.vc1_owner:
                result = 'vc1'
            elif channel == self.bot.vc2 and member == self.bot.vc2_owner:
                result = 'vc2'
            elif channel == self.bot.vc3 and member == self.bot.vc3_owner:
                result = 'vc3'
            else:
                result = None
        except(AttributeError):
            if channel == self.bot.bot.vc1 and member == self.bot.bot.vc1_owner:
                result = 'vc1'
            elif channel == self.bot.bot.vc2 and member == self.bot.bot.vc2_owner:
                result = 'vc2'
            elif channel == self.bot.bot.vc3 and member == self.bot.bot.vc3_owner:
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
            self.bot.vc1_dash = await self.bot.vc1.send('test', view=dashboard(self))
            self.bot.vc1_owner = random.choice(member)
            await channel.send(f'{self.bot.vc1_owner.mention}は{channel}の所有権を持っています', delete_after=60)
        elif channel == self.bot.vc2:
            await self.bot.vc2_dash.delete()
            self.bot.vc2_dash = await self.bot.vc2.send('test', view=dashboard(self))
            self.bot.vc2_owner = random.choice(member)
            await channel.send(f'{self.bot.vc2_owner.mention}は{channel}の所有権を持っています', delete_after=60)
        elif channel == self.bot.vc3:
            await self.bot.vc3_dash.delete()
            self.bot.vc3_dash = await self.bot.vc3.send('test', view=dashboard(self))
            self.bot.vc3_owner = random.choice(member)
            await channel.send(f'{self.bot.vc3_owner.mention}は{channel}の所有権を持っています', delete_after=60)

class perm():
    def __init__(self, bot):
        super().__init__()
    
    async def setstatus(self, chanel, status):
        try:
            if chanel == self.bot.vc1:
                self.bot.vc1_status = status
            elif chanel == self.bot.vc2:
                self.bot.vc2_status = status
            elif chanel == self.bot.vc3:
                self.bot.vc3_status = status
        except(AttributeError):
            if chanel == self.bot.bot.vc1:
                self.bot.bot.vc1_status = status
            elif chanel == self.bot.bot.vc2:
                self.bot.bot.vc2_status = status
            elif chanel == self.bot.bot.vc3:
                self.bot.bot.vc3_status = status
    
    async def checkstatus(self, channel):
        try:
            if channel == self.bot.vc1:
                result = self.bot.vc1_status
            elif channel == self.bot.vc2:
                result  = self.bot.vc2_status
            elif channel == self.bot.vc3:
                result = self.bot.vc3_status
        except(AttributeError):
            if channel == self.bot.bot.vc1:
                result = self.bot.bot.vc1_status
            elif channel == self.bot.bot.vc2:
                result  = self.bot.bot.vc2_status
            elif channel == self.bot.bot.vc3:
                result = self.bot.bot.vc3_status
        return result




# ダッシュボード用のやつ
class dashboard(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        discord.ui.view.timeout = None # タイムアウトをなしに
        self.bot = bot
    
    # 部屋関係
    @discord.ui.button(label='通常モード', style=discord.ButtonStyle.green, emoji='✅', row=1)
    async def nomal(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await owner.check(self, interaction.user, interaction.channel) != None:
            if await perm.checkstatus(self, interaction.channel) != 'Nomal':
                await interaction.channel.edit(sync_permissions=True)
                await perm.setstatus(self, interaction.channel, 'Nomal')
            else:
                await interaction.response.send_message('すでに通常モードに設定されています', ephemeral=True)

        '''if result == 'vc1':
            await interaction.response.send_message('vc1', ephemeral=True)
        elif result == 'vc2':
            await interaction.response.send_message('vc2', ephemeral=True)
        elif result == 'vc3':
            await interaction.response.send_message('vc3', ephemeral=True)
        else:
            await interaction.response.send_message('VCのオーナーではないため実行できません', ephemeral=True)'''


    @discord.ui.button(label='許可モード', style=discord.ButtonStyle.secondary, emoji='📩', row=1)
    async def mode(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = await owner.check(self, interaction.user, interaction.channel)
        if result == 'vc1':
            await interaction.response.send_message('vc1', ephemeral=True)
        elif result == 'vc2':
            await interaction.response.send_message('vc2', ephemeral=True)
        elif result == 'vc3':
            await interaction.response.send_message('vc3', ephemeral=True)
        else:
            await interaction.response.send_message('VCのオーナーではないため実行できません', ephemeral=True)


    @discord.ui.button(label='ロック', style=discord.ButtonStyle.secondary, emoji='🔒', row=1)
    async def lock(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = await owner.check(self, interaction.user, interaction.channel)
        if result == 'vc1':
            await interaction.response.send_message('vc1', ephemeral=True)
        elif result == 'vc2':
            await interaction.response.send_message('vc2', ephemeral=True)
        elif result == 'vc3':
            await interaction.response.send_message('vc3', ephemeral=True)
        else:
            await interaction.response.send_message('VCのオーナーではないため実行できません', ephemeral=True)


    @discord.ui.button(label='NSFW', style=discord.ButtonStyle.secondary, emoji='🔞', row=2)
    async def nsfw(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = await owner.check(self, interaction.user, interaction.channel)
        if result == 'vc1':
            await interaction.response.send_message('vc1', ephemeral=True)
        elif result == 'vc2':
            await interaction.response.send_message('vc2', ephemeral=True)
        elif result == 'vc3':
            await interaction.response.send_message('vc3', ephemeral=True)
        else:
            await interaction.response.send_message('VCのオーナーではないため実行できません', ephemeral=True)


    @discord.ui.button(label='名前変更', style=discord.ButtonStyle.secondary, emoji='📝', row=2)
    async def rename(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = await owner.check(self, interaction.user, interaction.channel)
        if result == 'vc1':
            await interaction.response.send_message('vc1', ephemeral=True)
        elif result == 'vc2':
            await interaction.response.send_message('vc2', ephemeral=True)
        elif result == 'vc3':
            await interaction.response.send_message('vc3', ephemeral=True)
        else:
            await interaction.response.send_message('VCのオーナーではないため実行できません', ephemeral=True)


    @discord.ui.button(label='発言禁止', style=discord.ButtonStyle.secondary, emoji='🔇', row=2)
    async def mute(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = await owner.check(self, interaction.user, interaction.channel)
        if result == 'vc1':
            await interaction.response.send_message('vc1', ephemeral=True)
        elif result == 'vc2':
            await interaction.response.send_message('vc2', ephemeral=True)
        elif result == 'vc3':
            await interaction.response.send_message('vc3', ephemeral=True)
        else:
            await interaction.response.send_message('VCのオーナーではないため実行できません', ephemeral=True)



    # ユーザー関係
    @discord.ui.button(label='キック', style=discord.ButtonStyle.secondary, emoji='🦵', row=3)
    async def kick(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = await owner.check(self, interaction.user, interaction.channel)
        if result == 'vc1':
            await interaction.response.send_message('vc1', ephemeral=True)
        elif result == 'vc2':
            await interaction.response.send_message('vc2', ephemeral=True)
        elif result == 'vc3':
            await interaction.response.send_message('vc3', ephemeral=True)
        else:
            await interaction.response.send_message('VCのオーナーではないため実行できません', ephemeral=True)


    @discord.ui.button(label='オーナー変更', style=discord.ButtonStyle.secondary, emoji='🔑', row=3)
    async def change(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = await owner.check(self, interaction.user, interaction.channel)
        if result == 'vc1':
            await interaction.response.send_message('vc1', ephemeral=True)
        elif result == 'vc2':
            await interaction.response.send_message('vc2', ephemeral=True)
        elif result == 'vc3':
            await interaction.response.send_message('vc3', ephemeral=True)
        else:
            await interaction.response.send_message('VCのオーナーではないため実行できません', ephemeral=True)






class vctool(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        


    @commands.command()
    async def vctool(self, ctx):
        if ctx.channel is self.bot.vc1:
            await self.bot.vc1_dash.delete()
            self.bot.vc1_dash = await ctx.send('test', view=dashboard(self))
        elif ctx.channel is self.bot.vc2:
            await self.bot.vc2_dash.delete()
            self.bot.vc2_dash = await ctx.send('test', view=dashboard(self))
        elif ctx.channel is self.bot.vc3:
            await self.bot.vc3_dash.delete()
            self.bot.vc3_dash = await ctx.send('test', view=dashboard(self))
        else:
            await ctx.send('チャンネルが違うで')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        
        stage = self.bot.get_channel(884734698759266324)
        log1 = self.bot.get_channel(983753547705372722)
        log2 = self.bot.get_channel(983753718094766152)
        log3 = self.bot.get_channel(983753740093911090)
        
        
        # 入退出ログ(処理用のものも)
        if member.bot is False:
            # 入退出以外は弾く
            if before.channel != after.channel:
                # 退出
                if before.channel is not None and before.channel != stage:



                    embed = discord.Embed(title="VC退出", colour=discord.Colour(0xd0021b), description="ユーザーが退出しました", timestamp=datetime.now())

                    embed.set_author(name=member.name, icon_url=member.display_avatar.url)
                    embed.set_footer(text="VC入退出通知")

                    await before.channel.send(embed=embed)
                    
                    if len(before.channel.members) == 0:
                        msg = await before.channel.send(embed=discord.Embed(title='チャンネルリセット中...', description='VCに誰もいなくなったためチャンネルをリセットしています', color=0x00ffff))
                        await before.channel.purge(limit=None, check=purge_check)
                        await msg.delete()
                        
                        await before.channel.edit(sync_permissions=True)
                        await perm.setstatus(self, before.channel, 'Nomal')

                    
                    else:
                        if await owner.check(self, member, before.channel) != None:
                            await owner.change(self, before.channel)
                    
                # 入室
                if after.channel is not None and after.channel != stage:
                    # オーナー指定
                    
                    result = await owner.setup(self, member, after)
                    
                    embed = discord.Embed(title = "VC入室", colour = discord.Colour(0x7ed321), description = "ユーザーが入室しました", timestamp = datetime.now())

                    embed.set_author(name=member.name, icon_url=member.display_avatar.url)
                    embed.set_footer(text="VC入退出通知")

                    await after.channel.send(embed=embed)
                    


            

async def setup(bot):
    await bot.add_cog(vctool(bot))
