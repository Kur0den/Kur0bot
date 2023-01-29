import os
import shutil
import traceback
from datetime import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv
from motor import motor_asyncio as motor

# 環境変数(.env)をロード
load_dotenv()

token = os.environ['DISCORD_BOT_TOKEN']
bot = commands.Bot(
    command_prefix='t/',
    case_insensitive=True,
    activity=discord.Activity(
        name='誰が使うのこのTTSBot', type=discord.ActivityType.playing),
    intents=discord.Intents.all(),
)

guild_id = 733707710784340100


@bot.event
async def on_ready():
    global osirase_ch, osirase_role
    bot.guild = bot.get_guild(733707710784340100)
    bot.owner = bot.get_user(699414261075804201)

    # VC機能系定義
    bot.tts_file = '.tts_voice'
    try:
        shutil.rmtree(bot.tts_file)
    except:
        pass
    os.mkdir(bot.tts_file)

    # DataBase
    bot.dbclient = motor.AsyncIOMotorClient('mongodb://localhost:27017')
    bot.db = bot.dbclient["TTSBot"]
    bot.vc_info = bot.db.vc_info
    bot.kur0db = bot.dbclient["Kur0Bot"]
    bot.kur0vc_info = bot.db.vc_info

    # cogをロード
    for file in os.listdir('./cog'):
        if file.endswith('.py'):
            try:
                await bot.load_extension(f'cog.{file[:-3]}')
                print(f'Loaded cog: {file[:-3]}')
            except:
                traceback.print_exc()
    try:
        await bot.load_extension('jishaku')
        print('Loaded cog: jishaku')
    except:
        traceback.print_exc()
    print('cog loaded')
    ttsinfo = await bot.vc_info.find_one({
        "tts": True
    }, {
        "_id": False  # 内部IDを取得しないように
    })
    radioinfo = await bot.vc_info.find_one({
        "tts": True
    }, {
        "_id": False  # 内部IDを取得しないように
    })
    if ttsinfo is not None:
        channel = bot.guild.get_channel(ttsinfo['channel_id'])
        await channel.connect()
        await channel.send('再接続しました')
    elif radioinfo is not None:
        channel = bot.guild.get_channel(ttsinfo['channel_id'])
        await channel.connect()
        bot.guild.voice_client.play(
            discord.FFmpegPCMAudio(radioinfo['radioURL']))
        await channel.send('再接続しました')
    print(f'ready: {bot.user} (ID: {bot.user.id})')
    await bot.owner.send(f'きどうしたよ！！！！！！！ほめて！！！！！！！！\n起動時刻: {datetime.now()}')


# エラー表示
@bot.event
async def on_command_error(ctx, error):
    error_ch = bot.get_channel(1002616704603525151)
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(
        traceback.TracebackException.from_exception(orig_error).format())
    embed = discord.Embed(title="<:guard_ng:748539994557120614> Error!", description='エラーが発生しました',
                          timestamp=ctx.message.created_at, color=discord.Colour.red())
    embed.add_field(
        name='メッセージID', value=f'お問い合わせの際にはこちらのidもお持ちください:\n`{ctx.message.id}`')
    embed.add_field(name='エラー内容', value=error, inline=False)
    embed.set_footer(text="お困りの場合はBot管理者までお問い合わせください")
    await ctx.send(embed=embed)
    embed2 = discord.Embed(title='エラー情報', description='',
                           timestamp=ctx.message.created_at, color=discord.Colour.red())
    embed2.add_field(name='サーバー', value=ctx.message.guild.name, inline=False)
    embed2.add_field(
        name='チャンネル', value=ctx.message.channel.name, inline=False)
    embed2.add_field(name='コマンド', value=ctx.message.content, inline=False)
    embed2.add_field(name='実行ユーザー名', value=ctx.author, inline=False)
    embed2.add_field(name='id', value=ctx.message.id, inline=False)
    embed2.add_field(name='内容', value=error, inline=False)
    await error_ch.send(embed=embed2)

bot.run(token)
