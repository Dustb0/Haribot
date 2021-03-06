from random import random
import random
from random import sample
from api.image_search import ImageSearch
from api.jisho import JishoApi
from api.quizlet import QuizletApi
from commands.cmd_translate import get_example_sentence
from commands.conjugation_strings import CONJUGATION_STRINGS

async def daily_quiz(client, quizfile, channelName):
  # Load vocab
  quizlet = QuizletApi()
  vocab = quizlet.load_cache(quizfile)
  random.shuffle(vocab)  
  
  jisho = JishoApi()
  imageSearch = ImageSearch()

  # Get quiz channel
  channel = client.get_channel(channelName)

  questionType = random.randint(0, 100)

  if questionType >= 0 and questionType <= 20:
    quizText = quiz_reading(vocab, jisho)
  
  elif questionType >= 21 and questionType <= 50:
    quizText = await image_guess(vocab, imageSearch)
  
  elif questionType >= 51 and questionType <= 80:
    quizText = conjugation_quiz(vocab, jisho)
  
  elif questionType >= 81 and questionType <= 91:
    quizText = audio_guess(vocab, jisho)
  
  else:
    quizText = example_sentence(vocab, jisho)

  # Title
  titleText = ':information_source: **Goldbär Quiz Time**\n\n'

  # Send message
  await channel.send(titleText + client.get_random_hand_emoji() + client.random_emoji() + ' ' + quizText)


def quiz_reading(vocab, jisho):
  question = '**Wie ist die Lesung der folgenden Wörter?**\n'
  entries = sample(vocab, 3)

  for entry in entries:
    reading = jisho.get_reading(entry[0])
    question += '- **' + entry[0] + '** (' + entry[1] + ')  ||' + reading + '||\n'

  return question

async def image_guess(vocab, imageSearch):
  entries = sample(vocab, 3)
  question = '**Welches Wort passt zu dem Bild?**\n'

  # Add choices
  question += ':a: ' + entries[0][0] + '\n:b: ' + entries[1][0] + '\n:regional_indicator_c: ' + entries[2][0] + '\n'

  # Pick answer
  answer = random.choice(entries)
  question += 'Lösung: ||' + answer[0] + ' (' + answer[1] + ')||\n'

  # Get question
  searchTerm = answer[0].split(',')[0]
  print(searchTerm)
  image = await imageSearch.get_image(searchTerm)
  question += image

  return question

def conjugation_quiz(vocab, jisho):
  question = ''

  # Find an entry with conjugation
  conjugations = {}
  for entry in vocab:
    conjugations = jisho.get_conjugations(entry[0])

    # Maybe check if it's an adjective
    if len(conjugations) == 0:
      conjugations = jisho.get_declensions(entry[0])

    # If no conjugations found, continue
    if len(conjugations) == 0:
      continue
    else:
      question = 'Konjugiere **' + entry[0] + '** (' + entry[1] + ') zu **'
      break

  # Get conjugation
  conjugationKey = random.choice(list(conjugations))
  question += CONJUGATION_STRINGS[conjugationKey] + '**\n'
  question += 'Lösung: ||' + conjugations[conjugationKey] + '||'

  return question
  
def example_sentence(vocab, jisho):
  question = '**Übersetze folgenden Beispielsatz:**\n'
  return question + get_example_sentence(vocab, jisho)

def audio_guess(vocab, jisho):
  audioFile = None
  answer = None

  for entry in vocab:
    answer = entry
    audioFile = jisho.get_audio_file(answer[0])

    if len(audioFile) > 0:
      break

  question = '**Welches Wort wird hier gesprochen?**\n' + audioFile + '\n'
  question += 'Lösung: ||' + answer[0] + ' (' + answer[1] + ') ||'
  return question