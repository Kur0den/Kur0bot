import asyncio
import os
import re
import shutil
import uuid
from collections import deque

import discord
from discord import app_commands
from discord.ext import commands
from gtts import gTTS

regex = r"https?://.*?( |$)"


class tts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.jcall = False

    group = app_commands.Group(name="tts", description="Text To Speech", guild_ids=[733707710784340100], guild_only=True)

    @group.command(name='connect', description='VCに接続します')
    @app_commands.guild_only()
    async def join(self, interaction: discord.Interaction, joinannounce: bool = False):
        vcinfo = await self.bot.vc_info.find_one({
            'channel_id': interaction.channel_id
        }, {
            "_id": False  # 内部IDを取得しないように
        })
        ttsinfo = await self.bot.vc_info.find_one({
            "tts": True
        }, {
            "_id": False  # 内部IDを取得しないように
        })
        radioinfo = await self.bot.vc_info.find_one({
            "radio": True
        }, {
            "_id": False  # 内部IDを取得しないように
        })
        kur0info = await self.bot.kur0vc_info.find_one({
            'channel_id': interaction.channel.id
        }, {
            "_id": False  # 内部IDを取得しないように
        })
        if vcinfo is not None:
            if ttsinfo is None and radioinfo is None:
                if interaction.user.voice.channel is interaction.channel:
                    if kur0info['tts'] is False:
                        await interaction.channel.connect()
                        await interaction.response.send_message('接続しました')
                        vcinfo = await self.bot.vc_info.find_one({
                            'channel_id': interaction.channel_id
                        }, {
                            "_id": False  # 内部IDを取得しないように
                        })
                        new_info = {
                            'channel_id': interaction.channel_id,
                            'tts': True,
                            'joincall': joinannounce,
                            'radio': False,
                            'radioURL': None
                        }
                        await self.bot.vc_info.replace_one({
                            'channel_id': interaction.channel_id
                        }, new_info, upsert=True)
                        try:
                            shutil.rmtree(self.bot.tts_file)
                            os.mkdir(self.bot.tts_file)
                        except:
                            pass
                    else:
                        await interaction.response.send_message('既に<@875961973597171722>がTTSモードとして接続されています\nラジオモードとして使用するか<@875961973597171722>をVCから切断して再度コマンドを実行してください')
                else:
                    await interaction.response.send_message('接続に失敗しました\nこのコマンドは接続しているVCの聞き専チャンネルで使用してください')
            else:
                await interaction.response.send_message('他のチャンネルですでにbotが使用されているため使用できません')
        else:
            await interaction.response.send_message('このコマンドは接続しているVCの聞き専チャンネルで使用してください')

    @group.command(name='disconnect', description='VCから切断します')
    @app_commands.guild_only()
    async def leave(self, interaction: discord.Interaction):
        if self.bot.guild.voice_client != None:
            if interaction.channel is self.bot.guild.voice_client.channel:
                if interaction.user.voice.channel is self.bot.guild.voice_client.channel:
                    await self.bot.guild.voice_client.disconnect()
                    new_info = {
                        'channel_id': interaction.channel_id,
                        'tts': False,
                        'joincall': False,
                        'radio': False,
                        'radioURL': None
                    }
                    await self.bot.vc_info.replace_one({
                        'channel_id': interaction.channel_id
                    }, new_info, upsert=True)
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
        vcinfo = await self.bot.vc_info.find_one({
            'channel_id': message.channel.id
        }, {
            "_id": False  # 内部IDを取得しないように
        })
        try:
            if vcinfo['tts'] is True:
                if message.author.bot is False:
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
                        message = re.sub(regex, "URL ", message, flags=re.MULTILINE)
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
        except TypeError:
            return

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        beforeinfo = None
        afterinfo = None
        try:
            beforeinfo = await self.bot.vc_info.find_one({
                'channel_id': before.channel.id
            }, {
                "_id": False  # 内部IDを取得しないように
            })
        except AttributeError:
            pass
        try:
            afterinfo = await self.bot.vc_info.find_one({
                'channel_id': after.channel.id
            }, {
                "_id": False  # 内部IDを取得しないように
            })
        except AttributeError:
            pass

        # Botは弾く
        if member.bot is False:
            # 入退出以外は弾く
            if before.channel != after.channel:
                a = 0
                b = 0
                # TTS実行中か判断&入退出判断
                # 退出
                try:
                    if beforeinfo['joincall'] is True:
                        call_queue = deque([])
                        if afterinfo is not None:
                            message = (f'{member.name}:が移動しました')
                        else:
                            message = (f'{member.name}:が退室しました')
                    else:
                        b = 1
                except TypeError:
                    b = 1
                    pass
                #入室
                try:
                    call_queue = deque([])
                    if afterinfo['joincall'] is True:
                        message = (f'{member.name}:が入室しました')
                    else:
                        a = 1
                except TypeError:
                    a = 1
                    pass

                if b+a == 2:
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
        elif member.id is self.bot.user.id:
            pass


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(tts(bot))
