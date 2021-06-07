import os
import discord
from quiz import QuizHandler

client = discord.Client()
quizHandler = QuizHandler(client)

@client.event
async def on_ready():
  print("Logged in")

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  # Quiz Handler
  if message.content.startswith('!q'):
    if quizHandler.active():
      await quizHandler.end_quiz(message)
    else:
      await quizHandler.setup(message)

  elif quizHandler.active():
    await quizHandler.handle_quiz(message)



client.run(os.environ['TOKEN'])