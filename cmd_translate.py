from jisho import JishoApi
import random

async def command_translate(message, channel):
    list = await fill_quiz(channel)
    print(len(list) + " elements")
    sentence = random.choice(list)
    print(sentence)
    await message.channel.send(sentence)

async def fill_quiz(channel):
    list = []
    jishoApi = JishoApi()

    async for msg in channel.history():
        entry = msg.content.splitlines()

        # Add Japanese entries
        if len(entry) >= 2:
            jpWord = entry[0]
            sentence = jishoApi.getExampleSentence(jpWord)

            if sentence is not None:
                list.append(sentence[0] + " ||" + sentence[1] + "||")

    return list