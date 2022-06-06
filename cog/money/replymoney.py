import os
import random

import aiohttp
import discord
from discord.ext import commands


class replymoney(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        cooldown = int(self.bot.config['reply_money_cooldown'])
        reply_money_min = int(self.bot.config['reply_money_min'])
        reply_money_max = int(self.bot.config['reply_money_max'])
        cooldown_ch = self.bot.manageguild.get_channel(983303783721369640)
        if message.guild == self.bot.guild:
            if message.author.bot is False:
                if message.reference is not None:
                    async for msg in cooldown_ch.history():
                        if msg.content.startswith(str(message.author.id)):
                            return
                        else:
                            origin_channel = self.bot.get_channel(message.reference.channel_id)
                            origin_message = await origin_channel.fetch_message(message.reference.message_id)
                            if origin_message.author.id != message.author.id:
                                if bool(self.bot.config['reply_money_random']) is True:
                                    money = random.randint(reply_money_min, reply_money_max)
                                else:
                                    money = reply_money_max
                                async with aiohttp.ClientSession(headers=self.bot.ub_header) as session:
                                    #replyer
                                    await session.patch(url=f'{self.bot.ub_url}{message.author.id}', json={'cash': money, 'reason': f'返信報酬(送信側)'})
                                    #origin
                                    await session.patch(url=f'{self.bot.ub_url}{origin_message.author.id}', json={'cash': (money + int(self.bot.config['reply_origin_bonus'])), 'reason': f'返信報酬(受信側)'})
                                    print('replyed')
                                await cooldown_ch.send(message.author.id, delete_after=cooldown)
                            return

async def setup(bot):
    await bot.add_cog(replymoney(bot))
