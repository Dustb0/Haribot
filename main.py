import os
import discord
from quiz import QuizHandler
from quiz_spotlight import SpotlightQuizHandler

client = discord.Client()
quizHandler = None

@client.event
async def on_ready():
  print("Logged in")

@client.event
async def on_message(message):
  global quizHandler

  if message.author == client.user:
    return

  # Quiz Handler
  if message.content.startswith('!q'):
    if quizHandler is None:
      quizHandler = QuizHandler(client)
      await quizHandler.setup(message)
    else:
      await quizHandler.end_quiz(message)
      quizHandler = None

  if message.content.startswith('!sq'):
    if quizHandler is None:
      quizHandler = SpotlightQuizHandler(client)
      await quizHandler.setup(message)
    else:
      await quizHandler.end_quiz(message)   

  elif quizHandler is not None and quizHandler.active():
    await quizHandler.handle_quiz(message)



client.run(os.environ['TOKEN'])