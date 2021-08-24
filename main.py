import os
import discord
from quiz import QuizHandler
from quiz_spotlight import SpotlightQuizHandler

client = discord.Client()
handlers = {}

@client.event
async def on_ready():
  print("Logged in")

@client.event
async def on_message(message):
  global handlers

  if message.author == client.user:
    return

  # Retrieve channel-scoped quiz handler
  channelId = message.channel.id
  quizHandler = handlers.get(channelId, None)

  if message.content.startswith('!q'):
    if quizHandler is None:
      # Create quiz and add to scope
      quizHandler = QuizHandler(client)
      handlers[channelId] = quizHandler
      await quizHandler.setup(message)

    else:
      await endHandler(quizHandler, channelId, message)

  if message.content.startswith('!sq'):
    if quizHandler is None:
      # Create quiz and add to scope
      quizHandler = SpotlightQuizHandler(client)
      handlers[channelId] = quizHandler
      await quizHandler.setup(message)

    else:
      await endHandler(quizHandler, channelId, message)

  elif quizHandler is not None and quizHandler.active():
    await quizHandler.handle_quiz(message)

    # Check if handler just handled the last message
    if not quizHandler.active():
      await endHandler(quizHandler, channelId, message)

async def endHandler(quizHandler, channelId, message):
  await quizHandler.end_quiz(message)
  handlers.pop(channelId)
  quizHandler = None


client.run(os.environ['TOKEN'])