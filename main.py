import os
import discord
import random
import json
from replit import db

from keep_alive import keep_alive

keep_alive()

client = discord.Client()

default_prefix = '>'
default_authority = 'Normal People'
default_commands = {
            'purge_messages': 'purgeMessages',
            'change_user_ID': 'changeUID',
            'change_bot_prefix': 'changePrefix',
            'reset_user_id': 'resetUID',
            'commands_list': 'help'
            }
default_userIds = {}
         
class Parser(object):
  def __init__(self,obj):
    self.__dict__ = json.loads(obj)

class Server:
  def __init__(self,prefix=default_prefix,authority=default_authority,commands=default_commands,userIds=default_userIds):
    self.prefix = prefix
    self.authority = authority
    self.commands = commands
    self.userIds = userIds

def generate_user_id(serverObject, author):
  author = str(author.id)
  if author not in serverObject.userIds.keys():
    rand = random.randint(0000, 9999)
    while rand in serverObject.userIds.values():
      rand = random.randint(0000, 9999)
    serverObject.userIds[author] = rand

  return serverObject


def reset_user_id(serverObject, author):
  del serverObject.userIds[str(author.id)]
  serverObject = generate_user_id(serverObject, author)
  
  return serverObject


def change_user_id_to(serverObject, author, num):
  author = str(author.id)
  del serverObject.userIds[author]
  serverObject.userIds[author] = num

  return serverObject


def load_server(serverid):
    if "server" not in db.keys():
      db["server"] = {}
    if serverid not in db["server"].keys():
      db["server"][serverid] = json.dumps(Server().__dict__)

def update_server(serverid,serverObject):
  del db["server"][serverid]
  db["server"][serverid]=json.dumps(serverObject.__dict__)


def add_extra_digit(num):
    temp = ""
    for i in range(4 - len(str(num))):
        temp += "0"
    temp += str(num)
    return temp


def find_role(role, author):
    roles = map(str, author.roles)
    for i in roles:
        if role in i:
            return True
    return False
#Try changing boolean into int


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name="your confession"))


@client.event
async def on_message(message):
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name="your confession"))

    DM = False
    if str(message.channel) != "ngaku":
        if not str(message.channel).startswith("Direct Message"):
            return
        DM = True
    if message.author.bot:
        return

    msg = message.content
    atchs = message.attachments
    author = message.author
    serverid = str(message.channel.id)

    load_server(serverid)
    serverObject = Parser(db["server"][serverid])
    prefix = serverObject.prefix
    commands = serverObject.commands
    authority = serverObject.authority

    if str(author.id) not in serverObject.userIds.keys():
      serverObject = generate_user_id(serverObject, author)

    user_id = add_extra_digit(serverObject.userIds[str(author.id)])

    if msg.startswith(prefix):
        args = []
        try:
            args = str(msg).split()[1:]
        finally:
            try:
                if find_role(authority, author):
                    if msg.startswith(prefix + commands['purge_messages']):
                        await message.channel.purge()
                    elif msg.startswith(prefix + commands['change_user_ID']) and len(args) :
                        if 0 < int(args[0]) and int(args[0]) <= 9999 and int(args[0]) not in serverObject.userIds.values():
                            serverObject = change_user_id_to(serverObject,author, int(args[0]))
                    elif msg.startswith(prefix +
                                        commands['change_bot_prefix']):
                        serverObject.prefix=args[0]
                        update_server(serverid,serverObject)
                if msg.startswith(prefix + commands['reset_user_id']):
                    serverObject = reset_user_id(serverObject,author)
                    update_server(serverid,serverObject)
                elif msg.startswith(prefix + commands['commands_list']):
                    s = "```"
                    for command in commands:
                        s += f"{command} : {commands[command]}\n"
                    s += f"prefix : {prefix}```"
                    await message.channel.send(s)

            finally:
                try:
                    if not DM:
                      await message.delete()
                finally:
                    update_server(serverid, serverObject)
                    return

    try:
        if not DM:
          await message.delete()
    finally:
        update_server(serverid, serverObject)
        await message.channel.send(content=f"`<{user_id}>`: {msg}",
                                   reference=message.reference)
        for atch in atchs:
            await message.channel.send(atch)


client.run(os.getenv('TOKEN'))

# TODO:
#   CONFESS VIA DM
