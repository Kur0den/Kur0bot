import discord
from discord.ext import commands
import add_socket_response_event

bot = commands.Bot(command_prefix="c/")

bot.load_extension("cog.test")

bot = commands.Bot(
    commands.when_mentioned_or('k/'),
    case_insensitive=True,
    activity = discord.Activity(name = 'くろでんのくろでんによるくろでんのためのぼっと', type = discord.ActivityType.playing),
    intents=discord.Intents.all())
token = os.environ['DISCORD_BOT_TOKEN']
guild = None
guild_id = [733707710784340100]



