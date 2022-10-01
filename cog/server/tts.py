import os

import discord
from discord import app_commands
from discord.ext import commands
from gtts import gTTS



class tts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vc = None

    group = app_commands.Group(name="tts", description="Text To Speech", guild_ids=[733707710784340100], guild_only=True)

    @group.command(name='connect', description='VCに接続します')
    @app_commands.guild_only()
    async def join(self, interaction: discord.Interaction):
        if interaction.channel is (self.bot.vc1 or saelf.bot.vc2 or self.bot.vc3):
            if self.bot.voice_clients == []:
                if interaction.user.voice.channel is interaction.channel:
                    self.vc = await interaction.channel.connect()
                    await interaction.response.send_message('接続しました')
                    return
        await interaction.response.send_message('接続に失敗しました\nこのコマンドは接続しているVCの聞き専チャンネルで使用してください')


    @group.command(name='disconnect', description='VCから切断します')
    @app_commands.guild_only()
    async def leave(self, interaction: discord.Interaction):
        if self.vc != None:
            if interaction.channel is self.vc.channel:
                if interaction.user.voice.channel is self.vc.channel:
                    await self.vc.disconnect()
                    self.vc = None
                    await interaction.response.send_message('切断しました')
                    return
        await interaction.response.send_message('失敗しました')




    # メッセージ取得
    @commands.Cog.listener()
    async def on_message(self, message):
        if self.vc != None:
            if message.author.bot is False:
                if message.channel is self.vc.channel:
                    await message.channel.send('じゃーん')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(tts(bot))
