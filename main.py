import os
import discord
import random
from replit import db

from keep_alive import keep_alive
keep_alive()

client = discord.Client()
db[user_id]={}
db[list_id]=[]

def get_user_id(author):
  if db[user_id].get(author,-1)!=-1:
    rand = random.randint(1000,9999)
    while rand in db[list_id]:
      rand=random.randint(1000,9999)
    db[user_id][author]=rand
  
  return db[user_id][author]

@client.event
async def on_message(message):
  if message.author.bot and message.channel=="ngaku":
    return

  msg = message.content;
  user_id = get_user_id(message.author)

  await message.channel.send(user_id)

client.run(os.getenv('TOKEN'))