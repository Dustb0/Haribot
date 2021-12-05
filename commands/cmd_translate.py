import random

from api.quizlet import QuizletApi

# Provides a random example sentence from Jisho + its translation
async def process_translate_quiz(jishoApi, client, message, quizletUrl):
    sentence = get_sentence(jishoApi, quizletUrl)
    await message.channel.send(client.random_emoji() + ':point_down: <( 訳してください )\n\n' + sentence)
    
def get_sentence(jishoApi, quizletUrl):
    quizlet = QuizletApi()
    list = quizlet.get_vocabulary(quizletUrl)
    random.shuffle(list)

    for entry in list:
        jpWord = entry[0]
        sentence = jishoApi.get_example_sentence(jpWord)
        if sentence is not None and len(sentence) == 2:
            return sentence[0] + "     ||" + sentence[1] + "||"