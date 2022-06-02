import random

import aiohttp
import discord
from discord.ext import commands
from discord.ext.tasks import loop


class stagemoney(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stage_check.start()
        self.stage_check = False
    
    # ステージやってるか検知
    @commands.Cog.listener()
    async def on_stage_instance_create(self,stage_instance):
        if stage_instance.channel == self.bot.stage:
            print('イベント開始')
            self.stage_check = True
    
    @commands.Cog.listener()
    async def on_stage_instance_delete(self,stage_instance):
        if stage_instance.channel == self.bot.stage:
            print('イベント終了')
            self.stage_check = False
    
    @loop(minutes=10.0)
    async def stage_check(self):
        #configロード
        stage_money_min = int(self.bot.config['stage_money_min'])
        stage_money_max = int(self.bot.config['stage_money_max'])
        print(f'講堂チェック')
        #ステージやってるか判定(放置対策)
        if self.stage_check == True:
            for member in self.bot.stage.members:
                #Botじゃないかどうか判別
                if member.bot is False:
                    #報酬ランダム化
                    money = random.randint(stage_money_min, stage_money_max)
                    async with aiohttp.ClientSession(headers=self.bot.ub_header) as session:
                            await session.patch(url=f'{self.bot.ub_url}{member.id}', json={'cash':money, 'reason': f'ステージチャンネル報酬'})
                            


    
    

        

async def setup(bot):
    await bot.add_cog(stagemoney(bot))
