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

def find_role(role,author):
  roles = map(str,author.roles)
  for i in roles:
    if role in i:
      return True
  return False

def reset_user_id(author):
  del db["user_id"][author]

@client.event
async def on_message(message):
  if str(message.channel)!="ngaku":
    if not str(message.channel).startswith("Direct Message"):
      return
  if message.author.bot:
    return

  msg = message.content;
  user_id = get_user_id(str(message.author))

  if msg.startswith('>'):
    if find_role("Normal People", message.author):
      if msg.startswith('>del_msg_all'):
        await message.channel.purge()
    if msg.startswith('>reset_user_id'):
      reset_user_id(str(message.author))
    await message.channel.purge(limit=1)
    return
  
  # delete_all_message(message)

  try:
    await message.channel.purge(limit=1)
  except:
    pass
  await message.channel.send(f"`<{user_id}>`: {msg}")

client.run(os.getenv('TOKEN'))