import discord
import re
import time
import random
from base_quiz import BaseQuizHandler, QuizEntry         

class SpotlightQuizHandler(BaseQuizHandler):

  def __init__(self, client):
    BaseQuizHandler.__init__(self, client)
    self.playercount = 0
    self.dmMode = False
    self.players = []
    self.currentPlayer = ""
    self.health = 3

  def reset_quiz(self):
    self.quiz.clear()
    self.phase = 0
    self.players.clear()
    self.currentPlayer = ""
    self.health = 3

  async def set_next_entry(self, message):
    # Pick random entry
    self.currentEntry = None
    entryCount = len(self.quiz)
    selectedEntry = 0
    self.currentPlayer = ""

    if entryCount == 0:
      await self.end_quiz(message)
      return
      
    elif entryCount > 1:
      selectedEntry = random.randrange(0, entryCount - 1)

    # Assign entry
    self.currentEntry = self.quiz.pop(selectedEntry)

    # Assign player
    self.currentPlayer = random.choice(self.players)

    # Display question
    await message.channel.send(":question: " + self.currentPlayer + "**: "  + self.currentEntry.ask + "**")

  async def end_quiz(self, message):
      self.reset_quiz()
      await message.channel.send('**Das wars mit dem Quiz!** ' + self.random_emoji())

  async def setup(self, message):
    self.reset_quiz()
    self.phase = 1
    await message.channel.send('**Die Goldbär Quizshow :cloud_lightning: SPOTLIGHT-EDITION :cloud_lightning: beginnt!** ' + self.random_emoji())
    await message.channel.send('*Wie viele Mitspieler?*')

  def retrieve_quiz_source(self, message, channelName):
    for guild in self.client.guilds:
      for channel in guild.channels:
        if str(channel.type) == 'text' and str(channel).lower() == channelName:
          return channel

  async def write_health(self, message):
    emojis = ""
    for index in range(3):
      if index >= self.health:
        emojis += ":black_heart: "
      else:
        emojis += ":heart: "
    await message.channel.send("**HP:" + emojis + "**")

  async def handle_quiz(self, message):
    if self.phase == 1 and message.content.isnumeric():
      # Setting player count
      self.phase = 2
      self.playercount = int(message.content)
      await message.channel.send("*" + str(self.playercount) + ' Spieler :thumbsup: Antworte auf diese Nachricht um mitzuspielen!*')

    elif self.phase == 2:
      # Retrieve names
      if not message.author.name in self.players:
        self.players.append(message.author.name)
        await message.channel.send("*" + message.author.name + ' spielt mit!*')

        if len(self.players) == self.playercount:
          await message.channel.send("**Fragen aus welchem Kanal generieren?**")
          self.phase = 3

    elif self.phase == 3:
      # Retrieve channel
      channel = self.retrieve_quiz_source(message, message.clean_content.replace('#', '').lower())      

      # Fill quiz
      if channel is not None:
        await self.fill_quiz(channel)

        # Start quiz
        if len(self.quiz) > 0:
          self.phase = 4
          await self.write_health(message)
          await self.set_next_entry(message)      
            
    elif self.phase == 4 and message.author.name == self.currentPlayer:
      # Check if response is correct
      if self.check_answer(message.content):
        await message.add_reaction("✅")
      else:
        await message.add_reaction("❌")
        self.health -= 1
        await self.write_health(message)

      await message.channel.send('**Lösung:** ' + self.currentEntry.solution)
      time.sleep(2)

      # Check if still alive
      if self.health > 0:
        await self.set_next_entry(message)
      else:
        await message.channel.send(':boom::boom: **GAME OVER!** :boom::boom:')
        await self.end_quiz(message)
        
