from jisho import JishoApi
import random

async def command_translate(message, channel):
    sentence = await get_sentence(channel)
    print(sentence)
    await message.channel.send(sentence)

async def get_sentence(channel):
    list = []
    jishoApi = JishoApi()

    async for msg in channel.history():
        entry = msg.content.splitlines()

        # Add Japanese entries
        if len(entry) >= 2:
            list.append(entry[0])

    # Get random entries until we get one with an example sentence
    while True:
        jpWord = random.choice(list)
        sentence = jishoApi.getExampleSentence(jpWord)

        if sentence is not None and len(sentence) == 2:
            list.append(sentence[0] + " ||" + sentence[1] + "||")