import discord
from discord.ext import commands
import re


class anchor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        #Bot回避
        if message.author.bot is True: return
        # >>0を防ぐ
        r1 = re.match(r'>>0', message.content)
        print(message.content)
        print(r1)
        if r1 == None:
            # 指定部分切り抜き(とりあえず50まで検知)
            r2 = re.match(r'>>[1-9]|>>[1-4][0-9]|>>50', message.content)
            print(r2)
            if r2 != None:
                await message.channel.send('検知したよ')
        
        else:
            await message.channel.send('⚓安価は1~50の間で指定してね')
        


async def setup(bot):
    await bot.add_cog(anchor(bot))
