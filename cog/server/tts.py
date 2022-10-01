import os
import uuid

import discord
from discord import app_commands
from discord.ext import commands, tasks
from gtts import gTTS


class tts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vc_client = None
        self.file_deleter.start()

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
                    g_tts = gTTS(text=message.content, lang='ja', tld='jp')
                    name = uuid.uuid1()
                    g_tts.save(f'./tts/{name}.mp3')
                    self.vc_client.play(discord.FFmpegPCMAudio(f"./tts/{name}.mp3"))

    @tasks.loop(seconds=60)
    async def file_deleter():
        for file in os.listdir('./tts'):
            os.remove(file)
    
    async def cog_unload(self):
            self.timesignal.stop()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(tts(bot))
