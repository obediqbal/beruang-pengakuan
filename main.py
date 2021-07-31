import os
import discord
from replit import db
import utils
import data
from data import client

from keep_alive import keep_alive
keep_alive()

def add_extra_digit(num):
    temp = ""
    for i in range(4 - len(str(num))):
        temp += "0"
    temp += str(num)
    return temp


def has_role(role, author):
    roles = map(str, author.roles)
    for i in roles:
        if role in i:
            return True
    return False


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

    if DM:
      serverid = msg.split()[0]
      channel = data.get_channel(serverid)
      serverObject = utils.Parser(db["server"][serverid])

      if str(author.id) not in serverObject.userIds.keys():
        serverObject = data.generate_user_id(serverObject, author)

      user_id = add_extra_digit(serverObject.userIds[str(author.id)])

      authmsg = msg[len(serverid)+1:]

      data.update_server(serverid,serverObject)

      await channel.send(content=f"`<{user_id}>`: {authmsg}",reference=message.reference)
      for atch in atchs:
              await channel.send(atch)

    else:
      serverid = str(message.guild.id)

      data.load_server(serverid)
      serverObject = utils.Parser(db["server"][serverid])
      prefix = serverObject.prefix
      commands = serverObject.commands
      authority = serverObject.authority

      if str(author.id) not in serverObject.userIds.keys():
        serverObject = data.generate_user_id(serverObject, author)

      user_id = add_extra_digit(serverObject.userIds[str(author.id)])
      
      if msg.startswith(prefix):
          args = []
          try:
              args = str(msg).split()[1:]
          finally:
              try:
                  if has_role(authority, author):
                      if msg.startswith(prefix + commands['purge_messages']):
                          await message.channel.purge()
                      elif msg.startswith(prefix + commands['change_user_ID']) and len(args) :
                          if 0 < int(args[0]) and int(args[0]) <= 9999 and int(args[0]) not in serverObject.userIds.values():
                              serverObject = data.change_user_id_to(serverObject,author, int(args[0]))
                      elif msg.startswith(prefix +
                                          commands['change_bot_prefix']):
                          serverObject.prefix=args[0]
                          data.update_server(serverid,serverObject)
                  if msg.startswith(prefix + commands['reset_user_id']):
                      serverObject = data.reset_user_id(serverObject,author)
                      data.update_server(serverid,serverObject)
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
                      data.update_server(serverid, serverObject)
                      return

      try:
          await message.delete()
      finally:
          data.update_server(serverid, serverObject)
          await message.channel.send(content=f"`<{user_id}>`: {msg}",
                                    reference=message.reference)
          for atch in atchs:
              await message.channel.send(atch)


client.run(os.getenv('TOKEN'))

# TODO:
#   CONFESS VIA DM
