import datetime

import aiohttp
import discord
from discord.ext import commands
from discord import app_commands


def purge_check(m):
    return not m.embeds[0].title in ['しりとりヘルプ', 'チャンネルリセット中...'] if bool(m.embeds) else True

def is_siritori_ch(ctx):
    return ctx.channel.id == 982967189109878804

async def siritori_reset(self):
    self.bot.siritori = False
    n_member = 'None'
    async for msg in self.bot.siritori_ch.history(limit=None):
        if msg.content.endswith('ん'):
            n_member = msg.author
            break
    
    if n_member != 'None':
        siritori_fine = -int(self.bot.config['siritori_fine'])
        # siritori_fine = -siritori_fine
        async with aiohttp.ClientSession(headers=self.bot.ub_header) as session:
            await session.patch(url=f'{self.bot.ub_url}{n_member.id}', json={'cash': siritori_fine, 'reason': f'しりとり罰金'}) 
    
    msg = await self.bot.siritori_ch.send(embed=discord.Embed(title='チャンネルリセット中...', description='しりとりが終了しました', color=0x00ffff))
    await self.bot.siritori_ch.purge(limit=None, check=purge_check)
    if n_member == 'None':
        await msg.edit(
            embed=discord.Embed(
                title='しりとりが終了しました', 
                description=f'連結回数: {len(self.bot.siritori_list)}\n”ん”をつけた人: {n_member}',
                color=0x00ffff
            )
        )
    else:
        await msg.edit(
            embed=discord.Embed(
                title='しりとりが終了しました', 
                description=f'連結回数: {len(self.bot.siritori_list)}\n”ん”をつけた人: {n_member.mention}',
                color=0x00ffff
            )
        )

    self.bot.siritori_list = []
    self.bot.siritori = True
    return()



class Siritori(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    group = app_commands.Group(name="siritori", description="しりとり関連", guild_ids=[733707710784340100], guild_only=True)
    
    @group.command(name="reset", description='リセットします')
    async def reset(self, interaction: discord.Interaction):
        if interaction.user.get_role(self.bot.unei_role.id) is not None:
            if interaction.channel_id == self.bot.siritori_ch.id:
                if not self.bot.siritori:
                    return
                await interaction.response.send_message('リセットします',ephemeral=True)
                
                await siritori_reset(self)
                return
            await interaction.response.send_message('しりとり部屋以外では実行できません',ephemeral=True)
            return
        await interaction.response.send_message('運営以外は実行できません',ephemeral=True)
    
    @group.command(name="remove", description='単語を削除します')
    async def remove(self, interaction: discord.Interaction, moji: str):
        if interaction.channel_id == self.bot.siritori_ch.id:
            if not self.bot.siritori:
                return
            if not moji in self.bot.siritori_list:
                await interaction.response.send_message(embed=discord.Embed(title='発言されたことのない単語です', color=0xff0000), ephemeral=True)
                return
            if self.bot.unei_role in interaction.user.roles:
                async for msg in interaction.channel.history():
                    if msg.content == moji:
                        await msg.delete()
                self.bot.siritori_list.remove(moji)
                await interaction.response.send_message(embed=discord.Embed(title=f'”{moji}”を削除しました', color=0x00ffff))
                return
            
            async for msg in interaction.channel.history():
                if msg.content == moji and msg.author.id == interaction.user.id:
                    await msg.delete()
                    self.bot.siritori_list.remove(moji)
                    await interaction.responce.send_message(embed=discord.Embed(title=f'”{moji}”を削除しました', color=0x00ffff))
                    return
            await interaction.response.send(embed=discord.Embed(f'過去100メッセージに{interaction.user.mention}が送信した”{moji}”という内容のメッセージがみつかりませんでした', color=0xff0000), ephemeral=True)
            return
        await interaction.response.send_message('しりとり部屋以外では実行できません',ephemeral=True)
    
    @group.command(name='history', description='履歴を表示します')
    async def history(self, interaction, page=1):
        if not self.bot.siritori:
            return
        tango_count = 1
        page_count = 1
        pages = {}
        page_naiyou = ''
        for r in range(0, len(self.bot.siritori_list), 10):
            for tango in self.bot.siritori_list[r:r+10]:
                if page_naiyou == '':
                    page_naiyou = f"{tango_count}. {tango}"
                else:
                    page_naiyou += f"\n{tango_count}. {tango}"
                tango_count += 1
            pages[page_count] = page_naiyou
            page_count += 1
            page_naiyou = ''
        await interaction.responce.send_message(embed=discord.Embed(title='履歴', description=f'```{pages[page]}```').set_footer(text=f'{page}/{page_count-1}'))
        return
    
    
    
    @group.command(name='len', description='連結回数を表示します')
    async def _len(self, interaction):
        if not self.bot.siritori:
            return
        await interaction.responce.send_message(embed=discord.Embed(title='現在の連結回数', description=len(self.bot.siritori_list), color=0x00ffff))
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.bot.siritori:
            return
        if not message.channel.id == 982967189109878804:
            return
        
        if message.author.bot or message.content.startswith(self.bot.command_prefix) or message.content.startswith('!'):
            return
        
        if message.content in self.bot.siritori_list:
            await message.delete()
            await message.channel.send(embed=discord.Embed(title=f'”{message.content}” はすでに使用されています', color=0xff0000).set_author(name=message.author.name, icon_url=message.author.display_avatar.url))
            return

        if message.content.endswith('ん'):
            print('ん！！！！！')
            await siritori_reset(self)
        
        self.bot.siritori_list.append(message.content)
        
        
async def setup(bot):
    await bot.add_cog(Siritori(bot))
