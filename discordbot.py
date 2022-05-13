import discord
from discord.ext import commands
import os
import cog
# import add_socket_response_event



bot = commands.Bot(
    commands.when_mentioned_or('k/'),
    case_insensitive=True,
    activity = discord.Activity(name = 'くろでんのくろでんによるくろでんのためのぼっと', type = discord.ActivityType.playing),
    intents=discord.Intents.all())
token = 'ODc1OTYxOTczNTk3MTcxNzIy.GLMD1j.Zz19BlU2Il-ocu7ir-QM71feSNDgglWHTCtCrE'
guild = None
guild_id = [733707710784340100]





@bot.event
async def on_ready():
    await bot.load_extension("cog.test")
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


bot.run(ODc1OTYxOTczNTk3MTcxNzIy.GLMD1j.Zz19BlU2Il-ocu7ir-QM71feSNDgglWHTCtCrE)