import discord
from discord.ext import commands
from datetime import datetime

class botrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self,member):
        if member.guild == self.bot.guild:
            if member.bot is True:
                botrole = self.bot.guild.get_role(734059242977230969)
                await member.add_roles(botrole)

                embed = discord.Embed(title="新規Bot追加", colour=discord.Colour(0xb22222), description="新しいBotが追加されたよ", timestamp=datetime.now())

                embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
                embed.set_footer(text="くろぼっと", icon_url="https://cdn.discordapp.com/attachments/733707711228674102/975786870309007471/Discord-Logo-Color.png")

                await self.bot.guild.system_channel.send(embed = embed)

async def setup(bot):
    await bot.add_cog(botrole(bot))
