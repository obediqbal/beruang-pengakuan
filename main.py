import os
import discord
import random
from replit import db

from keep_alive import keep_alive
keep_alive()

client = discord.Client()
prefix = '>'

def get_user_id(author):
  if author not in db["user_id"].keys():
    rand = random.randint(0000,9999)
    while rand in db["user_id"].values():
      rand = random.randint(0000,9999)
    db["user_id"][author]=rand
  user_id = db["user_id"][author]

  return user_id

def reset_user_id(author):
  del db["user_id"][author]

def change_user_id_to(author,num):
  reset_user_id(author)
  db["user_id"][author]=num

def add_extra_digit(num):
  temp = ""
  for i in range(4-len(str(num))):
    temp+="0"
  temp+=str(num)
  return temp

def find_role(role,author):
  roles = map(str,author.roles)
  for i in roles:
    if role in i:
      return True
  return False
#Try changing boolean into int

@client.event
async def on_message(message):
  if str(message.channel)!="ngaku":
    if not str(message.channel).startswith("Direct Message"):
      return
  if message.author.bot:
    return

  msgid = message.id
  msg = message.content
  atchs = message.attachments
  author = message.author
  user_id = add_extra_digit(get_user_id(str(author)))

  if msg.startswith(prefix):
    args = []
    command = str(msg).split() 
    try:
      args = str(msg).split()[1:]
    except:
      pass

    try:
      if find_role("Normal People", author):
        if msg.startswith(prefix+'del_msg_all'):
          await message.channel.purge()
        if msg.startswith(prefix+'change_user_id_to') and len(args):
          if 0<int(args[0]) and int(args[0])<=9999 and int(args[0]) not in db["user_id"].values():
            change_user_id_to(str(author), int(args[0]))
      if msg.startswith(prefix+'reset_user_id'):
        reset_user_id(str(author))
    
    finally:
      try:
        await message.delete()
      finally:
        return

  try:
    await message.delete()
  except:
    pass
  await message.channel.send(f"`<{user_id}>`: {msg}")
  for atch in atchs:
    await message.channel.send(atch)

client.run(os.getenv('TOKEN'))

# TODO:
#   CONFESS VIA DM
#   LIST OF COMMANDS
#   DIFFERENT ID PER SERVER
#   FIX WRONG MESSAGE DELETETION