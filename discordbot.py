import discord
from discord.ext import commands
import os
import cog
import asyncio
from pathlib import Path
from os import sep as ossep
import traceback
from datetime import datetime
from dotenv import load_dotenv 
# import add_socket_response_event

load_dotenv()

token = os.environ['DISCORD_BOT_TOKEN']
bot = commands.Bot(
    commands.when_mentioned_or('k!'),
    case_insensitive=True,
    activity = discord.Activity(name = 'くろでんのくろでんによるくろでんのためのぼっと', type = discord.ActivityType.playing),
    intents=discord.Intents.all(),
    )

guild_id = [733707710784340100]


@bot.event
async def on_ready():
    global guild, unei_members, osirase_ch, osirase_role
    bot.guild = bot.get_guild(733707710784340100)
    bot.owner = bot.get_user(699414261075804201)
    unei_role = bot.guild.get_role(738956776258535575)
    unei_members = unei_role.members
    osirase_ch = bot.get_channel(734605726491607091)
    osirase_role = bot.guild.get_role(738954587922235422)
    login_ch = bot.get_channel(888416525579612230)
    for file in os.listdir('./cog'):
        if file.endswith('.py'):
            try:
                await bot.load_extension(f'cog.{file[:-3]}')
                print(f'Loaded cog: {file[:-3]}')
            except:
                traceback.print_exc()
    print('cog loaded')
    print(f'ready: {bot.user} (ID: {bot.user.id})')
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