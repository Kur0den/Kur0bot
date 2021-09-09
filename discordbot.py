from discord.ext import commands
import discord
import os
import traceback

bot = commands.Bot(command_prefix='k/', intents=discord.Intents.all())
token = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client(intents = discord.Intents.all())

# 起動メッセージ
@bot.event
async def on_ready():
    user = client.get_user(699414261075804201)
    print(f'ready: {client.user} (ID: {client.user.id})')
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
    channel = client.get_channel(734540948024852491)
    await channel.sepvnd('でーん')

bot.run(token)
