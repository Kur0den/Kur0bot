import os

import discord
from discord import app_commands
from discord.ext import commands
from gtts import gTTS



class tts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    group = app_commands.Group(name="tts", description="Text To Speech", guild_ids=[733707710784340100], guild_only=True)

@group.command()
@app_commands.guild_only()
async def join(self, interaction: discord.Interaction):
    
    await interaction.response.send_message()


@group.command()
@app_commands.guild_only()
async def leave(self, interaction: discord.Interaction):
    
    await interaction.response.send_message()




# メッセージ取得
async def on_message(self, message):
    if message.channel.type is (self.bot.vc1 or self.bot.vc2 or self.bot.vc3):


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(tts(bot))
