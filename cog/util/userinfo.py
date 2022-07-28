import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone


class userinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ui'])
    async def userinfo(self, ctx, user: discord.User = None):
        if user == None:
            user = ctx.author


        member = ctx.guild.get_member(user.id)
        if member is not None:
            user = member

        embed = discord.Embed(title=f'{user}の詳細', description='詳細だよ', color=user.color)

        embed.add_field(name='名前', value=user)
        embed.add_field(name='Botかどうか', value=user.bot)
        embed.add_field(name='ID', value=user.id)

        embed.set_thumbnail(url=user.avatar)

        jst = timezone(timedelta(hours=9))


        if member is not None:
            joined_at = member.joined_at.astimezone(jst).strftime(
                "%Y/%m/%d %H:%M:%S"
            )
            embed.add_field(name="サーバー参加日", value=joined_at, inline=False)

        created_at = user.created_at.astimezone(jst).strftime(
        "%Y/%m/%d %H:%M:%S"
        )
        embed.add_field(name="アカウント作成日", value=created_at, inline=False)

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(userinfo(bot))
