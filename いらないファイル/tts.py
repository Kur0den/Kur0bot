import asyncio
from collections import deque
from tempfile import TemporaryFile

import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions, has_permissions
from gtts import gTTS


async def on_message(self, message):
    if message.author.bot is False:
        message_queue = deque([])
        message = message.content[5:]
        usernick = message.author.display_name
        message = usernick + ":" + message
        try:
            if not self.vc_client.is_playing():
                tts = gTTS(message)
                f = TemporaryFile()
                tts.write_to_fp(f)
                f.seek(0)
                vc.play(discord.FFmpegPCMAudio(f, pipe=True))
            else:
                message_queue.append(message)
                while self.vc_client.is_playing():
                    await asyncio.sleep(0.1)
                tts = gTTS(message_queue.popleft())
                f = TemporaryFile()
                tts.write_to_fp(f)
                f.seek(0)
                vc.play(discord.FFmpegPCMAudio(f, pipe=True))
        except(TypeError, AttributeError):
            try:
                tts = gTTS(message)
                f = TemporaryFile()
                tts.write_to_fp(f)
                f.seek(0)
                channel = message.author.voice.channel
                vc = await channel.connect()
                vc.play(discord.FFmpegPCMAudio(f, pipe=True))
            except(AttributeError, TypeError):
                await message.channel.send("I'm not in a voice channel and neither are you!")
            return
        f.close()
        
        
        


    @commands.Cog.listener()
    async def on_message(self, message):
        if self.vc_client != None:
            if message.author.bot is False:
                if message.channel is self.vc_client.channel:
                    g_tts = gTTS(text=message.content, lang='ja', tld='jp')
                    name = uuid.uuid1()
                    g_tts.save(f'./tts/{name}.mp3')
                    self.vc_client.play(discord.FFmpegPCMAudio(f"./tts/{name}.mp3"))
