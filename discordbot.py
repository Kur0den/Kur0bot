from discord.ext import commands
import discord
import os
import traceback

bot = commands.Bot(command_prefix='k/')
token = os.environ['DISCORD_BOT_TOKEN']

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
# 起動メッセージ
# ちなみに動かない()
@client.event
async def on_ready():
    user = client.get_user(699414261075804201)
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
@client.event
async def on_thread_join():
    channel = client.get_channel(734540948024852491)
    await channel.send('でーん')


bot.run(token)
