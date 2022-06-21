import discord
from discord.ext import commands
from datetime import datetime
import random



def purge_check(m):    return not m.embeds[0].title in ['VCダッシュボード', 'チャンネルリセット中...'] if bool(m.embeds) else True


class owner():
    def __init__(self, bot):
        super().__init__()
        self.vcowner = None
        self.bot = bot
    
    # オーナー設定
    async def setup(self, member, after, result):
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
    
    # ボタン用オーナーチェック
    async def buttoncheck(self, interaction, result):
        if interaction.channel == self.bot.bot.vc1 and interaction.user == self.bot.bot.vc1_owner:
            result = 'vc1'
            return result
        elif interaction.channel == self.bot.bot.vc2 and interaction.user == self.bot.bot.vc2_owner:
            result = 'vc2'
            return result
        elif interaction.channel == self.bot.bot.vc3 and interaction.user == self.bot.bot.vc3_owner:
            result = 'vc3'
            return result
        else:
            result = None
            return result
    
    # それ以外用オーナーチェック
    async def usercheck(self, member, before, result):
        if before.channel == self.bot.vc1 and member == self.bot.vc1_owner:
            result = 'vc1'
            return result
        elif before.channel == self.bot.vc2 and member == self.bot.vc2_owner:
            result = 'vc2'
            return result
        elif before.channel == self.bot.vc3 and member == self.bot.vc3_owner:
            result = 'vc3'
            return result
        else:
            result = None
            return result
    
    # オーナー変更
    async def change(self, channel, result):
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



class dashboard(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        discord.ui.view.timeout = None
    
    @discord.ui.button(label='ロック', style=discord.ButtonStyle.green, emoji='🔒', row=1)
    async def lock(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = None
        result = await owner.buttoncheck(self, interaction, result)
        if result == 'vc1':
            await interaction.response.send_message('vc1', ephemeral=True)
        elif result == 'vc2':
            await interaction.response.send_message('vc2', ephemeral=True)
        elif result == 'vc3':
            await interaction.response.send_message('vc3', ephemeral=True)
        else:
            await interaction.response.send_message('VCのオーナーではないため実行できません', ephemeral=True)


    @discord.ui.button(label='許可モード', style=discord.ButtonStyle.grey, emoji='📩')
    async def mode(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner.id:
            await interaction.response.send_message('キャンセルしました', ephemeral=True)
            self.value = False
            self.stop()
        else:
            await interaction.response.send_message('スレッドの作成者ではないため実行できません', ephemeral=True)



class vctool(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        


    

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
                    else:
                        result = await owner.usercheck(self, member, before, None)
                    
                        if result != None:
                            await owner.change(self, before.channel, None)
                    
                # 入室
                if after.channel is not None and after.channel != stage:
                    # オーナー指定
                    
                    result = await owner.setup(self, member, after, None)
                    
                    embed = discord.Embed(title = "VC入室", colour = discord.Colour(0x7ed321), description = "ユーザーが入室しました", timestamp = datetime.now())

                    embed.set_author(name=member.name, icon_url=member.display_avatar.url)
                    embed.set_footer(text="VC入退出通知")

                    await after.channel.send(embed=embed)
                    


            

async def setup(bot):
    await bot.add_cog(vctool(bot))
