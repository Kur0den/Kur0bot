import discord
from discord.ext import commands


class threadnotice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_create(self,thread):
        thnotice = self.bot.get_channel(975618002953318420)
        await thnotice.send(f'スレッドが作成されたよ！\nスレッド名: {thread.name}\nスレッドID: {thread.id}\nスレッドが作成されたチャンネル: {thread.parent}')


def setup(bot):
    bot.add_cog(threadnotice(bot))
