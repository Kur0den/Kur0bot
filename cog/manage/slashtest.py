import discord
from discord.ext import commands
from discord import app_commands

class Dropdown(discord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Red', description='Your favourite colour is red', emoji='🟥'),
            discord.SelectOption(label='Green', description='Your favourite colour is green', emoji='🟩'),
            discord.SelectOption(label='Blue', description='Your favourite colour is blue', emoji='🟦'),
        ]
        super().__init__(placeholder='Choose your favourite colour...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        await interaction.response.send_message(f'Your favourite colour is {self.values[0]}')


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown())
class Slashtest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.guild_only()
    async def test(self, interaction): 

        view = DropdownView()
        await interaction.response.send_message('いえい！！！！！！', view=view)
    

async def setup(bot):
    await bot.add_cog(Slashtest(bot))
