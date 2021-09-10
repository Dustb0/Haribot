import os
import discord
from twitch_client_ex import TwitchClientEx
from handler import Handler

# Instantiate client
discordClient = discord.Client()
client = TwitchClientEx(discordClient)

# Each channel gets its own instance or "handler" 
handlers = {}

@discordClient.event
async def on_ready():
  print("Logged in")

@discordClient.event
async def on_message(message):
  global handlers
  global client

  # Ignore messages by bot itself
  if message.author == client.get().user:
    return

  # Check if the channel already has a handler assigned
  channelId = message.channel.id
  handler = handlers.get(channelId, None)

  if handler is None:
    handler = Handler(client)

  await handler.process_message(message)


client.get().run(os.environ['TOKEN'])