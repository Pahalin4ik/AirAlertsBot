import os
from pyrogram import Client, types
from dispacher import bot
from config import ChannelId, db
from translate import Translator


app = Client("alerts parser", os.environ.get("ApiId"),
             os.environ.get("ApiHash"))
t = Translator(to_lang="en")


@app.on_message()
async def parse(client: Client, message: types.Message):
    if message.chat.id != ChannelId:
        return
    tag = message.text.split("\n")[-1]
    users = db.get_users_by_tag("".join(tag))
    text = {
        "EN": t.translate(message.text),
        "UA": message.text
    }
    for i in users:
        await bot.send_message(i[0], text[i[1]])



