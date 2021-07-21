import os
import discord
import random
from replit import db

from keep_alive import keep_alive
keep_alive()

client = discord.Client()

prefix=''
authority=''
commands={}
dbUID = {}
# for key in db.keys():
#   del db[key]

def load_db():
  # if "server" not in db.keys():

  if "prefix" not in db.keys():
    db["prefix"] = '>'
  if "authority" not in db.keys():
    db["authority"] = 'Normal People'
  if "commands" not in db.keys():
    db["commands"] = {
      'purge_messages' : 'purgeMessages',
      'change_user_ID' : 'changeUID',
      'change_bot_prefix' : 'changePrefix',
      'reset_user_id' : 'resetUID',
      'commands_list' : 'help'
    }
  if "user_id" not in db.keys():
    db["user_id"] = {}
  global prefix, authority, commands, dbUID
  prefix = db["prefix"]
  authority = db["authority"]
  commands = db["commands"]
  dbUID = db["user_id"]

def save_to_db(key,changes):
  del db[key]
  db[key]=changes

def get_user_id(author):
  author = str(author)
  if author not in dbUID.keys():
    rand = random.randint(0000,9999)
    while rand in dbUID.values():
      rand = random.randint(0000,9999)
    dbUID[author]=rand
  user_id = dbUID[author]

  return user_id

def reset_user_id(author):
  author = str(author)
  del dbUID[author]

def change_user_id_to(author,num):
  author = str(author)
  reset_user_id(author)
  dbUID[author]=num

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
async def on_ready():
  load_db()
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name="your confession"))

@client.event
async def on_message(message):

  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name="your confession"))
  if str(message.channel)!="ngaku":
    if not str(message.channel).startswith("Direct Message"):
      return
  if message.author.bot:
    return

  msg = message.content
  atchs = message.attachments
  author = message.author
  user_id = add_extra_digit(get_user_id(author.id))

  if msg.startswith(prefix):
    args = [] 
    try:
      args = str(msg).split()[1:]
    finally:
      try:
        if find_role(authority, author):
          if msg.startswith(prefix+commands['purge_messages']):
            await message.channel.purge()
          elif msg.startswith(prefix+commands['change_user_ID']) and len(args):
            if 0<int(args[0]) and int(args[0])<=9999 and int(args[0]) not in dbUID.values():
              change_user_id_to(author.id, int(args[0]))
          elif msg.startswith(prefix+commands['change_bot_prefix']):
            save_to_db("prefix",args[0])
            load_db()
        if msg.startswith(prefix+commands['reset_user_id']):
          reset_user_id(author.id)
        elif msg.startswith(prefix+commands['commands_list']):
          s = "```"
          for command in commands:
            s+=f"{command} : {commands[command]}\n"
          s+=f"prefix : {prefix}```"
          await message.channel.send(s)
            
      
      finally:
        try:
          await message.delete()
        finally:
          return

  try:
    pass
    await message.delete()
  finally:
    await message.channel.send(content=f"`<{user_id}>`: {msg}",reference=message.reference)
    for atch in atchs:
      await message.channel.send(atch)

client.run(os.getenv('TOKEN'))

# TODO:
#   CONFESS VIA DM
#   DIFFERENT ID PER SERVER