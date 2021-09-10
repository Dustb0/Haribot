import discord
import re
import time
import random
from base_quiz import BaseQuizHandler, QuizEntry         

class QuizHandler(BaseQuizHandler):

  def __init__(self, client):
    BaseQuizHandler.__init__(self, client)
    self.playercount = 0
    self.playerRespondedCount = 0
    self.dmMode = False

  def reset_quiz(self):
    self.quiz.clear()
    self.playercount = 0
    self.phase = 0

  async def set_next_entry(self, message):
    # Pick random entry
    self.currentEntry = None
    entryCount = len(self.quiz)
    selectedEntry = 0
    self.playerRespondedCount = 0

    if entryCount == 0:
      await self.end_quiz(message)
      return
      
    elif entryCount > 1:
      selectedEntry = random.randrange(0, entryCount - 1)

    # Assign entry
    self.currentEntry = self.quiz.pop(selectedEntry)

    # Display question
    await message.channel.send(self.get_ask_string())

  async def setup(self, message):
    self.reset_quiz()
    self.phase = 1
    await message.channel.send('**ゴルヅベアのクイズショウを始めましょう！** ' + self.client.random_emoji())

    # Check if we're in DM mode
    self.dmMode = type(message.channel) is discord.DMChannel
    if self.dmMode:
      self.phase = 2
      self.playercount = 1
      await message.channel.send("*どのチャンネル？?*")

    else:
      await message.channel.send('*何人ですか?*')

  async def handle_quiz(self, message):
    if self.phase == 1 and message.content.isnumeric():
      # Setting player count
      self.phase = 2
      self.playercount = int(message.content)
      await message.channel.send("*" + str(self.playercount) + ' :thumbsup: どのチャンネル?*')

    elif self.phase == 2:
      # Retrieve channel
      channel = self.client.get_channel(message.clean_content.replace('#', '').lower())      

      # Fill quiz
      if channel is not None:
        await self.fill_quiz(channel)

        # Start quiz
        if len(self.quiz) > 0:
          self.phase = 3
          await self.set_next_entry(message)      
            
    elif self.phase == 3:
      # Answering questions
      self.playerRespondedCount += 1

      # Check if response is correct
      if self.check_answer(message.content):
        await message.add_reaction("✅")
      else:
        await message.add_reaction("❌")

        # If we're in DM Mode, add the question again if it was wrong
        if self.dmMode:
          self.quiz.append(self.currentEntry)

      # Check if everyone answered
      if self.playerRespondedCount == self.playercount:
        await message.channel.send('**答え:** ' + self.currentEntry.solution)
        time.sleep(2)
        await self.set_next_entry(message)