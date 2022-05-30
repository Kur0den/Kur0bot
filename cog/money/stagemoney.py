import discord
from discord.ext import commands
from discord.ext.tasks import loop


class stagemoney(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @loop(seconds=60)
    async def stage_check(self):
        #configロード
        stage_money_min = self.bot.config['stage_money_min']
        stage_money_max = self.bot.config['stage_money_max']
        print('講堂チェック')
        #ステージやってるか判定(放置対策)
        if self.bot.stage.topic is not None:
            for member in self.bot.stage.members:
                #Botじゃないかどうか判別
                if member.bot is False:
                    #報酬ランダム化
                    money = random.randint(stage_money_min, stage_money_max)
                    async with aiohttp.ClientSession(headers=self.bot.ub_header) as session:
                            await session.patch(url=f'{self.bot.ub_url}{member.id}', json={'cash':money, 'reason': f'ステージチャンネル報酬'})

async def setup(bot):
    await bot.add_cog(stagemoney(bot))
