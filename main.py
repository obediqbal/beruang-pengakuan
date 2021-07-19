import os


from keep_alive import keep_alive
keep_alive()

import discord

client = discord.Client()

@client.event
async def on_message(message):
  if message.author.bot and message.channel=="ngaku":
    return

  msg = message.content;

  await message.channel.purge()

client.run(os.getenv('TOKEN'))