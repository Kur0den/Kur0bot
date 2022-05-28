import discord
from discord.ext import commands
from datetime import datetime
from datetime import timedelta
from dateutil import tz



class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    


    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        Member_role = self.bot.guild.get_role(734392722462605352)
        if Member_role not in before.roles and Member_role in after.roles:
            

            join_jst = after.joined_at + timedelta(hours = 9)

            embed = discord.Embed(title="新規参加", colour=discord.Colour(0xaa3cc8), description="新しいユーザーが認証を終えて参加したよ\n手厚く歓迎してあげてね", timestamp=datetime.now())

            embed.set_author(name=after.display_name, icon_url=after.display_avatar.url)
            embed.set_footer(text="くろぼっと", icon_url="https://cdn.discordapp.com/attachments/733707711228674102/975786870309007471/Discord-Logo-Color.png")
            embed.add_field(name="サーバー参加日時", value=join_jst.strftime("%Y/%m/%d, %H:%M:%S"), inline=False)

            await self.bot.guild.system_channel.send(content = self.bot.guild.get_role(739313414769213488).mention,embed = embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
