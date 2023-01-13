from discord.ext import commands
from discord import app_commands
import discord


class radio(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot):
        self.bot = bot

    group = app_commands.Group(name="radio", description="web radio", guild_ids=[733707710784340100], guild_only=True)

    @group.command(name='connect', description='VCに接続します')
    @app_commands.guild_only()
    async def radio_join(self, interaction: discord.Interaction, url: str):
        if interaction.channel is self.bot.vc1 or interaction.channel is self.bot.vc2 or interaction.channel is self.bot.vc3:
            if self.bot.guild.voice_client == None:
                if interaction.user.voice.channel is interaction.channel:
                    await interaction.channel.connect()
                    await interaction.response.send_message(f'{url} を再生します')
                    self.bot.guild.voice_client.play(discord.FFmpegPCMAudio(url))
                    return
        await interaction.response.send_message('接続に失敗しました\nこのコマンドは接続しているVCの聞き専チャンネルで使用してください')

    @group.command(name='disconnect', description='VCから切断します')
    @app_commands.guild_only()
    async def radio_leave(self, interaction: discord.Interaction):
        if self.bot.guild.voice_client != None:
            if interaction.channel is self.bot.guild.voice_client.channel:
                if interaction.user.voice.channel is self.bot.guild.voice_client.channel:
                    await self.bot.guild.voice_client.disconnect()
                    self.vc = None
                    await interaction.response.send_message('切断しました')
                    return
        await interaction.response.send_message('失敗しました')

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(radio(bot))