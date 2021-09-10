from discord.ext import commands
import discord
import os
import traceback
import datetime
import subprocess
from subprocess import PIPE

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
    if thread.message_count == 1:# and thread.member_count == 2:
        ctx.send('てすとだよ')
    await thread.send('くろぼっとが参加したよ！')
    thnotice = bot.get_channel(733707711228674102)
    await thnotice.send('でーん')

# evalもどき
@bot.command()
@commands.is_owner()
async def test(ctx, im):
    proc = subprocess.Popen(im, shell=True, stdout=PIPE, stderr=PIPE, text=True)

    ex = proc.communicate(timeout=10)
    await ctx.send(f'{ex}\nだよ')

# 時間表示
@bot.command()
async def time(ctx, sub = None):
    jst_date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y/%m/%d")
    jst_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%H:%M:%S")
    est_date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5))).strftime("%Y/%m/%d")
    est_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5))).strftime("%H:%M:%S")
    utc_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y/%m/%d")
    utc_time = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")
    if sub == 'date':
        embed = discord.Embed(title='📅Date', description=f'UTC `{utc_date}`\nJST `{jst_date}`\nEST `{est_date}`')
        await ctx.send(embed=embed)
    elif sub == 'time':
        embed = discord.Embed(title='⏲Time', description=f'UTC `{utc_time}`\nJST `{jst_time}`\nEST `{est_time}`')
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='📅Date&Time⏲', description=f'UTC `{utc_date} {utc_time}`\nJST `{jst_date} {jst_time}`\nEST `{est_date} {est_time}`')
        await ctx.send(embed=embed)
    




bot.run(token)
