import os
import discord
import random
from replit import db

from keep_alive import keep_alive
keep_alive()

client = discord.Client()

def get_user_id(author):
  if author not in db["user_id"].keys():
    rand = random.randint(1000,9999)
    while rand in db["user_id"].values():
      rand = random.randint(1000,9999)
    db["user_id"][author]=rand
  user_id = db["user_id"][author]

  return user_id

# def delete_all_message(message):
#   for msg in message.channel:
#     print(msg)

@client.event
async def on_message(message):
  if message.author.bot or str(message.channel)!="ngaku":
    return

  msg = message.content;
  msgStripped = msg.strip("`")
  user_id = get_user_id(str(message.author))
  
  # delete_all_message(message)

  await message.channel.purge(limit=1)
  await message.channel.send(f"<{user_id}>: ```{msgStripped}```")

client.run(os.getenv('TOKEN'))