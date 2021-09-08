from discord.ext import commands
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
    embed = discord.Embed(title=f':ping_pong:Pong!',description=f'{round(bot.latency * 1000)}ms',color='#006400')
    await ctx.send(embed=embed)


bot.run(token)
