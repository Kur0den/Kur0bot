import datetime

import re
import aiohttp
import discord
import Paginator
from discord import app_commands
from discord.ext import commands


def purge_check(m):
    return not m.embeds[0].title in ['しりとりヘルプ', 'チャンネルリセット中...'] if bool(m.embeds) else True

def is_siritori_ch(ctx):
    return ctx.channel.id == 982967189109878804

class comment_modal(discord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="コメント",
            timeout=1024,
        )

        self.read = discord.ui.TextInput(
            label="コメント内容",
            style=discord.TextStyle.long,
            placeholder="発言したい内容",
            max_length=128,
            required=True,
        )
        self.add_item(self.read)

    async def on_submit(self, interaction) -> None:
        self.stop()
        embed = discord.Embed(colour=interaction.user.top_role.color, description=self.read.value)
        embed.set_footer(text=f'こめんと')
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

async def siritori_reset(self):
    self.bot.siritori = False
    n_member = 'None'
    async for msg in self.bot.siritori_ch.history(limit=None):
        if msg.content.endswith('ん'):
            n_member = msg.author
            break
    
    if n_member != 'None':
        siritori_fine = -int(self.bot.config['siritori_fine'])
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
    async def history(self, interaction: discord.Interaction, page: int = 1, show: bool = False):
        if not self.bot.siritori:
            return
        tango_count = 1
        page_count = 0
        pages = {}
        page_naiyou = ''
        for r in range(0, len(self.bot.siritori_list), 10):
            for tango in self.bot.siritori_list[r:r+10]:
                if page_naiyou == '':
                    page_naiyou = f"{tango_count}. {tango}"
                else:
                    page_naiyou += f"\n{tango_count}. {tango}"
                tango_count += 1
            pages[page_count] = discord.Embed(title='履歴', description=page_naiyou)
            page_count += 1
            page_naiyou = ''
        
        page-=1
        
        match show: # 公開するかどうかの設定を反転
            case True:
                show = False
            case False:
                show = True
        try:
            await Paginator.Simple(InitialPage=page,ephemeral=show).start(interaction, pages=pages)
        except KeyError:
            await Paginator.Simple(ephemeral=show).start(interaction, pages=pages)
        return

    @group.command(name='len', description='連結回数を表示します')
    async def _len(self, interaction):
        if not self.bot.siritori:
            return
        await interaction.response.send_message(embed=discord.Embed(title='現在の連結回数', description=len(self.bot.siritori_list), color=0x00ffff), ephemeral=True)
    
    @group.command(name='comment', description='しりとりとは関係ないコメントを送信できます')
    async def name(self, interaction: discord.Interaction):
        modal=comment_modal()
        await interaction.response.send_modal(modal)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.bot.siritori:
            return
        if not message.channel.id == 982967189109878804:
            return

        if message.author.bot or message.content.startswith(self.bot.command_prefix):
            return

        r = re.compile('([\u3040-\u309F]|\u30FC)+')
        if r.fullmatch(message.content) == None:
            await message.delete()
            embed = discord.Embed(title="エラー", colour=discord.Colour(0xff0000), description="しりとりはひらがなで投稿してください")
            await message.channel.send(content=message.author.mention, embed=embed, delete_after=15)
            return

        if message.content in self.bot.siritori_list:
            await message.delete()
            await message.channel.send(embed=discord.Embed(title=f'”{message.content}” はすでに使用されています', color=0xff0000).set_author(name=message.author.name, icon_url=message.author.display_avatar.url))
            return

        messages = [message async for message in message.channel.history(limit=10)]
        i = 0
        for m in messages:
            if i == 0:
                i += 1
                continue
            elif m.author.bot == False:
                next_message=m
                break
        if message.author == next_message.author:
            await message.delete()
            await message.channel.send(embed=discord.Embed(title=f'同じ人が続けて投稿することはできません', color=0xff0000).set_author(name=message.author.name, icon_url=message.author.display_avatar.url), delete_after=15)
            return

        if next_message.content[-1] != message.content[0]:
            r = re.compile('[\u30FC\u3041\u3043\u3045\u3047\u3049\u3063\u3083\u3085\u3087]')
            if r.fullmatch(next_message.content[-1]) != None:
                if next_message.content[-2] != message.content[0]:
                    if r.fullmatch(next_message.content[-2]) != None:
                        if next_message.content[-3] != message.content[0]:
                            await message.delete()
                            await message.channel.send(embed=discord.Embed(title=f'前の人が投稿した最後の文字が最初に来る単語を投稿してください', color=0xff0000).set_author(name=message.author.name, icon_url=message.author.display_avatar.url), delete_after=15)
                            return
                        else:
                            pass
                    else:
                        await message.delete()
                        await message.channel.send(embed=discord.Embed(title=f'前の人が投稿した最後の文字が最初に来る単語を投稿してください', color=0xff0000).set_author(name=message.author.name, icon_url=message.author.display_avatar.url), delete_after=15)
                        return
                else:
                    pass
            else:
                await message.delete()
                await message.channel.send(embed=discord.Embed(title=f'前の人が投稿した最後の文字が最初に来る単語を投稿してください', color=0xff0000).set_author(name=message.author.name, icon_url=message.author.display_avatar.url), delete_after=15)
                return

        if message.content.endswith('ん'):
            print('ん！！！！！')
            await siritori_reset(self)
            return

        self.bot.siritori_list.append(message.content)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not self.bot.siritori:
            return
        if not payload.channel_id == 982967189109878804:
            return
        message = await (self.bot.guild.get_channel(982967189109878804).fetch_message(payload.message_id))
        if not message.author == self.bot.user:
            return
        if message.interaction == None:
            return
        member = self.bot.guild.get_member(payload.user_id)
        if not message.interaction.type == discord.InteractionType.application_command:
            return
        if not message.interaction.user == member:
            return
        if not message.embeds[0].footer.text == 'こめんと':
            return
        if not payload.emoji.name == '🗑️':
            return
        await message.delete()


async def setup(bot):
    await bot.add_cog(Siritori(bot))
