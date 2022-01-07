import os
import discord
from commands.quiz_job import daily_quiz
from discord.ext import tasks, commands
from api.twitch_client_ex import TwitchClientEx
from handler import Handler

# Instantiate client
discordClient = discord.Client()
client = TwitchClientEx(discordClient)

# Each channel gets its own instance or "handler" 
handlers = {}

@discordClient.event
async def on_ready():
  print("Logged in")
  daily_quiz_job.start()

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
    handlers[channelId] = handler

  await handler.process_message(message)

@tasks.loop(hours=48)
async def daily_quiz_job():
  await daily_quiz(client, 'manu', 'quiz2')

client.get().run(os.environ['TOKEN'])