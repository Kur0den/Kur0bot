import discord
from discord.ext import commands


class quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        QuoteBot = self.bot.guild.get_member(949479338275913799)
        if message.author == QuoteBot:
            Call_Channel = message.channel
            Call_Message = await Call_Channel.fetch_message(message.reference.message_id)
            if Call_Message.reference is not None:
                Origin_Channel = await self.bot.guild.fetch_channel(Call_Message.reference.channel_id)
                Origin_Message = await Origin_Channel.fetch_message(Call_Message.reference.message_id)
                NotQuoteRole = self.bot.guild.get_role(978291308332453928)
                if NotQuoteRole in Origin_Message.author.roles:
                    embed = discord.Embed(title="参照元のユーザーがQuoteを拒否しているため削除しました", colour=discord.Colour(0x7289da))
                    await message.channel.send(embed = embed, delete_after = 10)
                    await message.delete()

async def setup(bot):
    await bot.add_cog(quote(bot))
