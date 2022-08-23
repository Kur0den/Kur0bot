import discord
from discord.ext import commands
from discord import app_commands

class Slashtest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.guild_only()
    async def test(self, interaction): 

        await interaction.response.send_message('いえい！！！！！！')
    

async def setup(bot):
    await bot.add_cog(Slashtest(bot))
