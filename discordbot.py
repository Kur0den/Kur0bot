from discord.ext import commands
import discord
import os
import traceback

bot = commands.Bot(command_prefix='k/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    pong = :'ping_pong:'
    embed = discord.Embed(title=f'{pong}Pong!',　description=f'{round(bot.latency * 1000)}ms',　color='006400')
    await ctx.send(embed=embed)


bot.run(token)
