from discord.ext import commands
import discord
import os
import traceback
import datetime

bot = commands.Bot(command_prefix='k/', intents=discord.Intents.all())
token = os.environ['DISCORD_BOT_TOKEN']





# 起動メッセージ
@bot.event
async def on_ready():
    user = bot.get_user(699414261075804201)
    print(f'ready: {bot.user} (ID: {bot.user.id})')
    await user.send('きどうしたよ！！！！！！！ほめて！！！！！！！！')

# エラー表示するやつ
@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

# Pingコマンド
@bot.command()
async def ping(ctx):
    pong = ':ping_pong:'
    embed = discord.Embed(title=f'{pong}Pong!', description=f'{round(bot.latency * 1000)}ms')
    await ctx.send(embed=embed)

# スレッド通知
@bot.event
async def on_thread_join(thread):
    await thread.send('くろぼっとが参加したよ！')
    thnotice = bot.get_channel(733707711228674102)
    await thnotice.send('でーん')

# evalもどき
@bot.command()
@commands.is_owner()
async def test(ctx, im):
    ex = eval(im)
    await ctx.send(f'{ex}\nだよ')
    
# 時間表示
@bot.command()
async def time(ctx, sub = None):
    await ctx.send('test')
    jst_date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y/%m/%d")
    jst_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%H:%M:%S")
    utc_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y/%m/%d")
    utc_time = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")
    if sub == 'date':
        await ctx.send(f'UTC `{utc_date}`\nJST `{jst_date}`')
    elif sub == 'time':
        await ctx.send(f'UTC `{utc_time}`\nJST `{jst_time}`')
    else:
        await ctx.send(f'UTC `{utc_date} {utc_time}`\nJST `{jst_date}{jst_time}`')
    




bot.run(token)
