import random

class QuizEntry:
  def __init__(self, ask, solution):
    self.ask = ask
    self.solution = solution

class BaseQuizHandler:

  def __init__(self, client):
    self.quiz = []
    self.client = client
    self.currentEntry = None
    self.phase = 0

  def active(self):
    return self.phase > 0    

  def random_emoji(self):
    return str(random.choice(self.client.emojis))

  async def fill_quiz(self, channel):
    async for msg in channel.history():
      entry = msg.content.splitlines()
      
      if len(entry) >= 2:
        # Randomize asking 
        if bool(random.getrandbits(1)):
          self.quiz.append(QuizEntry(entry[0], entry[1]))
        else: 
          self.quiz.append(QuizEntry(entry[1], entry[0]))   

  def check_answer(self, answer):
    print(answer + " == " + self.currentEntry.solution)

    for solution in self.currentEntry.solution.split(","):
      if answer.lower().strip() == solution.lower().strip():
        return True

    return False    