from discord.ext import commands
from discord import app_commands


class disconnect(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        stage = self.bot.get_channel(884734698759266324)
        if member.id == self.bot.user.id:
            if before.channel != after.channel:
                if before.channel is not None and before.channel != stage and before.channel == self.bot.guild.afk_channel:
                    newinfo = {
                        'channel_id': before.channel.id,
                        'tts': False,
                        'joincall':False,
                        'radio': False,
                        'radioURL': None
                    }
                    await self.bot.vc_info.replace_one({
                        'channel_id': before.channel.id
                    }, newinfo, upsert=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(disconnect(bot))