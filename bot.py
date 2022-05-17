from discord.ext import commands
import os

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    async def setup_hook(self):
        for file in os.listdir('./cog'):
            if file.endswith('.py'):
                await self.load_extension(f'cog.{file[:-3]}')
                print(f'Loaded cog: {file[:-3]}')
        print('cog loaded')
        print(f'ready: {self.user} (ID: {self.user.id})')