import discord
from discord.ext import commands
from datetime import datetime

class thnotice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.Cog.listener()
    async def on_thread_create(self,thread):
        noticech = self.bot.get_channel(975618002953318420)
        noticerole = self.bot.guild.get_role(956128433660899358)
#        await thnotice.send(f'スレッドが作成されたよ！\nスレッド名: {thread.name}\nスレッドID: {thread.id}\nスレッドが作成されたチャンネル: {thread.parent}')
        embed = discord.Embed(title="スレッド通知", colour=discord.Colour(0xff00), url=f"https://discord.com/channels/733707710784340100733707710784340100/{thread.id}", description="新しいスレッドが作成されました", timestamp=datetime.utcnow())

        embed.set_footer(text="くろぼっと", icon_url="https://cdn.discordapp.com/attachments/733707711228674102/975786870309007471/Discord-Logo-Color.png")

        embed.add_field(name="スレッド名", value=thread.name, inline=True)
        embed.add_field(name="スレッドID", value=thread.id, inline=True)
        embed.add_field(name="スレッドが作成されたチャンネル", value=thread.parent, inline=True)
        embed.add_field(name="スレッド作成者", value=thread.owner.mention, inline=True)

        await noticech.send(content=noticerole.mention, embed=embed)

    @commands.Cog.listener()
    async def on_thread_update(self, before, after):
        
        await self.bot.owner.send(before)
        await self.bot.owner.send(after)
    
    @commands.Cog.listener()
    async def on_thread_remove():
        await self.bot.owner.send(thread)

async def setup(bot):
    await bot.add_cog(thnotice(bot))
