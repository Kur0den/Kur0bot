from discord.ext import commands
import discord
import os
import traceback
import datetime
import subprocess
from subprocess import PIPE
from discord_slash import SlashCommand, SlashContext
import add_socket_response_event
from discord_components import DiscordComponents, ComponentsBot, Button
import asyncio
import time


bot = commands.Bot(
    commands.when_mentioned_or('k/'),
    case_insensitive=True,
    activity = discord.Activity(name = 'くろでんのくろでんによるくろでんのためのぼっと', type = discord.ActivityType.playing),
    intents=discord.Intents.all())
token = os.environ['DISCORD_BOT_TOKEN']
slash = SlashCommand(bot, sync_commands = True)
guild = None
guild_id = [733707710784340100]
login_channel = None
unei_members = None
osirase_ch = None
osirase_role = None



# 起動メッセージ
@bot.event
async def on_ready():
    global guild, unei_members, osirase_ch, osirase_role
    user = bot.get_user(699414261075804201)
    print(f'ready: {bot.user} (ID: {bot.user.id})')
    await user.send('きどうしたよ！！！！！！！ほめて！！！！！！！！')
    guild = bot.get_guild(733707710784340100)
    unei_role = guild.get_role(738956776258535575)
    unei_members = unei_role.members
    osirase_ch = bot.get_channel(734605726491607091)
    osirase_role = guild.get_role(738954587922235422)
    login_channel = bot.get_channel(888416525579612230)
    DiscordComponents(bot)


# エラー表示するやつ
@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg  = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


#ログインボード送信
@bot.command(hidden =True)
async def loginboard(ctx):
    embed = discord.Embed(title='📆ログインボード',description='毎日ログインしてログインボーナスをゲット！(小並感')
    await ctx.send(
    embed = embed,
	components=[
            Button(style=1, label="ぼたん", custom_id = "login")
        ],
    )
    interaction = await bot.wait_for("button_click", check = lambda i: i.custom_id == "login")
    await interaction.send(content = "Button clicked!")





# Pingコマンド
@bot.command()
async def ping(ctx):
    pong = ':ping_pong:'
    embed = discord.Embed(title=f'{pong}Pong!', description=f'{round(bot.latency * 1000)}ms')
    await ctx.send(embed=embed)

# スレッド通知
@bot.event
async def on_thread_join(thread):
    
    if len(await thread.history(limit=2).flatten()) == 0 or 1:
        sent = await thread.send(content = f'くろぼっとが参加したよ！\nこのスレッド作成されたことを通知するには1分以内に下のボタンを押してね！',
            components=[
                Button(style=3,label='通知する',custom_id = 'tuuti',emoji = '🔔')
                ],
            )
        if thread.last_ssage_id.author.id == 875961973597171722:
            await sent.delete()
        try:
            interaction = await bot.wait_for('button_click', check = lambda i: i.custom_id == 'tuuti',timeout = 60)
            thnotice = bot.get_channel(733707711228674102)
            await thnotice.send(f'スレッドが作成されたよ！\nスレッド名: {thread.name}\nスレッドID: {thread.id}\nスレッドが作成されたチャンネル: {thread.parent}')
            await sent.edit(content = 'スレッドが作成されたことを通知したよ！', components = [])
        except asyncio.TimeoutError:
            try:
                await sent.edit(content = 'タイムアウトしたよ！', components = [])
            except:
                pass

# evalもどき
@bot.command(hidden = True)
@commands.is_owner()
async def test(ctx, im):
    proc = subprocess.Popen(im, shell=True, stdout=PIPE, stderr=PIPE, text=True)

    ex = proc.communicate(timeout=10)
    await ctx.send(f'{ex}\nだよ')

# 時間表示
@bot.command(aliases = ['t'])
async def time(ctx, sub = None):
    jst_date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y/%m/%d")
    jst_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%H:%M:%S")
    est_date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5))).strftime("%Y/%m/%d")
    est_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5))).strftime("%H:%M:%S")
    tst_date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime("%Y/%m/%d")
    tst_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime("%H:%M:%S")
    utc_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y/%m/%d")
    utc_time = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")
    if sub == 'date':
        embed = discord.Embed(title='📅Date', description=f'UTC `{utc_date}`\n\nTST `{tst_date}`JST `{jst_date}`\n\nEST `{est_date}`')
        await ctx.send(embed=embed)
    elif sub == 'time':
        embed = discord.Embed(title='⏲Time', description=f'UTC `{utc_time}`\n\nTST: `{tst_time}`\n\nJST `{jst_time}`\n\nEST `{est_time}`')
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='📅Date&Time⏲', description=f'UTC `{utc_date} {utc_time}`\n\nTST: `{tst_date} {tst_time}`\n\nJST `{jst_date} {jst_time}`\n\nEST `{est_date} {est_time}`')
        await ctx.send(embed=embed)


@bot.command(aliases = ['ui','ii'])
async def idinfo(ctx, imid):
    tid = 0
    
    iid = guild.get_channel(imid)
    # ty = 'チャンネル又はスレッドID'
    if iid == None:
        iid = guild.get_role(imid)
    
    if iid == None:
        iid == bot.get_emoji(imid)
    
    if iid == None:
        iid == guild.get_thread(imid)
    
    if iid == None:
        try:
            iid = await bot.fetch_user(imid)
            # ty = 'ユーザーID'
        except discord.NotFound:
            tid = 1
    if tid == 1:
        try:
            iid = await bot.fetch_guild(imid)
            # ty = 'サーバーID'
        except:
            tid = 2
    if tid == 2:
            iid = None
    # try:
    ex_name = iid.name
    # except:
        # ex_name = 'none'
        # pass
    await ctx.send(f'{ex_name}\n{tid}')

@bot.command(hidden=True)
async def deletetest(ctx):
    sent = await ctx.send(content = 'ぺぺぺぺぺっっぺえぺぺぺぺpえ！！！！！',
        components=[
            Button(style=1,label="さくじょぼたん",custom_id = "delete")
            ],
        )
    interaction = await bot.wait_for("button_click", check = lambda i: i.custom_id == "delete")
    await sent.delete()

@slash.slash(
    name = 'ktest',
    description = 'てすとだよ',
    guild_ids = guild_id,
    options = [
        {
            "name":"hidden",
            "description":"隠すかどうか(?)",
            "type":5,
            "required":False
        }
    ]
)
async def test(ctx, hidden = False):
    if hidden == True:
        await ctx.send(content = 'ぺぺぺぺぺぺぺぺ！！！', hidden = True)
    else:
        await ctx.send(content = 'あばば')

@slash.slash(
    name = 'announce',
    description = 'アナウンスをお知らせに投稿します(運営専用)',
    guild_ids = guild_id,
    options = [
        {
            "name":"description",
            "description":"アナウンスする内容を送信してください",
            "type":3,
            "required":True
        },
        {
            "name":"title",
            "description":"タイトル(なしでも一応可)",
            "type":3,
            "required":False
        },
        {
            "name":"mention",
            "description":"一斉通知ロールに通知するかどうか",
            "type":5,
            "required":False
        }
    ]
)
async def announce(ctx, description, title = 'お知らせ', mention = False):
    if ctx.author not in unei_members:
        await ctx.send(content = 'このコマンドは運営専用です。\n運営なのに使えない方はKur0denまでお知らせ下さい。', hidden = True)
    else:
        embed = discord.Embed(title = title, description = description)
        embed.set_author(name = ctx.author)
        
        if mention == True:
            await osirase_ch.send(content = osirase_role.mention, embed = embed)
            await ctx.send(content = '多分正常に送信しました', hidden = True)
        else:
            await osirase_ch.send(embed = embed)
            await ctx.send(content = '多分正常に送信しました', hidden = True)


bot.run(token)
