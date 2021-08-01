import os
import discord
import data
from data import client

from keep_alive import keep_alive
keep_alive()

recognized_channel = "ngaku"

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
    if str(message.channel) != recognized_channel:
        if not str(message.channel).startswith("Direct Message"):
            return
        DM = True
    if message.author.bot:
        return

    msg = message.content
    atchs = message.attachments
    author = message.author

    if DM:
      guildId = msg.split()[0]
      channelTarget = data.get_channel(guildId)
      guildObjectTarget = data.load_guild_from_db(guildId)

      if str(author.id) not in guildObjectTarget.userIds.keys():
        guildObjectTarget = data.generate_user_id(guildObjectTarget, author)

      user_id = add_extra_digit(guildObjectTarget.userIds[str(author.id)])

      authmsg = msg[len(guildId)+1:]

      await channelTarget.send(content=f"`<{user_id}>`: {authmsg}",reference=message.reference)
      for atch in atchs:
              await channelTarget.send(atch)

    else:
      guildId = str(message.guild.id)

      guildObject = data.load_guild_from_db(guildId)
      prefix = guildObject.prefix
      commands = guildObject.commands
      authority = guildObject.authority

      if str(author.id) not in guildObject.userIds.keys():
        guildObject = data.generate_user_id(guildObject, author)

      user_id = add_extra_digit(guildObject.userIds[str(author.id)])
      
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
                          if 0 < int(args[0]) and int(args[0]) <= 9999 and int(args[0]) not in guildObject.userIds.values():
                              guildObject = data.change_user_id_to(guildObject,author, int(args[0]))
                      elif msg.startswith(prefix +
                                          commands['change_bot_prefix']):
                          guildObject.prefix=args[0]
                  if msg.startswith(prefix + commands['reset_user_id']):
                      guildObject = data.reset_user_id(guildObject,author)
                  elif msg.startswith(prefix + commands['commands_list']):
                      s = "```"
                      for command in commands:
                          s += f"{command} : {commands[command]}\n"
                      s += f"prefix : {prefix}```"
                      await message.channel.send(s)

              finally:
                  try:
                      await message.delete()
                  finally:
                      return

      try:
          await message.delete()
      finally:
          await message.channel.send(content=f"`<{user_id}>`: {msg}",
                                    reference=message.reference)
          for atch in atchs:
              await message.channel.send(atch)


client.run(os.getenv('TOKEN'))

# TODO:
#   CONFESS VIA DM
