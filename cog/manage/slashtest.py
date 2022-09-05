import discord
from discord.ext import commands
from discord import app_commands

class Slashtest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    group = app_commands.Group(name="test", description="楽しもう！", guild_ids=[733707710784340100], guild_only=True)
    
    @group.command(name="reply", description='オウム返し')
    @app_commands.guild_only()
    async def test(self, interaction, string :str):
        await interaction.response.send_message(string)
    

async def setup(bot):
    await bot.add_cog(Slashtest(bot))
