import discord
from discord.ext import commands
from datetime import datetime



def purge_check(m):    return not m.embeds[0].title in ['VCダッシュボード', 'チャンネルリセット中...'] if bool(m.embeds) else True


class owner():
    def __init__(self, bot):
        super().__init__()
        self.vcowner = None
        self.bot = bot
    
    async def setup(self, member, after, vcowner):
        if len(after.channel.members) == 1:
            if after.channel == self.bot.vc1:
                self.bot.vc1_owner = member
                vcowner = True
                return vcowner
            elif after.channel == self.bot.vc2:
                self.bot.vc2_owner = member
                vcowner = True
                return vcowner
            elif after.channel == self.bot.vc3:
                self.bot.vc3_owner = member
                vcowner = True
                return vcowner
    
    async def check(self, interaction, result):
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


class dashboard(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    @discord.ui.button(label='ロック', style=discord.ButtonStyle.green, emoji='🔒')
    async def lock(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = None
        await owner.check(self, interaction, result)
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
        

    @commands.command()
    async def senddash(self, ctx):
        if (ctx.channel is self.bot.vc1 or
            ctx.channel is self.bot.vc2 or
            ctx.channel is self.bot.vc3):
            await ctx.send('test', view=dashboard(self))
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
                    #if before.channel == vc1:
                    #    async for msg in log1.history():
                    #        if msg.content.startswith(str(member.id)):
                    #            await msg.delete()
                    #elif before.channel == log2:
                    #    async for msg in vc2.history():
                    #        if msg.content.startswith(str(member.id)):
                    #            await msg.delete()
                    #elif before.channel == log3:
                    #    async for msg in vc3.history():
                    #        if msg.content.startswith(str(member.id)):
                    #            await msg.delete()

                    embed = discord.Embed(title="VC退出", colour=discord.Colour(0xd0021b), description="ユーザーが退出しました", timestamp=datetime.now())

                    embed.set_author(name=member.name, icon_url=member.display_avatar.url)
                    embed.set_footer(text="VC入退出通知")

                    await before.channel.send(embed=embed)
                    
                    if len(before.channel.members) == 0:
                        msg = await before.channel.send(embed=discord.Embed(title='チャンネルリセット中...', description='VCに誰もいなくなったためチャンネルをリセットしています', color=0x00ffff))
                        await before.channel.purge(limit=None, check=purge_check)
                        await msg.delete()
                    
                # 入室
                if after.channel is not None and after.channel != stage:
                    # オーナー指定
                    await owner.setup(self, member, after)
                    
                    embed = discord.Embed(title = "VC入室", colour = discord.Colour(0x7ed321), description = "ユーザーが入室しました", timestamp = datetime.now())

                    embed.set_author(name=member.name, icon_url=member.display_avatar.url)
                    embed.set_footer(text="VC入退出通知")

                    await after.channel.send(embed=embed)
                    
                    if owner.vcowner == True:
                        await ctx.send(f'{member.mention}は{after.channel}の所有権を持っています')

            

async def setup(bot):
    await bot.add_cog(vctool(bot))
