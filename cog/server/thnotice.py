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
    @discord.ui.button(label='้็ฅใใ', style=discord.ButtonStyle.green, emoji='๐')
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner.id:
            await interaction.response.send_message('้็ฅใใพใใ', ephemeral=True)
            self.value = True
            self.stop()
        else:
            await interaction.response.send_message('ในใฌใใใฎไฝๆ่ใงใฏใชใใใๅฎ่กใงใใพใใ', ephemeral=True)

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='้็ฅใใชใ', style=discord.ButtonStyle.grey, emoji='๐')
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner.id:
            await interaction.response.send_message('ใญใฃใณใปใซใใพใใ', ephemeral=True)
            self.value = False
            self.stop()
        else:
            await interaction.response.send_message('ในใฌใใใฎไฝๆ่ใงใฏใชใใใๅฎ่กใงใใพใใ', ephemeral=True)




class thnotice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.noticech = bot.get_channel(975618002953318420)
        self.noticerole = bot.guild.get_role(956128433660899358)
    
    @commands.Cog.listener()
    async def on_thread_create(self,thread):
        await thread.join()
        print(f'ในใฌใใไฝๆ: {thread.name}')
        
        embed = discord.Embed(title="ในใฌใใ้็ฅ", colour=discord.Colour(0x47ddcc), description="ใใฎในใฌใใใ้็ฅใใพใใ?")
        view =  NoticeButton(thread.owner)
        message = await thread.send(embed = embed, view = view, delete_after = 60)

        await view.wait()
        if view.value == True:
            
            await message.delete()
            
            embed = discord.Embed(title="ในใฌใใ้็ฅ", colour=0xff00, description="ๆฐใใในใฌใใใไฝๆใใใพใใ", timestamp=datetime.now())
            embed.set_footer(text="ใใใผใฃใจ", icon_url="https://cdn.discordapp.com/attachments/733707711228674102/975786870309007471/Discord-Logo-Color.png")
            embed.add_field(name="ในใฌใใๅ", value=f'[{thread.name}](https://discord.com/channels/733707710784340100733707710784340100/{thread.id})', inline=False)
            embed.add_field(name="ในใฌใใID", value=thread.id, inline=False)
            embed.add_field(name="ในใฌใใใไฝๆใใใใใฃใณใใซ", value=thread.parent, inline=True)
            embed.add_field(name="ในใฌใใไฝๆ่", value=thread.owner.mention, inline=True)

            await self.noticech.send(content=self.noticerole.mention, embed=embed)
        
        elif view.value == False:
            await message.delete()
        

    @commands.Cog.listener()
    async def on_thread_update(self, before, after):
        print(before.archived, after.archived)
        
        if before.locked is False and after.locked is True:
            embed = discord.Embed(title="ในใฌใใ้็ฅ", colour=0xd2691e, description="ในใฌใใใใญใใฏใใใพใใ", timestamp=datetime.now())

            embed.set_footer(text="ใใใผใฃใจ", icon_url="https://cdn.discordapp.com/attachments/733707711228674102/975786870309007471/Discord-Logo-Color.png")

            embed.add_field(name="ในใฌใใๅ", value=f'[{after.name}](https://discord.com/channels/733707710784340100733707710784340100/{after.id})')
            embed.add_field(name="ในใฌใใID", value=after.id, inline=True)
            embed.add_field(name="ในใฌใใใใญใใฏใใใใใฃใณใใซ", value=after.parent)
            embed.add_field(name="ในใฌใใไฝๆ่", value=after.owner.mention, inline=True)

            await self.noticech.send(embed=embed)
            print(f'ในใฌใใใญใใฏ: {after.name}')
            return 
        
        elif before.archived is False and after.archived is True or before.locked is False and after.locked is True:
            embed = discord.Embed(title="ในใฌใใ้็ฅ", colour=0xFFFF, description="ในใฌใใใใขใผใซใคใใใใพใใ", timestamp=datetime.now())

            embed.set_footer(text="ใใใผใฃใจ", icon_url="https://cdn.discordapp.com/attachments/733707711228674102/975786870309007471/Discord-Logo-Color.png")

            embed.add_field(name="ในใฌใใๅ", value=f'[{after.name}](https://discord.com/channels/733707710784340100733707710784340100/{after.id})')
            embed.add_field(name="ในใฌใใID", value=after.id, inline=True)
            embed.add_field(name="ในใฌใใใใขใผใซใคใใใใใใฃใณใใซ", value=after.parent)
            embed.add_field(name="ในใฌใใไฝๆ่", value=after.owner.mention, inline=True)

            await self.noticech.send(embed=embed)
            print(f'ในใฌใใใขใผใซใคใ: {after.name}')
            return 
        

        
        elif before.locked is True and after.locked is False:
            await self.bot.owner.send('ใญใใฏ่งฃ้คใใใใ๏ผ')
            print(f'ใญใใฏ่งฃ้ค: {after.name}')
            return
    
        elif before.archived is True and after.archived is False:
            await self.bot.owner.send('ใขใผใซใคใ่งฃ้คใใใใ๏ผ')
            print(f'ใขใผใซใคใ่งฃ้ค: {after.name}')
        

    @commands.Cog.listener()
    async def on_raw_thread_delete(self, payload):
        thread = payload.thread
        if thread is not None:
            embed = discord.Embed(title="ในใฌใใ้็ฅ", colour=0xff4500, description="ในใฌใใใๅ้คใใใพใใ", timestamp=datetime.now())
            embed.set_footer(text="ใใใผใฃใจ", icon_url="https://cdn.discordapp.com/attachments/733707711228674102/975786870309007471/Discord-Logo-Color.png")
            embed.add_field(name="ในใฌใใๅ", value=f'[{thread.name}](https://discord.com/channels/733707710784340100733707710784340100/{thread.id})', inline=False)
            embed.add_field(name="ในใฌใใID", value=thread.id, inline=False)
            embed.add_field(name="ในใฌใใใๅ้คใใใใใฃใณใใซ", value=thread.parent, inline=True)
            embed.add_field(name="ในใฌใใไฝๆ่", value=thread.owner.mention, inline=True)
            print(f'ในใฌใใๅ้ค: {thread.name}')
        else:
            embed = discord.Embed(title="ในใฌใใ้็ฅ", colour=0xff4500, description="ใขใผใซใคใ/ใญใใฏๆธใฎในใฌใใใๅ้คใใใพใใ", timestamp=datetime.now())
            embed.set_footer(text="ใใใผใฃใจ", icon_url="https://cdn.discordapp.com/attachments/733707711228674102/975786870309007471/Discord-Logo-Color.png")
            embed.add_field(name="ในใฌใใID", value=payload.thread_id, inline=False)
            embed.add_field(name="ในใฌใใใๅ้คใใใใใฃใณใใซ", value=self.bot.get_channel(payload.parent_id).name, inline=True)
            print('ในใฌใใๅ้ค(ใญใฃใใทใฅ็ก)')
        await self.noticech.send(embed=embed)




async def setup(bot):
    await bot.add_cog(thnotice(bot))
