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
    if len(await thread.history(limit=2).flatten()) == 0:
        await thread.send(f'くろぼっとが参加したよ！')
        thnotice = bot.get_channel(733707711228674102)
        await thnotice.send('スレッドが作成されたよ！')
# evalもどき
@bot.command(hidden = True)
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
        embed = discord.Embed(title='📅Date', description=f'UTC `{utc_date}`\n\nJST `{jst_date}`\n\nEST `{est_date}`')
        await ctx.send(embed=embed)
    elif sub == 'time':
        embed = discord.Embed(title='⏲Time', description=f'UTC `{utc_time}`\n\nJST `{jst_time}`\n\nEST `{est_time}`')
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='📅Date&Time⏲', description=f'UTC `{utc_date} {utc_time}`\n\nJST `{jst_date} {jst_time}`\n\nEST `{est_date} {est_time}`')
        await ctx.send(embed=embed)


@bot.command()
async def idinfo(ctx, imid):
    try:
        iid = bot.fetch_channel(imid)
        ty = ('チャンネル又はスレッドID')
    except:
        iid = bot.fetch_sticker(imid)
        ty = ('ステッカーID')
    except:
        iid = bot.fetch_user(imid)
        ty = ('ユーザーID')
    except:
        iid == bot.fetch_guild(imid)
        ty = ('サーバーID')
    except:
        ty = ('Not found')
    try:
        ex_name = iid.name
    except:
        ex_name = ('None')
    await ctx.send(ex_name)




bot.run(token)
