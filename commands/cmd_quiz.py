import random

class CommandQuiz():

    def __init__(self, client, jishoApi, quizChannel, playerCount):
        self.client = client
        self.jishoApi = jishoApi
        self.playerCount = playerCount
        self.quizChannel = quizChannel
        self.currentAnswer = ""
        self.playerRespondedCount = 0

    async def load(self, sourceChannel):
        self.list = await self.client.get_vocabulary(sourceChannel, True)
        await self.setup_next_question()

    async def end(self):
        await self.quizChannel.send(":wave:" + self.client.random_emoji() + " <( クイズが仕舞った。またね！ )")

    async def setup_next_question(self):
        # Assign entry
        currentEntry = self.list.pop(0)
        questionMessage = ""
        self.playerRespondedCount = 0

        # Check if entry has an audio file
        audioFile = self.jishoApi.get_audio_file(currentEntry[0])

        # Words with an audio are the preferred question type.
        # If audio exists chose this question type 50% of the time
        if len(audioFile) > 0 and bool(random.getrandbits(1)):
            self.currentAnswer = currentEntry[1]
            questionMessage = self.client.random_emoji() + " <( 聞いて訳してください )\n" + audioFile

        else:
            # Decide if we're asking for Japanese or German
            if bool(random.getrandbits(1)):
                # Japanese -> German
                self.currentAnswer = currentEntry[1]
                questionMessage = ":question: " + currentEntry[0]
            else:
                # German -> Japanese
                self.currentAnswer = currentEntry[0]
                questionMessage = ":question: " + currentEntry[1]

        # Write out message
        await self.quizChannel.send(questionMessage)

    def check_answer(self, answer):
        print(answer + " == " + self.currentAnswer)

        for solution in self.currentAnswer.split(","):
            if answer.lower().strip() == solution.lower().strip():
                return True

        return False  
    
    def is_active(self):
        # Check if there are still questions and if we're on the last question
        # check if everyone replied
        return len(self.list) > 0 or self.playerRespondedCount < self.playerCount

    async def process_message(self, message):
        self.playerRespondedCount += 1

        # Check if response is correct
        if self.check_answer(message.content):
            await message.add_reaction("✅")
        else:
            await message.add_reaction("❌")

        # Check if everyone answered
        print("playerCount: " + str(self.playerCount))
        print("playerRespondedCount: " + str(self.playerRespondedCount))
        print("end?" + str(self.playerRespondedCount == self.playerCount))
        if self.playerRespondedCount == self.playerCount:
            await self.quizChannel.send('答え:  ** ' + self.currentAnswer + '**')

            # Check if the quiz is finished
            if not self.is_active():
                await self.end()

            else:
                await self.setup_next_question()

