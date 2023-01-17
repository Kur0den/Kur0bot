import asyncio

import discord
from discord import app_commands
from discord.ext import commands


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
        if vcinfo is not None:
            if ttsinfo is None:
                if interaction.user.voice.channel is interaction.channel:
                    if radioinfo is None:
                        await interaction.channel.connect()
                        await interaction.response.send_message(f'{url} を再生します')
                        self.bot.guild.voice_client.play(discord.FFmpegPCMAudio(url))
                        new_info = {
                            'channel': vcinfo['channel'],
                            'channel_id': interaction.channel_id,
                            'owner_id': vcinfo['owner_id'],
                            'tts': vcinfo['tts'],
                            'joincall': vcinfo['joincall'],
                            'radio': True,
                            'radioURL': str(url),
                            'mode': vcinfo['mode'],
                            'dashboard_id': vcinfo['dashboard_id']
                        }
                        await self.bot.vc_info.replace_one({
                            'channel_id': interaction.channel_id
                        }, new_info, upsert=True)
                        return
                    elif radioinfo['channel_id'] == interaction.channel.id:
                        self.bot.guild.voice_client.stop()
                        await interaction.response.send_message(f'現在再生しているラジオを止めて{url} を再生します')
                        self.bot.guild.voice_client.play(discord.FFmpegPCMAudio(url))
                        new_info = {
                            'channel': vcinfo['channel'],
                            'channel_id': interaction.channel_id,
                            'owner_id': vcinfo['owner_id'],
                            'tts': vcinfo['tts'],
                            'joincall': vcinfo['joincall'],
                            'radio': True,
                            'radioURL': str(url),
                            'mode': vcinfo['mode'],
                            'dashboard_id': vcinfo['dashboard_id']
                        }
                        await self.bot.vc_info.replace_one({
                            'channel_id': interaction.channel_id
                        }, new_info, upsert=True)
                        return
                await interaction.response.send_message('接続に失敗しました\nこのコマンドは接続しているVCの聞き専チャンネルで使用してください')
                return
        await interaction.response.send_message('他のチャンネルですでにbotが使用されているため使用できません')
        return

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
                    'channel': vcinfo['channel'],
                    'channel_id': interaction.channel_id,
                    'owner_id': vcinfo['owner_id'],
                    'tts': vcinfo['tts'],
                    'joincall': vcinfo['joincall'],
                    'radio': False,
                    'radioURL': None,
                    'mode': vcinfo['mode'],
                    'dashboard_id': vcinfo['dashboard_id']
                }
                await self.bot.vc_info.replace_one({
                    'channel_id': interaction.channel_id
                }, new_info, upsert=True)
                await interaction.response.send_message('切断しました')
                return
        await interaction.response.send_message('失敗しました')


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
        if member.id is self.bot.user.id:
            if before.channel is not None and after.channel is None and beforeinfo['radio'] is True:
                await self.bot.guild.voice_client.disconnect()
                await asyncio.sleep(10)
                vcinfo = await self.bot.vc_info.find_one({
                    'channel_id': before.channel.id
                }, {
                    "_id": False  # 内部IDを取得しないように
                })
                new_info = {
                    'channel': vcinfo['channel'],
                    'channel_id': before.channel.id,
                    'owner_id': vcinfo['owner_id'],
                    'tts': False,
                    'joincall': False,
                    'radio': False,
                    'radioURL': None,
                    'mode': vcinfo['mode'],
                    'dashboard_id': vcinfo['dashboard_id']
                }
                await self.bot.vc_info.replace_one({
                    'channel_id': before.channel.id
                }, new_info, upsert=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(radio(bot))