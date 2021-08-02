import os
import discord
import data
from data import client
from data import recognized_channel

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


def load_data_objects(guildId, author):
    guildObject = data.load_guild_from_db(guildId)

    if str(author.id) not in guildObject.userIds.keys():
        guildObject.generate_user_id(author)

    userObject = data.load_user_from_db(str(author.id))
    userObject.update_from_guild(guildObject)

    return guildObject, userObject


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name="your confession"))


@client.event
async def on_message(message):
    if message.content == "clear_db()":
        data.clear_db()
        print("==DB CLEARED==")
        return

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
        userObject = data.load_user_from_db(str(author.id))
        default = False

        if not data.does_guild_exist(guildId):
          if userObject.default_guildId=="":
            await message.channel.send("Server tidak ditemukan!")
            return
          guildId = userObject.default_guildId
          default = True

        if not default:
            userObject.default_guildId = guildId
            userObject.update_user_to_db()

        channelTarget = data.get_channel(guildId)
        guildObjectTarget, userObject = load_data_objects(guildId, author)

        user_id = add_extra_digit(guildObjectTarget.userIds[str(author.id)])

        authmsg = msg[(len(guildId) + 1) * (not default):]

        await channelTarget.send(content=f"`<{user_id}>`: {authmsg}",
                                 reference=message.reference)
        for atch in atchs:
            await channelTarget.send(atch)

    else:
        guildId = str(message.guild.id)
        guildObject, userObject = load_data_objects(guildId, author)

        userObject.default_guildId = guildId
        userObject.update_user_to_db()

        prefix = guildObject.prefix
        commands = guildObject.commands
        authority = guildObject.authority

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
                        elif msg.startswith(prefix + commands['change_user_ID']
                                            ) and len(args):
                            if 0 < int(args[0]) and int(
                                    args[0]) <= 9999 and int(
                                        args[0]
                                    ) not in guildObject.userIds.values():
                                guildObject.change_user_id_to(
                                    author, int(args[0]))
                        elif msg.startswith(prefix +
                                            commands['change_bot_prefix']):
                            guildObject.prefix = args[0]
                            guildObject.update_guild_to_db()

                    if msg.startswith(prefix + commands['reset_user_id']):
                        guildObject.reset_user_id(author)
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
