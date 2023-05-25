import discord
from discord.ext import commands
from discord import app_commands

import random
from datetime import datetime
import json
import aiohttp

class lb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    group = app_commands.Group(name="login", description="ログインボーナス", guild_ids=[733707710784340100, 1033496363897475163], guild_only=True)
    
    @group.command(name="get", description="ログインボーナスをゲットします")
    async def lb_get(self, interaction: discord.Interaction):
        lb_list = self.bot.get_channel(1111211644123627520).history(after=datetime.today())
        login_bounus_min = int(self.bot.config['login_bounus_min'])
        login_bounus_max = int(self.bot.config['login_bounus_max'])
        lb_db = await self.bot.lb_data.find_one({
            "user_id": interaction.user.id
        }, {
            "_id": None
        })
        async for msg in lb_list:
            if interaction.user.id in msg.content:
                await interaction.response.send_message("すでにログインしてあります。また明日やってね", ephemeral=True)
            else:
                money = random.randint(login_bounus_min, login_bounus_max)
                async with aiohttp.ClientSession(headers=self.bot.ub_header) as session:
                            await session.patch(url=f'{self.bot.ub_url}{interaction.user.id}', json={'cash': money, 'reason': f'ログインボーナス'})
                if lb_db is None:
                    all_date = 1
                    await self.bot.lb_data.replace_one({
                        "user_id": interaction.user.id
                    },{
                        "user_id": interaction.user.id,
                        "all_date": all_date
                    }, upsert=True)
                else:
                    all_date = int(lb_db["all_date"]+1)
                    await self.bot.lb_data.replace_one({
                        "user_id": interaction.user.id
                    }, {
                        "user_id": interaction.user.id,
                        "all_date": all_date
                    })
                await self.bot.get_channel(1111211644123627520).send(interaction.user.id)
                await interaction.response.send_message(f"ログインしました！\n今日の報酬:{money}\n総合ログイン回数:{all_date}")
                
async def setup(bot):
    await bot.add_cog(lb(bot))