import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime




class NoticeButton(discord.ui.View):
    def __init__(self, owner):
        super().__init__()
        self.value = None
        self.owner = owner

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='通知する', style=discord.ButtonStyle.green, emoji='🔔')
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner.id:
            await interaction.response.send_message('通知しました', ephemeral=True)
            self.value = True
            self.stop()
        else:
            await interaction.response.send_message('スレッドの作成者ではないため実行できません', ephemeral=True)

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='通知しない', style=discord.ButtonStyle.grey, emoji='🔕')
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner.id:
            await interaction.response.send_message('キャンセルしました', ephemeral=True)
            self.value = False
            self.stop()
        else:
            await interaction.response.send_message('スレッドの作成者ではないため実行できません', ephemeral=True)

class CloseButton(discord.ui.View):
    def __init__(self, owner):
        super().__init__()
        self.value = None
        self.owner = owner

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='アーカイブする', style=discord.ButtonStyle.red, emoji='🔔')
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner.id:
            await interaction.response.send_message('アーカイブしました', ephemeral=True)
            self.value = True
            self.stop()
        else:
            await interaction.response.send_message('スレッドの作成者ではないため実行できません', ephemeral=True)

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='アーカイブしない', style=discord.ButtonStyle.green, emoji='🔕')
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner.id:
            await interaction.response.send_message('キャンセルしました', ephemeral=True)
            self.value = False
            self.stop()
        else:
            await interaction.response.send_message('スレッドの作成者ではないため実行できません', ephemeral=True)




class thmanager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.noticech = bot.get_channel(975618002953318420)
        self.noticerole = bot.guild.get_role(956128433660899358)
    
    group = app_commands.Group(name="thread", description="Thread manager", guild_ids=[733707710784340100], guild_only=True)

    @commands.Cog.listener()
    async def on_thread_create(self,thread):
        await thread.join()
        if not thread.parent.type is discord.ChannelType.forum:
            print(f'スレッド作成: {thread.name}')
            
            embed = discord.Embed(title="Thread Manager", colour=discord.Colour(0x47ddcc), description="このスレッドを通知しますか?")
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
        if not before.parent.type is discord.ChannelType.forum:
            print(before.archived, after.archived)
            
            if before.locked is False and after.locked is True:
                embed = discord.Embed(title="スレッド通知", colour=0xd2691e, description="スレッドがロックされました", timestamp=datetime.now())

                embed.set_footer(text="くろぼっと", icon_url="https://cdn.discordapp.com/attachments/733707711228674102/975786870309007471/Discord-Logo-Color.png")

                embed.add_field(name="スレッド名", value=f'[{after.name}](https://discord.com/channels/733707710784340100/{after.id})')
                embed.add_field(name="スレッドID", value=after.id, inline=True)
                embed.add_field(name="スレッドがロックされたチャンネル", value=after.parent)
                embed.add_field(name="スレッド作成者", value=after.owner.mention, inline=True)

                await self.noticech.send(embed=embed)
                print(f'スレッドロック: {after.name}')
                return
            
            elif before.archived is False and after.archived is True or before.locked is False and after.locked is True:
                embed = discord.Embed(title="スレッド通知", colour=0xFFFF, description="スレッドがアーカイブされました", timestamp=datetime.now())

                embed.set_footer(text="くろぼっと", icon_url="https://cdn.discordapp.com/attachments/733707711228674102/975786870309007471/Discord-Logo-Color.png")

                embed.add_field(name="スレッド名", value=f'[{after.name}](https://discord.com/channels/733707710784340100/{after.id})')
                embed.add_field(name="スレッドID", value=after.id, inline=True)
                embed.add_field(name="スレッドがアーカイブされたチャンネル", value=after.parent)
                embed.add_field(name="スレッド作成者", value=after.owner.mention, inline=True)

                await self.noticech.send(embed=embed)
                print(f'スレッドアーカイブ: {after.name}')
                return
            

            
            elif before.locked is True and after.locked is False:
                await self.bot.owner.send('ロックが解除されたよ！')
                print(f'ロック解除: {after.name}')
                return
        
            elif before.archived is True and after.archived is False:
                await self.bot.owner.send('アーカイブが解除されたよ！')
                print(f'アーカイブ解除: {after.name}')
        

    @commands.Cog.listener()
    async def on_raw_thread_delete(self, payload):
            thread = payload.thread
            if thread is not None:
                embed = discord.Embed(title="スレッド通知", colour=0xff4500, description="スレッドが削除されました", timestamp=datetime.now())
                embed.set_footer(text="くろぼっと", icon_url="https://cdn.discordapp.com/attachments/733707711228674102/975786870309007471/Discord-Logo-Color.png")
                embed.add_field(name="スレッド名", value=f'[{thread.name}](https://discord.com/channels/733707710784340100/{thread.id})', inline=False)
                embed.add_field(name="スレッドID", value=thread.id, inline=False)
                embed.add_field(name="スレッドが削除されたチャンネル", value=thread.parent, inline=True)
                embed.add_field(name="スレッド作成者", value=thread.owner.mention, inline=True)
                print(f'スレッド削除: {thread.name}')
            else:
                embed = discord.Embed(title="スレッド通知", colour=0xff4500, description="アーカイブ/ロック済のスレッドが削除されました", timestamp=datetime.now())
                embed.set_footer(text="くろぼっと", icon_url="https://cdn.discordapp.com/attachments/733707711228674102/975786870309007471/Discord-Logo-Color.png")
                embed.add_field(name="スレッドID", value=payload.thread_id, inline=False)
                embed.add_field(name="スレッドが削除されたチャンネル", value=self.bot.get_channel(payload.parent_id).name, inline=True)
                print('スレッド削除(キャッシュ無)')
            await self.noticech.send(embed=embed)
    
    
    @group.command(name="lock", description='スレッドをロックします')
    @app_commands.guild_only()
    async def thclose(self, interaction):
        if interaction.channel.type is (discord.ChannelType.public_thread or discord.ChannelType.private_thread):
            if interaction.user.id is interaction.channel.owner.id:
                embed = discord.Embed(title="Thread Manager", colour=discord.Colour(0xff0000), description="このスレッドをロックしますか?")
                view =  CloseButton(interaction.channel.owner)
                await interaction.response.send_message(embed = embed, view = view, ephemeral=True)

                await view.wait()
                if view.value == True:
                    await interaction.channel.edit(archived=True, locked=True, reason=f'スレッドアーカイブコマンド\n実行者: {interaction.user}')
            else:
                await interaction.response.send_message('スレッドの作成者ではないため実行できません',ephemeral=True)
        else:
            await interaction.response.send_message('このコマンドはスレッド又はフォーラムチャンネルでのみ実行可能です',ephemeral=True)

    @group.command(name="pin", description="メッセージをピン留めします")
    @app_commands.guild_only()
    async def pin(self, interaction, message_id):
        if interaction.channel.type is (discord.ChannelType.public_thread or discord.ChannelType.private_thread):
            if interaction.user.id is interaction.channel.owner.id:
                await interaction.channel.pin(message_id)
                await interaction.response.send_message("ピン留めしました。", ephemeral=True)
            else:
                await interaction.response.send_message('スレッドの作成者ではないため実行できません',ephemeral=True)
        else:
            await interaction.response.send_message('このコマンドはスレッド又はフォーラムチャンネルでのみ実行可能です',ephemeral=True)



async def setup(bot):
    await bot.add_cog(thmanager(bot))
