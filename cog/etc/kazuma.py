import discord
from discord.ext import commands


class kazuma(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(message):
        if bool(self.bot.config['kazuma_kill_switch']) == True:
            if message.author.id == 705264675138568192:
                embed = discord.Embed(title="おいkazuma勉強しろや　ばーかばーか", color=0xff0000)
                try:
                    await message.author.timeout(discord.utils.utcnow() + datetime.timedelta(minutes=30))
                    embed.add_field(name="kazumaがdiscordをしているためタイムアウトしました。",inline=False)
                    await message.channel.send(embed=embed, delete_after=10)
                except Exception as e:
                    print(e)
                    embed.add_field(name="kazumaよ勉強しろ",value="がんばれよ。discordやめるんだ。",inline=False)
                    await message.channel.send(embed=embed, delete_after=10)

async def setup(bot):
    await bot.add_cog(kazuma(bot))
