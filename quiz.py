import discord
import random
import re
import time

class QuizEntry:
  def __init__(self, ask, solution):
    self.ask = ask
    self.solution = solution

class QuizHandler:

  def __init__(self, client):
    self.playercount = 0
    self.playerRespondedCount = 0
    self.currentEntry = None
    self.quiz = []
    self.client = client
    self.phase = 0

  def active(self):
    return self.phase > 0

  def random_emoji(self):
    return str(random.choice(self.client.emojis))

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
    await message.channel.send(":question: **" + self.currentEntry.ask + "**")

  async def end_quiz(self, message):
      self.reset_quiz()
      await message.channel.send('**Das wars mit dem Quiz!** ' + self.random_emoji())

  async def setup(self, message):
    self.reset_quiz()
    self.phase = 1
    await message.channel.send('**Die Goldbär Quizshow beginnt!** ' + self.random_emoji())
    await message.channel.send('*Wie viele Mitspieler?*')

  async def handle_quiz(self, message):
    if message.content.startswith('!q'):
      await self.end_quiz(message)
        
    elif self.phase == 1 and message.content.isnumeric():
      # Setting player count
      self.phase = 2
      self.playercount = int(message.content)
      await message.channel.send("*" + str(self.playercount) + ' Spieler :thumbsup: Fragen aus welchem Kanal generieren?*')

    elif self.phase == 2:
      # Get channel name
      channelName = message.clean_content.replace('#', '').lower()

      # Retrieve channel
      for channel in message.channel.guild.channels:
        if str(channel.type) == 'text' and str(channel).lower() == channelName:
            print(channel)
            
            # Fill quiz
            async for msg in channel.history():
              entry = msg.content.splitlines()
              if len(entry) >= 2:

                # Randomize asking 
                if bool(random.getrandbits(1)):
                  self.quiz.append(QuizEntry(entry[0], entry[1]))
                else: 
                  self.quiz.append(QuizEntry(entry[1], entry[0]))

            if len(self.quiz) > 0:
              self.phase = 3
              await self.set_next_entry(message)

    elif self.phase == 3:
      # Answering questions
      self.playerRespondedCount += 1

      # Check if response is correct
      answer = re.escape(message.content)
      solution = re.escape(self.currentEntry.solution)
      print(answer + " == " + solution)
      if re.search(rf"\b{answer}\b", solution, re.IGNORECASE):
        await message.add_reaction("✅")
      else:
        await message.add_reaction("❌")

      # Check if everyone answered
      if self.playerRespondedCount == self.playercount:
        await message.channel.send('**Lösung:** ' + self.currentEntry.solution)
        time.sleep(2)
        await self.set_next_entry(message)