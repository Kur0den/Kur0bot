import discord
from discord.ext import commands
from datetime import datetime



def purge_check(m):    return not m.embeds[0].title in ['VCダッシュボード', 'チャンネルリセット中...'] if bool(m.embeds) else True


class dashboard(discord.ui.View):
    def __init__(self, owner,):
        super().__init__()
        self.value = None
        self.owner = owner


    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='ロック', style=discord.ButtonStyle.green, emoji='🔒️')
    async def lock(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner.id:
            await interaction.response.send_message('', ephemeral=True)
            
        else:
            await interaction.response.send_message('スレッドの作成者ではないため実行できません', ephemeral=True)

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='許可モード', style=discord.ButtonStyle.grey, emoji='🔕')
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
        self.vc1_owner = None
        self.vc2_owner = None
        self.vc3_owner = None
        

    @commands.command()
    async def senddash(self, ctx):
        await ctx.send('test')
    

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        
        stage = self.bot.get_channel(884734698759266324)
        log1 = self.bot.get_channel(983753547705372722)
        log2 = self.bot.get_channel(983753718094766152)
        log3 = self.bot.get_channel(983753740093911090)
        
        vc1 = self.bot.get_channel(981800095760670730)
        vc2 = self.bot.get_channel(981800262165495828)
        vc3 = self.bot.get_channel(981800316116803636)
        
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
                    if len(after.chanel.members) == 0:
                        if after.channel == vc1:
                            self.vc1_owner = member
                        elif after.channel == vc2:
                            self.vc2_owner = member
                        elif after.channel == vc3:
                            self.vc3_owner = member
                    
                    embed = discord.Embed(title = "VC入室", colour = discord.Colour(0x7ed321), description = "ユーザーが入室しました", timestamp = datetime.now())

                    embed.set_author(name=member.name, icon_url=member.display_avatar.url)
                    embed.set_footer(text="VC入退出通知")

                    await after.channel.send(embed=embed)

            

async def setup(bot):
    await bot.add_cog(vctool(bot))
