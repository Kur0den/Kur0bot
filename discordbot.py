import discord
from discord.ext import commands
import os
import cog
import asyncio
from pathlib import Path
from os import sep as ossep
import traceback
from dotenv import load_dotenv
from json import load
from discord.ext.tasks import loop
# import add_socket_response_event


#環境変数をロード
load_dotenv()


bot = commands.Bot(
    commands.when_mentioned_or('k!'),
    case_insensitive=True,
    activity = discord.Activity(name = 'くろでんのくろでんによるくろでんのためのぼっと', type = discord.ActivityType.playing),
    intents=discord.Intents.all())

#トークン定義
token = os.environ['DISCORD_BOT_TOKEN']
guild = None
guild_id = [733707710784340100]







@bot.event
async def on_ready():
    global guild, unei_members, osirase_ch, osirase_role
    bot.guild = bot.get_guild(733707710784340100)
    bot.owner = bot.get_user(699414261075804201)
    bot.unei_role = bot.guild.get_role(738956776258535575)
    bot.unei_members = bot.unei_role.members
    bot.stage =bot.get_channel(884734698759266324)
    osirase_ch = bot.get_channel(734605726491607091)
    osirase_role = bot.guild.get_role(738954587922235422)
    login_ch = bot.get_channel(888416525579612230)
    
    #UnbelievaBoatのAPI系のやつを定義
    UB_API_TOKEN = os.environ.get('UNB_TOKEN')
    bot.ub_url = 'https://unbelievaboat.com/api/v1/guilds/733707710784340100/users/'
    bot.ub_header = {'Authorization': UB_API_TOKEN, 'Accept': 'application/json'}
    
    #config.jsonをロード
    try:
        with open('config.json', 'r+', encoding='utf-8') as file:
            bot.config = load(file)
        print('Config loaded')
    except:
        traceback.print_exc()
        print('Config not loaded')
    #welcomeフォルダ内のcogをロード
    for file in os.listdir('./cog/welcome'):
        if file.endswith('.py'):
            try:
                await bot.load_extension(f'cog.welcome.{file[:-3]}')
                print(f'Loaded cog: welcome.{file[:-3]}')
            except:
                traceback.print_exc()
    # moneyフォルダ内のcogをロード
    for file in os.listdir('./cog/money'):
        if file.endswith('.py'):
            try:
                await bot.load_extension(f'cog.money.{file[:-3]}')
                print(f'Loaded cog: money.{file[:-3]}')
            except:
                traceback.print_exc()
    # manageフォルダ内のcogをロード
    for file in os.listdir('./cog/manage'):
        if file.endswith('.py'):
            try:
                await bot.load_extension(f'cog.manage.{file[:-3]}')
                print(f'Loaded cog: manage.{file[:-3]}')
            except:
                traceback.print_exc()
    try:
        await bot.load_extension('jishaku')
        print('Loaded cog: jishaku')
    except:
        traceback.print_exc()
    print('cog loaded')

    user = bot.get_user(699414261075804201)
    print(f'ready: {bot.user} (ID: {bot.user.id})')
    await user.send('きどうしたよ！！！！！！！ほめて！！！！！！！！')
#    DiscordComponents(bot)

# エラー表示
@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg  = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    embed = discord.Embed(title = 'Error', description = error_msg)
    await ctx.send(error_msg)

bot.run(token)
