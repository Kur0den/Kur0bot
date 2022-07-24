# Kur0bot
* くろでんによるくろでんのためのぼっと
* くろでんが基本作成しているbotです
# 起動方法
* ```pip install -r requirements.txt```
でいるものを追加します

* ```.env.sample```を```.env```に変え、TOKEN=""のところにTOKENを入れてください、

<details><summary>別のBotで使う場合</summary>

((ながいけどゆるして))
* いろいろな定義を変更する必要があります。
まず、0den.pyの
```py:0den.py
guild_id = 733707710784340100
```
を自分のサーバーのIDに変更してください。
また、その下少し行くと、
```py:0den.py
bot.manageguild = bot.get_guild(981923517736046592)
bot.guild = bot.get_guild(733707710784340100)
bot.owner = bot.get_user(699414261075804201)
bot.unei_role = bot.guild.get_role(738956776258535575)
bot.unei_members = bot.unei_role.members
bot.everyone = bot.guild.get_role(733707710784340100)
```
とあると思いますのでそこも変えてください。
<details1><summary>上から順に何かを説明</summary>
* manageguildは管理するサーバーのidを貼ってください。
* guildはサーバーを貼ってください。
* ownerはBot所有者のidを貼ってください。
* unei_roleはサーバーの運営につけましょう
* everyoneは@@everyoneのidを張ってください。
取得方法は知りません
</details1>
* もう少し下にまだあるからそれも設定してください。
```py:0den.py
bot.siritori_ch = bot.get_channel(982967189109878804)
```
しりとりのチャンネルを貼ってください。

* 多分最後です。
VC系統の定義で、
```py:0den.py
bot.vc1 = bot.get_channel(981800095760670730)
bot.vc2 = bot.get_channel(981800262165495828)
bot.vc3 = bot.get_channel(981800316116803636)
```
* というのがあるはずです。
一つのVCの場合はvc2,vc3のget_channelの中身を殻にしておいてください。
それ以外はすべて埋めましょう。
</details>

# ちょうざつ
https://7bot.ml/chozatu

