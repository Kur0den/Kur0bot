import asyncio
import os
import shutil
import uuid
from collections import deque

import discord
from discord import app_commands
from discord.ext import commands
from gtts import gTTS


class tts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.jcall = False

    group = app_commands.Group(name="tts", description="Text To Speech", guild_ids=[733707710784340100], guild_only=True)

    @group.command(name='connect', description='VCに接続します')
    @app_commands.guild_only()
    async def join(self, interaction: discord.Interaction, joinannounce: bool = False):
        if interaction.channel is self.bot.vc1 or interaction.channel is self.bot.vc2 or interaction.channel is self.bot.vc3:
            if self.bot.guild.voice_client == None:
                if interaction.user.voice.channel is interaction.channel:
                    await interaction.channel.connect()
                    await interaction.response.send_message('接続しました')
                    self.jcall = joinannounce
                    return
        await interaction.response.send_message('接続に失敗しました\nこのコマンドは接続しているVCの聞き専チャンネルで使用してください')

    @group.command(name='disconnect', description='VCから切断します')
    @app_commands.guild_only()
    async def leave(self, interaction: discord.Interaction):
        if self.bot.guild.voice_client != None:
            if interaction.channel is self.bot.guild.voice_client.channel:
                if interaction.user.voice.channel is self.bot.guild.voice_client.channel:
                    await self.bot.guild.voice_client.disconnect()
                    self.vc = None
                    await interaction.response.send_message('切断しました')
                    return
        await interaction.response.send_message('失敗しました')

    # stopコマンド
    @group.command(name='stop', description='読み上げを停止します')
    async def stop(self, interaction: discord.Interaction):
        if interaction.channel is self.bot.guild.voice_client.channel:
            try:
                self.bot.guild.voice_client.stop()
                await interaction.response.send_message('読み上げを停止しました')
            except:
                await interaction.response.send_message('なぜか実行できませんでした', ephemeral=True)
        else:
            await interaction.response.send_message('なぜか実行できませんでした', ephemeral=True)

    # メッセージ取得
    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.guild.voice_client != None:
            if message.author.bot is False:
                if message.channel is self.bot.guild.voice_client.channel:
                    message_queue = deque([])
                    i = 0
                    for m in [message async for message in message.channel.history(limit=2)]:
                        if i == 0:
                            m1 = m.author.id
                        else:
                            m2 = m.author.id
                        i = +1
                    usernick = message.author.display_name
                    message = message.content[:100]
                    if m1 == m2:
                        pass
                    else:
                        message = usernick + ":" + message
                    if not self.bot.guild.voice_client.is_playing():
                        g_tts = gTTS(text=message, lang='ja', tld='jp')
                        name = uuid.uuid1()
                        g_tts.save(f'./.tts_voice/{name}.mp3')
                        self.bot.guild.voice_client.play(discord.FFmpegPCMAudio(f"./.tts_voice/{name}.mp3"))
                    else:
                        message_queue.append(message)
                        while self.bot.guild.voice_client.is_playing():
                            await asyncio.sleep(0.1)
                        g_tts = gTTS(message_queue.popleft(), lang='ja', tld='jp')
                        name = uuid.uuid1()
                        g_tts.save(f'./.tts_voice/{name}.mp3')
                        self.bot.guild.voice_client.play(discord.FFmpegPCMAudio(f"./.tts_voice/{name}.mp3"))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # TTS実行中か判断
        if self.bot.guild.voice_client != None:
            # 入退出処理
            if member.bot is False:
                # 入退出以外は弾く
                if before.channel != after.channel:
                    if self.jcall is True:
                        # 入室
                        call_queue = deque([])
                        if after.channel is not None and after.channel != self.bot.stage:
                            message = (f'{member.name}:が入室しました')
                        # 退出
                        elif before.channel is not None and before.channel != self.bot.stage:
                            message = (f'{member.name}:が退室しました')
                        else:
                            return
                        if not self.bot.guild.voice_client.is_playing():
                            g_tts = gTTS(text=message, lang='ja', tld = 'jp')
                            name = uuid.uuid1()
                            g_tts.save(f'./.tts_voice/{name}.mp3')
                            self.bot.guild.voice_client.play(discord.FFmpegPCMAudio(f"./.tts_voice/{name}.mp3"))
                        else:
                            call_queue.append(message)
                            while self.bot.guild.voice_client.is_playing():
                                await asyncio.sleep(0.1)
                            g_tts = gTTS(call_queue.popleft(), lang='ja', tld='jp')
                            name = uuid.uuid1()
                            g_tts.save(f'./.tts_voice/{name}.mp3')
                            self.bot.guild.voice_client.play(discord.FFmpegPCMAudio(f"./.tts_voice/{name}.mp3"))
        if member.id is self.bot.user.id:
            if before.channel is not None:
                shutil.rmtree(self.bot.tts_file)
                os.mkdir(self.bot.tts_file)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(tts(bot))