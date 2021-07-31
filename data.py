import random
import json
import discord
from replit import db

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

class Server:
  def __init__(self,id,prefix=default_prefix,authority=default_authority,commands=default_commands,userIds=default_userIds):
    self.id = id
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
      db["server"][serverid] = json.dumps(Server(serverid).__dict__)

def update_server(serverid,serverObject):
  del db["server"][serverid]
  db["server"][serverid]=json.dumps(serverObject.__dict__)

def get_guild(id):
  return client.get_guild(int(id))

def get_channel(id, channelName = "ngaku"):
  guild = get_guild(id)
  for channel in guild.channels:
    if channel.name==channelName:
      return channel
