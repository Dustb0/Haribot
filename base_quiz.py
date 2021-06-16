import random

from jisho import JishoApi

class QuizEntry:
  def __init__(self, ask, solution, audioFile, answerLang):
    self.ask = ask
    self.solution = solution
    self.audioFile = audioFile
    self.answerLang = answerLang

class BaseQuizHandler:

  def __init__(self, client):
    self.quiz = []
    self.client = client
    self.currentEntry = None
    self.phase = 0
    self.jishoApi = JishoApi()

  def active(self):
    return self.phase > 0

  async def end_quiz(self, message):
      self.reset_quiz()
      await message.channel.send('**Das wars mit dem Quiz!** ' + self.random_emoji())      

  def random_emoji(self):
    return str(random.choice(self.client.emojis))

  def get_ask_string(self):
    return ":question: **" + self.currentEntry.ask + "**"

  async def fill_quiz(self, channel):
    async for msg in channel.history():
      entry = msg.content.splitlines()
      
      if len(entry) >= 2:
        jpWord = entry[0]
        deWord = entry[1]
        audio = self.jishoApi.getAudioFile(jpWord)

        # Randomize asking 
        if bool(random.getrandbits(1)):
          self.quiz.append(QuizEntry(jpWord, deWord, audio, ":flag_de:"))
        else: 
          self.quiz.append(QuizEntry(deWord, jpWord, audio, ":flag_jp:"))   

  def check_answer(self, answer):
    print(answer + " == " + self.currentEntry.solution)

    for solution in self.currentEntry.solution.split(","):
      if answer.lower().strip() == solution.lower().strip():
        return True

    return False    