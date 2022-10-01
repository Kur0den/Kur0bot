import os

import discord
from discord import app_commands
from discord.ext import commands
from gtts import gTTS
from langdetect import detect
import uuid



class tts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vc_client = None

    group = app_commands.Group(name="tts", description="Text To Speech", guild_ids=[733707710784340100], guild_only=True)

    @group.command(name='connect', description='VCに接続します')
    @app_commands.guild_only()
    async def join(self, interaction: discord.Interaction):
        if interaction.channel is (self.bot.vc1 or saelf.bot.vc2 or self.bot.vc3):
            if self.bot.voice_clients == []:
                if interaction.user.voice.channel is interaction.channel:
                    self.vc_client = await interaction.channel.connect()
                    await interaction.response.send_message('接続しました')
                    return
        await interaction.response.send_message('接続に失敗しました\nこのコマンドは接続しているVCの聞き専チャンネルで使用してください')


    @group.command(name='disconnect', description='VCから切断します')
    @app_commands.guild_only()
    async def leave(self, interaction: discord.Interaction):
        if self.vc_client != None:
            if interaction.channel is self.vc_client.channel:
                if interaction.user.voice.channel is self.vc_client.channel:
                    await self.vc_client.disconnect()
                    self.vc = None
                    await interaction.response.send_message('切断しました')
                    return
        await interaction.response.send_message('失敗しました')




    # メッセージ取得
    @commands.Cog.listener()
    async def on_message(self, message):
        if self.vc_client != None:
            if message.author.bot is False:
                if message.channel is self.vc_client.channel:
                    tts = gTTS(text=message.content, lang=detect(message.content), tld='jp')
                    name = uuid.uuid1()
                    tts.save(f'tts/{name}.mp3')
                    self.vc_client.play(f'{name}.wav')
                    os.remove(f'tts/{name}.mp3')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(tts(bot))
