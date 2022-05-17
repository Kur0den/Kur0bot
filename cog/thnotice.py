import discord
from discord.ext import commands
from datetime import datetime

class thnotice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.noticech = bot.get_channel(975618002953318420)
        self.noticerole = bot.guild.get_role(956128433660899358)
    
    @commands.Cog.listener()
    async def on_thread_create(self,thread):
        embed = discord.Embed(title="スレッド通知", colour=discord.Colour(0xff00), description="新しいスレッドが作成されました", timestamp=datetime.now())

        embed.set_footer(text="くろぼっと", icon_url="https://cdn.discordapp.com/attachments/733707711228674102/975786870309007471/Discord-Logo-Color.png")

        embed.add_field(name="スレッド名", value=f'[{thread.name}](https://discord.com/channels/733707710784340100733707710784340100/{thread.id})', inline=False)
        embed.add_field(name="スレッドID", value=thread.id, inline=False)
        embed.add_field(name="スレッドが作成されたチャンネル", value=thread.parent, inline=True)
        embed.add_field(name="スレッド作成者", value=thread.owner.mention, inline=True)

        await self.noticech.send(content=self.noticerole.mention, embed=embed)
        print(f'スレッド作成:{thread.name}')

    @commands.Cog.listener()
    async def on_thread_update(self, before, after):
        if before.archived is False and after.archived is True:
            embed = discord.Embed(title="スレッド通知", colour=0x00ff00, description="スレッドがアーカイブされました", timestamp=datetime.now())

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
