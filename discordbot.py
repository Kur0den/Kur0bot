import discord
from discord.ext import commands
import os
import cog
import asyncio
from pathlib import Path
import traceback
from datetime import datetime
from dotenv import load_dotenv
from bot import MyBot
# import add_socket_response_event

load_dotenv()

bot = MyBot(
    commands.when_mentioned_or('k/'),
    case_insensitive=True,
    activity = discord.Activity(name = 'くろでんのくろでんによるくろでんのためのぼっと', type = discord.ActivityType.playing),
    intents=discord.Intents.all())
token = os.environ['DISCORD_BOT_TOKEN']
guild_id = [733707710784340100]


@bot.event
async def on_ready():
    global unei_members, osirase_ch, osirase_role
    bot.guild = bot.get_guild(733707710784340100)
    bot.owner = bot.get_user(699414261075804201)
    unei_role = bot.guild.get_role(738956776258535575)
    unei_members = unei_role.members
    osirase_ch = bot.get_channel(734605726491607091)
    osirase_role = bot.guild.get_role(738954587922235422)
    login_ch = bot.get_channel(888416525579612230)
    # cogload

    await bot.owner.send(f'きどうしたよ！！！！！！！ほめて！！！！！！！！\n起動時刻: {datetime.now()}')


#    DiscordComponents(bot)



# エラー表示
@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg  = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    embed = discord.Embed(title = 'Error', description = error_msg)
    await ctx.send(error_msg)

bot.run(token)