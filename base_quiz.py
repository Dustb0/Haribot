import random

from jisho import JishoApi

class QuizEntry:
  def __init__(self, ask, solution, flipped):
    self.ask = ask
    self.solution = solution
    self.flipped = flipped

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
      await message.channel.send('**Das wars mit dem Quiz!** ' + self.client.random_emoji())

  def get_ask_string(self):
    ask = ""
    answerLang = ""
    audioFile = ""

    # Check in which language the solution should be in 
    if self.currentEntry.flipped:
      audioFile = self.jishoApi.getAudioFile(self.currentEntry.solution)
      answerLang = ":flag_jp:"
    
    else:
      audioFile = self.jishoApi.getAudioFile(self.currentEntry.ask)
      answerLang = ":flag_de:"

    # If audio file is present only ask for a listening questions half of the time
    if len(audioFile) > 0 and bool(random.getrandbits(1)):
      audioFile = ""

    # Check if audio file is present
    if len(audioFile) > 0:
      ask = "**" + audioFile + "** antworte auf " + answerLang
    else:
      ask = "**" + self.currentEntry.ask + "**"

    return ":question: " + ask

  async def fill_quiz(self, channel):
    async for msg in channel.history():
      entry = msg.content.splitlines()
      
      if len(entry) >= 2:
        jpWord = entry[0]
        deWord = entry[1]

        # Randomize asking 
        if bool(random.getrandbits(1)):
          self.quiz.append(QuizEntry(jpWord, deWord, False))
        else: 
          self.quiz.append(QuizEntry(deWord, jpWord, True))   

  def check_answer(self, answer):
    print(answer + " == " + self.currentEntry.solution)

    for solution in self.currentEntry.solution.split(","):
      if answer.lower().strip() == solution.lower().strip():
        return True

    return False    