"""
A quick embed maker command.
Supports Title, URL, Description, Color, Timestamp, 
Author (name, icon, url), Footer (icon, name), Image (url), Thumbnail (url)

adding and inserting fields (name, value, inline, index), 
removing fields (index),
clearing fields,
editing fields (select -> name, value, inline)

export to json (text file if > 2000 chars),
import to json (modal but limited to 4000 chars),
reset and done buttons.
"""

import io
import copy
import json
import datetime
import discord
from discord.ext import commands
from discord import app_commands

class InputModal(discord.ui.Modal):
  def __init__(self, name, *text_inputs):
    super().__init__(title = '{} Modal'.format(name), timeout = 300.0)
    for text_input in text_inputs:
      self.add_item(text_input)
    self.done = False # prevents submitting same modal twice
  
  async def on_submit(self, interaction):
    if not self.done: 
      self.interaction = interaction
      self.done = True

class EmbedMakerView(discord.ui.View):
  def __init__(self, interaction, embed):
    super().__init__()
    self.interaction = interaction
    self.embed = embed
    self.embed_dict = copy.deepcopy(embed.to_dict()) # used for default values and reverting changes
    self.embed_original = copy.deepcopy(self.embed_dict) # for resetting

    self.update_fields(self.embed_original)
    
  async def interaction_check(self, interaction):
    if interaction.user == self.interaction.user:
      return True
    await interaction.response.send_message('あなたの実行したコマンドではないため操作はできません', ephemeral = True)
    return False

  async def on_error(self, interaction, error, item):
    embed = discord.Embed(
      title = 'Edit failed',
      description = '```fix\n{} \n```',
      color = discord.Color.red()
    )
    if isinstance(error, discord.HTTPException):
      embed.description = embed.description.format(error.text)
      await self.interaction.followup.send(embed = embed, ephemeral = True)
    elif isinstance(error, (ValueError, TypeError)): # .convert() failed, reuse the modal.interaction
      embed.description = embed.description.format(str(error))
      await error.interaction.response.send_message(embed = embed, ephemeral = True)
    else:
      #print('unhandled error:', interaction, error, item, error.__class__.__mro__, sep = '\n')
      raise error

  async def do(self, interaction, button, *text_inputs, method = None):
    name = button.label.lower()

    old_values = []
    for text_input in text_inputs:
      old = self.embed_dict.get(name, None)
      if hasattr(text_input, 'key'):
        if old:
          old = old.get(text_input.key, None)
      text_input.default = old
      old_values.append(old)
    
    modal = InputModal(button.label, *text_inputs)
    await interaction.response.send_modal(modal)
    timed_out = await modal.wait()
    if timed_out or not modal.done:
      return

    new_values = []
    for text_input in text_inputs:
      new = text_input.value.strip()
      if new:
        if hasattr(text_input, 'convert'):
          try:
            new = text_input.convert(new)
          except Exception as error:
            error.interaction = modal.interaction
            raise error
        new_values.append(new)
      else:
        new_values.append(None)

    if old_values == new_values:
      return await modal.interaction.response.defer()

    try:
      if method:
        kwargs = {
          text_input.key : new
          for text_input, new in zip(text_inputs, new_values)
        }
        getattr(self.embed, method)(**kwargs) # embed.set_author(name=...,url=...)
      else:
        setattr(self.embed, name, new_values[0]) # embed.title = ...
      await modal.interaction.response.edit_message(embed = self.embed)
      
    except Exception as error:
      self.embed = discord.Embed.from_dict(copy.deepcopy(self.embed_dict))
      raise error
    
    self.embed_dict = copy.deepcopy(self.embed.to_dict())

  def update_fields(self, embed_dict = None):
    embed_dict = embed_dict or self.embed_dict
    if 'fields' in embed_dict and embed_dict['fields']:
      self.remove_field_button.disabled = False
      self.clear_fields_button.disabled = False
      self.edit_field_select.disabled = False
      self.edit_field_select.options = [
        discord.SelectOption(label = 'Field {}'.format(i+1), description = field['name'][:100])
        for i, field in enumerate(embed_dict['fields'])
      ]
    else:
      self.remove_field_button.disabled = True
      self.clear_fields_button.disabled = True
      self.edit_field_select.disabled = True
  
  @discord.ui.button(label = 'Title', style = discord.ButtonStyle.blurple)
  async def title_button(self, interaction, button):
    text_input = discord.ui.TextInput(
      label = button.label, 
      placeholder = 'embedのタイトルを入力', 
      required = False
    )
    await self.do(interaction, button, text_input)

  @discord.ui.button(label = 'URL', style = discord.ButtonStyle.blurple)
  async def url_button(self, interaction, button):
    text_input = discord.ui.TextInput(
      label = button.label, 
      placeholder = 'embedのURLを入力', 
      required = False
    )
    await self.do(interaction, button, text_input)
    
  @discord.ui.button(label = 'Description', style = discord.ButtonStyle.blurple)
  async def description_button(self, interaction, button):
    text_input = discord.ui.TextInput(
      label = button.label, 
      placeholder = '説明を入力', 
      style = discord.TextStyle.long,
      required = False
    )
    await self.do(interaction, button, text_input)
    
  @discord.ui.button(label = 'Color', style = discord.ButtonStyle.blurple)
  async def color_button(self, interaction, button):
    text_input = discord.ui.TextInput(
      label = button.label, 
      placeholder = '16進数のカラーコードまたは色数値', 
      required = False
    )
    text_input.convert = lambda x: int(x) if x.isnumeric() else int(x.lstrip('#'), base = 16)
    await self.do(interaction, button, text_input)

  @discord.ui.button(label = 'Timestamp', style = discord.ButtonStyle.blurple)
  async def timestamp_button(self, interaction, button):
    text_input = discord.ui.TextInput(
      label = button.label, 
      placeholder = 'unixタイムスタンプを入力 例:"1659876635".', 
      required = False
    )
    def convert(x):
      try:
        return datetime.datetime.fromtimestamp(int(x))
      except:
        return datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S%z') # 1970-01-02T10:12:03+00:00
        
    text_input.convert = convert
    await self.do(interaction, button, text_input)

  @discord.ui.button(label = 'Author', style = discord.ButtonStyle.blurple)
  async def author_button(self, interaction, button):
    name_input = discord.ui.TextInput(
      label = 'Author Name', 
      placeholder = 'Author Nameを入力', 
      required = False
    )
    name_input.key = 'name'
    url_input = discord.ui.TextInput(
      label = 'URL', 
      placeholder = 'URLを入力.', 
      required = False
    )
    url_input.key = 'url'
    icon_input = discord.ui.TextInput(
      label = 'Author Icon URL', 
      placeholder = 'アイコンのURLを入力', 
      required = False
    )
    icon_input.key = 'icon_url'
    text_inputs = [name_input, url_input, icon_input]
    await self.do(interaction, button, *text_inputs, method = 'set_author')

  @discord.ui.button(label = 'Thumbnail', style = discord.ButtonStyle.blurple)
  async def thumbnail_button(self, interaction, button):
    text_input = discord.ui.TextInput(
      label = button.label, 
      placeholder = 'サムネイルの画像URL', 
      required = False
    )
    text_input.key = 'url'
    await self.do(interaction, button, text_input, method = 'set_thumbnail')
    
  @discord.ui.button(label = 'Image', style = discord.ButtonStyle.blurple)
  async def image_button(self, interaction, button):
    text_input = discord.ui.TextInput(
      label = button.label, 
      placeholder = '画像のURLを入力してください', 
      required = False
    )
    text_input.key = 'url'
    await self.do(interaction, button, text_input, method = 'set_image')
  
  @discord.ui.button(label = 'Image', style = discord.ButtonStyle.blurple)
  async def footer_button(self, interaction, button):
    text_input = discord.ui.TextInput(
      label = 'Footer Text', 
      placeholder = 'フッターの内容を入力', 
      required = False
    )
    text_input.key = 'text'
    icon_input = discord.ui.TextInput(
      label = 'Footer Icon URL', 
      placeholder = 'URLを入力', 
      required = False
    )
    icon_input.key = 'icon_url'
    text_inputs = [text_input, icon_input]
    await self.do(interaction, button, *text_inputs, method = 'set_footer')

  @discord.ui.button(label = 'Add Field', style = discord.ButtonStyle.blurple)
  async def add_field_button(self, interaction, button):
    name_input = discord.ui.TextInput(
      label = 'Field Name',
      placeholder = 'フィールドの名前を入力'
    )
    value_input = discord.ui.TextInput(
      label = 'Field Value', 
      placeholder = 'フィールドの内容を入力',
      style = discord.TextStyle.long
    )
    inline_input = discord.ui.TextInput(
      label = 'Field Inline (Optional)', 
      placeholder = '"1"を入力することによって、inline化されます。',
      required = False
    )
    index_input = discord.ui.TextInput(
      label = 'Field Index (Optional)',
      placeholder = 'フィールドをどこに入れるか指定できます。',
      required = False
    )
    text_inputs = [name_input, value_input, inline_input, index_input]
    
    modal = InputModal(button.label, *text_inputs)
    await interaction.response.send_modal(modal)
    timed_out = await modal.wait()
    if timed_out or not modal.done:
      return

    inline = inline_input.value.strip() == '1'
    index = None
    if index_input.value.strip().isnumeric():
      index = int(index_input.value)
                     
    embed = discord.Embed.from_dict(copy.deepcopy(self.embed_dict))
    
    kwargs = {
      'name' : name_input.value,
      'value' : value_input.value,
      'inline' : inline
    }
    if index or index == 0:
      kwargs['index'] = index
      embed.insert_field_at(**kwargs)
    else:
      embed.add_field(**kwargs)

    if embed == self.embed:
      return await modal.interaction.response.defer()

    self.update_fields(embed.to_dict())
    
    try:
      await modal.interaction.response.edit_message(embed = embed, view = self)
    except Exception as error:
      self.update_fields()
      raise error

    self.embed = embed
    self.embed_dict = copy.deepcopy(embed.to_dict())

  @discord.ui.select(placeholder = 'Edit Field', options = [discord.SelectOption(label = 'invisible option', description = 'because options cant be empty')])
  async def edit_field_select(self, interaction, select):
    index = int(select.values[0].lstrip('Field ')) - 1
    field = self.embed_dict['fields'][index]
    name_input = discord.ui.TextInput(
      label = 'Field Name', 
      placeholder = 'フィールドの名前を入力',
      default = field['name']
    )
    value_input = discord.ui.TextInput(
      label = 'Field Value', 
      placeholder = 'フィールドの説明を入力',
      style = discord.TextStyle.long,
      default = field['value']
    )
    inline_input = discord.ui.TextInput(
      label = 'Field Inline (Optional)', 
      placeholder = '"1"を入力することによって、inline化されます。',
      required = False,
      default = str(int(field['inline']))
    )
    text_inputs = [name_input, value_input, inline_input]
      
    modal = InputModal(select.placeholder, *text_inputs)
    await interaction.response.send_modal(modal)
    timed_out = await modal.wait()
    if timed_out or not modal.done:
      return

    inline = inline_input.value.strip() == '1'
                     
    kwargs = {
      'index' : index,
      'name' : name_input.value,
      'value' : value_input.value,
      'inline' : inline
    }

    embed = discord.Embed.from_dict(copy.deepcopy(self.embed_dict))
    embed.set_field_at(**kwargs)

    if embed == self.embed:
      return await modal.interaction.response.defer()

    self.update_fields(embed.to_dict())
    
    try:
      await modal.interaction.response.edit_message(embed = embed, view = self)
    except Exception as error:
      self.update_fields()
      raise error

    self.embed = embed
    self.embed_dict = copy.deepcopy(embed.to_dict())
    
  @discord.ui.button(label = 'Remove Field', style = discord.ButtonStyle.blurple)
  async def remove_field_button(self, interaction, button):
    # ?tag no modal selects
    text_input = discord.ui.TextInput(
      label = 'Field Index (Optional)', 
      placeholder = 'フィールド(n+1)を削除。未指定で最後のフィールド',
      required = False
    )
    
    modal = InputModal(button.label, text_input)
    await interaction.response.send_modal(modal)
    timed_out = await modal.wait()
    if timed_out or not modal.done:
      return
    
    if text_input.value.strip().isnumeric():
      index = int(text_input.value)
    else:
      index = len(self.embed_dict['fields']) - 1
    
    embed = discord.Embed.from_dict(copy.deepcopy(self.embed_dict))

    embed.remove_field(index)

    if embed == self.embed:
      return await modal.interaction.response.defer()

    self.embed = embed
    self.embed_dict = copy.deepcopy(embed.to_dict())
  
    self.update_fields()

    await modal.interaction.response.edit_message(embed = embed, view = self)
    
  @discord.ui.button(label = 'Clear Fields', style = discord.ButtonStyle.red)
  async def clear_fields_button(self, interaction, button):
    self.embed.clear_fields()
    self.embed_dict = copy.deepcopy(self.embed.to_dict())
    self.update_fields()
    await interaction.response.edit_message(embed = self.embed, view = self)

  @discord.ui.button(label = 'Reset', style = discord.ButtonStyle.red)
  async def reset_button(self, interaction, button):

    if self.embed_original == self.embed_dict:
      return await interaction.response.defer()

    self.embed = discord.Embed.from_dict(copy.deepcopy(self.embed_original))
    self.embed_dict = copy.deepcopy(self.embed_original)
    self.update_fields(self.embed_original)
    await interaction.response.edit_message(embed = self.embed, view = self)
  
  @discord.ui.button(label = 'Import JSON', style = discord.ButtonStyle.green)
  async def import_button(self, interaction, button):
    text_input = discord.ui.TextInput(
      label = 'JSON', 
      placeholder = 'JSONを張り付けて下さい。',
      style = discord.TextStyle.long
      #more than 4000 characters needs files/pastebin
    ) 
    modal = InputModal(button.label, text_input)
    await interaction.response.send_modal(modal)
    timed_out = await modal.wait()
    if timed_out:
      return

    try:
      embed_dict = json.loads(text_input.value)
    except Exception as error:
      error.interaction = modal.interaction
      raise error

    embed = discord.Embed.from_dict(embed_dict)

    if embed == self.embed:
      return await modal.interaction.response.defer()

    await modal.interaction.response.edit_message(embed = embed)
    self.embed = embed
    self.embed_dict = copy.deepcopy(embed.to_dict()) # no user keys

  @discord.ui.button(label = 'Export JSON', style = discord.ButtonStyle.green)
  async def export_button(self, interaction, button):

    data = json.dumps(self.embed_dict, indent = 2)
    text = '```json\n{}```'
    if len(data) > 2000 - len(text) + 2:
      await interaction.response.send_message(
        file = discord.File(io.StringIO(data), filename = 'embedmaker.json'),
        ephemeral = True
      )
    else:
      await interaction.response.send_message(text.format(data), ephemeral = True)
  
  @discord.ui.button(label = 'Stop', style = discord.ButtonStyle.red)
  async def stop_button(self, interaction, button):
    await interaction.response.edit_message(view = None)
    self.stop()
    
class EmbedMaker(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    
  @app_commands.command()
  @app_commands.guilds(733707710784340100)
  @app_commands.guild_only()
  async def embedmaker(self, interaction): 
    """Interactively makes an embed from scratch"""

    embed = discord.Embed(
      title = 'Embed Maker!',
      #description = 'Click the buttons below to edit this embed.'
    )

    view = EmbedMakerView(interaction, embed)
    
    await interaction.response.send_message(embed = embed, view = view)

    timed_out = await view.wait()

    if timed_out:
      message = await interaction.original_message()
      await message.edit(view = None)

async def setup(bot):
  await bot.add_cog(EmbedMaker(bot))
