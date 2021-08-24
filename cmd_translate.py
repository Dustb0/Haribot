from jisho import JishoApi
import random

async def command_translate(message, channel):
    sentence = random.choice(fill_quiz(channel))
    await message.channel.send(sentence)

async def fill_quiz(channel):
    list = []
    jishoApi = JishoApi()

    async for msg in channel.history():
        entry = msg.content.splitlines()

        # Add Japanese entries
        if len(entry) >= 2:
            jpWord = entry[0]
            sentence = await jishoApi.getExampleSentence(jpWord)

            if sentence is not None:
                list.append(sentence[0] + " ||" + sentence[1] + "||")

    return list