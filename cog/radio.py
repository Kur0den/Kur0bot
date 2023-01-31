import asyncio

import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

class radio(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot):
        self.bot = bot

    group = app_commands.Group(name="radio", description="web radio", guild_ids=[733707710784340100], guild_only=True)

    @group.command(name='connect', description='ラジオを再生します')
    @app_commands.guild_only()
    async def radio_join(self, interaction: discord.Interaction, url: str):
        vcinfo = await self.bot.vc_info.find_one({
            'channel_id': interaction.channel.id
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
            if ttsinfo is None:
                if interaction.user.voice.channel is interaction.channel:
                    if kur0info['radio'] is False:
                        if radioinfo is None:
                            await interaction.channel.connect()
                            await interaction.response.send_message(f'{url} を再生します')
                            self.bot.guild.voice_client.play(discord.FFmpegPCMAudio(url))
                            new_info = {
                                'channel_id': interaction.channel_id,
                                'tts': vcinfo['tts'],
                                'joincall': vcinfo['joincall'],
                                'radio': True,
                                'radioURL': str(url)
                            }
                            await self.bot.vc_info.replace_one({
                                'channel_id': interaction.channel_id
                            }, new_info, upsert=True)
                            status = discord.Game(name=f'VCで{url}を再生中', start=datetime.utcnow)
                            await self.bot.change_presence(activity=status)
                            return
                        elif radioinfo['channel_id'] == interaction.channel.id:
                            self.bot.guild.voice_client.stop()
                            await interaction.response.send_message(f'現在再生しているラジオを止めて{url} を再生します')
                            self.bot.guild.voice_client.play(discord.FFmpegPCMAudio(url))
                            new_info = {
                                'channel_id': interaction.channel_id,
                                'tts': vcinfo['tts'],
                                'joincall': vcinfo['joincall'],
                                'radio': True,
                                'radioURL': str(url)
                            }
                            await self.bot.vc_info.replace_one({
                                'channel_id': interaction.channel_id
                            }, new_info, upsert=True)
                            status = discord.Game(name=f'VCで{url}を再生中', start=datetime.utcnow)
                            await self.bot.change_presence(activity=status)
                        else:
                            await interaction.response.send_message('他のチャンネルですでにbotが使用されているため使用できません')
                    else:
                        await interaction.response.send_message('既に<@875961973597171722>がラジオモードとして接続されています\nTTSモードとして使用するか<@875961973597171722>をVCから切断して再度コマンドを実行してください')
                else:
                    await interaction.response.send_message('接続に失敗しました\nこのコマンドは接続しているVCの聞き専チャンネルで使用してください')
            else:
                await interaction.response.send_message('他のチャンネルですでにbotが使用されているため使用できません')
        else:
            await interaction.response.send_message('このコマンドは接続しているVCの聞き専チャンネルで使用してください')

    @group.command(name='disconnect', description='VCから切断します')
    @app_commands.guild_only()
    async def radio_leave(self, interaction: discord.Interaction):
        vcinfo = await self.bot.vc_info.find_one({
            'channel_id': interaction.channel.id
        }, {
            "_id": False  # 内部IDを取得しないように
        })
        if vcinfo['radio'] is True:
            if interaction.user.voice.channel is interaction.channel:
                await self.bot.guild.voice_client.disconnect()
                new_info = {
                    'channel_id': interaction.channel_id,
                    'tts': vcinfo['tts'],
                    'joincall': vcinfo['joincall'],
                    'radio': False,
                    'radioURL': None
                }
                await self.bot.vc_info.replace_one({
                    'channel_id': interaction.channel_id
                }, new_info, upsert=True)
                status = discord.Game(name='くろでんのくろでんによるくろでんのためのぼっと')
                await self.bot.change_presence(activity=status)
                await interaction.response.send_message('切断しました')
                return
        await interaction.response.send_message('失敗しました')


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        beforeinfo = None
        try:
            beforeinfo = await self.bot.vc_info.find_one({
                'channel_id': before.channel.id
            }, {
                "_id": False  # 内部IDを取得しないように
            })
        except AttributeError:
            pass
        if member.id is self.bot.user.id:
            if before.channel is not None and after.channel is None and beforeinfo['radio'] is True:
                await self.bot.guild.voice_client.disconnect()
                await self.bot.change_presence(activity=discord.Activity(name='くろでんのくろでんによるくろでんのためのぼっと', type=discord.ActivityType.playing))

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(radio(bot))