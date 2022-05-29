import discord
from discord.ext import commands
import json

class config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def config(self, ctx, mode = None, configname = None, argument = None):
        if mode == 'read':
            config = json.dumps(self.bot.config)
            await ctx.send(config)
        elif mode == 'write':
            if configname  is not None and argument is not None:
                await ctx.send('テスト成功！')
            else:
                await ctx.send('引数がおかしいよ\n設定を変更するconfigの名前と数値をいれてね')
        else:
            await ctx.send('モードがおかしいよ\n`read`か`write`で指定してね')
        

async def setup(bot):
    await bot.add_cog(config(bot))
