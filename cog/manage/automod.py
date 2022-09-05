import discord
from discord.ext import commands
import asyncio


class automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener(name='on_automod_action')
    async def automod_notice(self,execution):
        channel = self.bot.get_channel(987240589949034547)
        if execution.action.type == discord.AutoModRuleActionType.send_alert_message:
            await channel.send(self.bot.unei_role.mention)
    

async def setup(bot):
    await bot.add_cog(automod(bot))
