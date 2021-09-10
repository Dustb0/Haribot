import random

# Provides a random example sentence from Jisho + its translation
async def process_translate_quiz(jishoApi, client, message, channel):
    sentence = await get_sentence(jishoApi, client, channel)
    await message.channel.send(client.random_emoji() + ':point_down: <( 訳してください )\n\n' + sentence)
    
async def get_sentence(jishoApi, client, channel):
    list = await client.get_vocabulary(channel, True)

    for entry in list:
        jpWord = entry[0]
        sentence = jishoApi.getExampleSentence(jpWord)
        if sentence is not None and len(sentence) == 2:
            return sentence[0] + "     ||" + sentence[1] + "||"