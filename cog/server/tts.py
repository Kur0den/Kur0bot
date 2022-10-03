import asyncio
from collections import deque
from tempfile import TemporaryFile

import discord
from discord import app_commands
from discord.ext import commands, tasks
from gtts import gTTS


class tts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    group = app_commands.Group(name="tts", description="Text To Speech", guild_ids=[733707710784340100], guild_only=True)

    @group.command(name='connect', description='VCに接続します')
    @app_commands.guild_only()
    async def join(self, interaction: discord.Interaction):
        if self.bot.guild.voice_client == None:
            if interaction.channel.type is discord.ChannelType.voice:
                channel = interaction.user.voice.channel
                await interaction.response.send_message('接続しました')
                await channel.connect()
                return
        await interaction.response.send_message('接続に失敗しました\nこのコマンドは接続しているVCの聞き専チャンネルで使用してください')


    @group.command(name='disconnect', description='VCから切断します')
    @app_commands.guild_only()
    async def leave(self, interaction: discord.Interaction):
        if self.bot.guild.voice_client != None:
            if (interaction.channel and interaction.user.voice.channel) is self.bot.guild.voice_client.channel:
                await self.bot.guild.voice_client.disconnect(force=True)
                await interaction.response.send_message('切断しました')
                return
        await interaction.response.send_message('失敗しました')

    # メッセージ取得
    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.guild.voice_client != None:
            if message.author.bot is False:
                message_queue = deque([])
                usernick = message.author.display_name
                message = message.content[5:]
                message = usernick + ":" + message
                try:
                    if not self.bot.guild.voice_client.is_playing():
                        tts = gTTS(message)
                        f = TemporaryFile()
                        tts.write_to_fp(f)
                        f.seek(0)
                        self.bot.guild.voice_client.play(discord.FFmpegPCMAudio(f, pipe=True))
                    else:
                        message_queue.append(message)
                        while self.bot.guild.voice_client.is_playing():
                            await asyncio.sleep(0.1)
                        tts = gTTS(message_queue.popleft())
                        f = TemporaryFile()
                        tts.write_to_fp(f)
                        f.seek(0)
                        self.bot.guild.voice_client.play(discord.FFmpegPCMAudio(f, pipe=True))
                except(TypeError, AttributeError):
                    try:
                        tts = gTTS(message)
                        f = TemporaryFile()
                        tts.write_to_fp(f)
                        f.seek(0)
                        channel = message.author.voice.channel
                        self.bot.guild.voice_client = await channel.connect()
                        self.bot.guild.voice_client.play(discord.FFmpegPCMAudio(f, pipe=True))
                    except(AttributeError, TypeError):
                        await message.channel.send("I'm not in a voice channel and neither are you!")
                    return
    
    def play(server):
        player = playlist[server.id]
        if player[0][0].is_done():     # 再生が終わったら
            player[0][0].stop()        # 一応再生停止
            os.remove(player[0][1])    # 音声ファイル削除
            player.pop(0)              # リストの0個目を削除
            if 0 < len(player):        # 次再生すべき物があるか
                player[0][0].start()   # 次のを再生
    
    


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(tts(bot))
