from datetime import datetime

import discord
from discord.ext import commands, tasks


class timesignal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timesignal.start()
        self.message = None
        self.embed = None
    
    

    @tasks.loop(minutes=1)
    async def timesignal(self):
        now = datetime.now().strftime('%H')
        if datetime.now().strftime('%M') == '00':
            
            self.embed = discord.Embed(title='時報', colour=discord.Colour(0x4b78e6), description=f'{now}時ちょうどをお知らせします')

            self.embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/733707711228674102/986178408696393768/spin.gif')
            
            if now =='00':
                self.embed.add_field(name = 'あけおめ！！！！！！！',value=f'今日は{datetime.now().strftime("%m月%d日")}だよ！！！！！！')
            elif now == '12':
                self.embed.add_field(name = 'おひるだ！！！！！！！',value=f'ご飯を食べよう！！！！！！！！！')
            elif now == '15':
                self.embed.add_field(name = 'おやつ！！！！！！！',value=f'おやつ！！！！！！！！！')
            elif now == '23':
                    self.embed.add_field(name = 'よるだぞ！！！！！！！',value=f'そろそろ寝よう！！！！！！！！！')
            print(f'時報({now}時)')
            
        elif datetime.now().strftime('%M') == '30':
                self.embed = discord.Embed(title='時報', colour=discord.Colour(0x4b78e6), description=f'{now}時30分をお知らせします')

                self.embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/733707711228674102/986178408696393768/spin.gif')
                
                print(f'時報({now}時半)')
        
        if self.embed != None:
            if self.message != None:
                await self.message.delete()
            self.message = await self.bot.guild.system_channel.send(embed=self.embed)
            self.embed = None

    async def cog_unload(self):
            self.timesignal.stop()


async def setup(bot):
    await bot.add_cog(timesignal(bot))
