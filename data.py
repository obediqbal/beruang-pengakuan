import random
import json
import discord
from utils import Parser
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


class User:
  def __init__(self,id,guildIds={},default_guildId=""):
    self.id = id
    self.guildIds = guildIds
    self.default_guildId=default_guildId


def generate_user_id(guildObject, author):
  author = str(author.id)
  if author not in guildObject.userIds.keys():
    rand = random.randint(0000, 9999)
    while rand in guildObject.userIds.values():
      rand = random.randint(0000, 9999)
    guildObject.userIds[author] = rand

  update_guild_to_db(guildObject)

  return guildObject


def reset_user_id(guildObject, author):
  del guildObject.userIds[str(author.id)]
  guildObject = generate_user_id(guildObject, author)
  
  update_guild_to_db(guildObject)

  return guildObject


def change_user_id_to(guildObject, author, num):
  author = str(author.id)
  del guildObject.userIds[author]
  guildObject.userIds[author] = num

  update_guild_to_db(guildObject)
  
  return guildObject


def load_guild_from_db(guildId):
    if "guild" not in db.keys():
      db["guild"] = {}
    if guildId not in db["guild"].keys():
      db["guild"][guildId] = json.dumps(Server(guildId).__dict__)

    return Parser(db["guild"][guildId])


def load_user_from_db(userid):
  if "user" not in db.keys():
    db["user"] = {}
  if userid not in db["user"].keys():
    db["user"][userid] = json.dumps(User(userid))

  return Parser(db["user"][userid])


def update_guild_to_db(guildObject):
  guildId = guildObject.id
  del db["guild"][guildId]
  db["guild"][guildId] = json.dumps(guildObject.__dict__)


def update_user_to_db(userId,userObject):
  del db["user"][userId]
  db["user"][userId] = json.dumps(userObject.__dict__)


def get_guild(id):
  return client.get_guild(int(id))


def get_channel(id, channelName = "ngaku"):
  guild = get_guild(id)
  for channel in guild.channels:
    if channel.name==channelName:
      return channel


