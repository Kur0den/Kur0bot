import discord
from discord.ext import commands
from datetime import datetime



class NoticeButton(discord.ui.View):
    def __init__(self, owner):
        super().__init__()
        self.value = None
        self.owner = owner

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='通知する', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner.id:
            await interaction.response.send_message('通知しました', ephemeral=True)
            self.value = True
            self.stop()
        else:
            await interaction.response.send_message('スレッドの作成者ではないため実行できません', ephemeral=True)

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='通知しない', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner.id:
            await interaction.response.send_message('キャンセルしました', ephemeral=True)
            self.value = False
            self.stop()
        else:
            await interaction.response.send_message('スレッドの作成者ではないため実行できません', ephemeral=True)




class thnotice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.noticech = bot.get_channel(975618002953318420)
        self.noticerole = bot.guild.get_role(956128433660899358)
    
    @commands.Cog.listener()
    async def on_thread_create(self,thread):
        
        print(f'スレッド作成:{thread.name}')
        
        embed = discord.Embed(title="スレッド通知", colour=discord.Colour(0x47ddcc), description="このスレッドを通知しますか?")
        view =  NoticeButton(thread.owner)
        message = await thread.send(embed = embed, view = view, delete_after = 60)

        await view.wait()
        if view.value == True:
            
            await message.delete()
            
            embed = discord.Embed(title="スレッド通知", colour=0xff00, description="新しいスレッドが作成されました", timestamp=datetime.now())
            embed.set_footer(text="くろぼっと", icon_url="https://cdn.discordapp.com/attachments/733707711228674102/975786870309007471/Discord-Logo-Color.png")
            embed.add_field(name="スレッド名", value=f'[{thread.name}](https://discord.com/channels/733707710784340100733707710784340100/{thread.id})', inline=False)
            embed.add_field(name="スレッドID", value=thread.id, inline=False)
            embed.add_field(name="スレッドが作成されたチャンネル", value=thread.parent, inline=True)
            embed.add_field(name="スレッド作成者", value=thread.owner.mention, inline=True)

            await self.noticech.send(content=self.noticerole.mention, embed=embed)
        
        elif view.value == False:
            await message.delete()
        

    @commands.Cog.listener()
    async def on_thread_update(self, before, after):
        if before.archived is False and after.archived is True:
            embed = discord.Embed(title="スレッド通知", colour=0xFFFF, description="スレッドがアーカイブされました", timestamp=datetime.now())

            embed.set_footer(text="くろぼっと", icon_url="https://cdn.discordapp.com/attachments/733707711228674102/975786870309007471/Discord-Logo-Color.png")

            embed.add_field(name="スレッド名", value=f'[{after.name}](https://discord.com/channels/733707710784340100733707710784340100/{after.id})')
            embed.add_field(name="スレッドID", value=after.id, inline=True)
            embed.add_field(name="スレッドがアーカイブされたチャンネル", value=after.parent)
            embed.add_field(name="スレッド作成者", value=after.owner.mention, inline=True)

            await self.noticech.send(content=self.noticerole.mention, embed=embed)
            print(f'スレッドアーカイブ:{after.name}')
            return
        
        elif before.archived is True and after.archived is False:
            await bot.owner.send('アーカイブ解除されたよ！')
            print(f'アーカイブ解除:{after.name}')
    
    @commands.Cog.listener()
    async def on_thread_remove():
        await self.bot.owner.send(f'remove:{thread}')

async def setup(bot):
    await bot.add_cog(thnotice(bot))
