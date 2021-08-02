import random
import json
import discord
from utils import Parser
from replit import db

client = discord.Client()

recognized_channel = "ngaku"

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

def clear_db():
  db.clear()

class Server:
  def __init__(self,gid,prefix=default_prefix,authority=default_authority,commands=default_commands,userIds=default_userIds):
    self.id = gid
    self.prefix = prefix
    self.authority = authority
    self.commands = commands
    self.userIds = userIds

  def generate_user_id(self, author):
    if str(author.id) not in self.userIds.keys():
      rand = random.randint(0000, 9999)
      while rand in self.userIds.values():
        rand = random.randint(0000, 9999)
      self.userIds[str(author.id)] = rand

    self.update_guild_to_db()


  def reset_user_id(self, author):
    del self.userIds[str(author.id)]
    self.generate_user_id(author)
    

  def change_user_id_to(self, author, num):
    del self.userIds[str(author.id)]
    self.userIds[str(author.id)] = num

    self.update_guild_to_db()

  
  def update_guild_to_db(self):
    guildId = self.id
    del db["guild"][guildId]
    db["guild"][guildId] = json.dumps(self.__dict__)
    

class User:
  def __init__(self,uid,guildIds={},default_guildId=""):
    self.id = uid
    self.guildIds = guildIds
    self.default_guildId=default_guildId

  def update_user_to_db(self):
    del db["user"][self.id]
    db["user"][self.id] = json.dumps(self.__dict__)

  def update_from_guild(self,guildObject):
    if str(guildObject.id) not in self.guildIds.keys():
      self.guildIds[str(guildObject.id)] = {}

    self.guildIds[str(guildObject.id)]["userid"] = guildObject.userIds[str(self.id)]

    self.update_user_to_db()


def load_guild_from_db(guildId):
    if "guild" not in db.keys():
      db["guild"] = {}
    if guildId not in db["guild"].keys():
      db["guild"][guildId] = json.dumps(Server(guildId).__dict__)

    return Server(*Parser(db["guild"][guildId]).__dict__.values())


def load_user_from_db(userId):
  if "user" not in db.keys():
    db["user"] = {}
  if userId not in db["user"].keys():
    db["user"][userId] = json.dumps(User(userId).__dict__)

  return User(*Parser(db["user"][userId]).__dict__.values())


def get_guild(id):
  return client.get_guild(int(id))


def get_channel(id, channelName = "ngaku"):
  guild = get_guild(id)
  for channel in guild.channels:
    if channel.name==channelName:
      return channel


def does_guild_exist(guildId):
  if "guild" not in db.keys():
    return False
  elif guildId not in db["guild"].keys():
    return False
  return True


def is_guildId_valid(id):
  if len(id)==18 and id.isnumeric():
    return True
  return False
