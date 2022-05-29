import discord
from discord.ext import commands
import json

class config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.is_owner()
    async def config(self, ctx, mode = None, configname = None, argument = None):
        if mode == 'list':
            config = json.dumps(self.bot.config)
            #ここの表示もう少しきれいにしたい
            await ctx.send(config)
        elif mode == 'set':
            if configname  is not None and argument is not None:
                #try:
                    self.bot.config[configname] = argument
                    print(f'設定変更 {configname}:{argument}')
                    await ctx.send(f'設定を変更したよ\n変更した設定: {configname}\n数値: {argument}')
                    with open('config.json', 'r+', encoding='utf-8') as file:
                        json.dump(self.bot.config, file, indent=4)
                        try:
                            #ここエラー吐くから今度直してよ
                            self.bot.config = json.load(file)
                        except:
                            pass
                    print('Config reloaded')
                #except:
                #    await ctx.send('設定が変更できなかったよ\n引数を見直してみてね')
            else:
                await ctx.send('引数がおかしいよ\n設定を変更するconfigの名前と数値をいれてね')
        elif mode == 'reload':
            with open('config.json', 'r+', encoding='utf-8') as file:
                self.bot.config = json.load(file)
            print('Config reloaded')
            await ctx.send('configを再読み込みしたよ')
        else:
            await ctx.send('モードがおかしいよ\n`list`か`read`、それか`reload`で指定してね')
        

async def setup(bot):
    await bot.add_cog(config(bot))
