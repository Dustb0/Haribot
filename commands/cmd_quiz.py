import random
from api.jisho import Conjugations

CONJUGATION_STRINGS = {
    Conjugations.PLAIN_NONPAST: '[Non-Keigo] Nonpast +',
    Conjugations.PLAIN_NEGATIVE: '[Non-Keigo] Nonpast -',
    Conjugations.PLAIN_PAST: '[Non-Keigo] Past +',
    Conjugations.PLAIN_PAST_NEGATIVE: '[Non-Keigo] Past -',
    Conjugations.PLAIN_TE: '[Non-Keigo] Te-Form',
    Conjugations.PLAIN_TAI: '[Non-Keigo] Tai-Form',
    Conjugations.KEIGO_NONPAST: '[Keigo] Nonpast +',
    Conjugations.KEIGO_NEGATIVE: '[Keigo] Nonpast -',
    Conjugations.KEIGO_PAST: '[Keigo] Past +',
    Conjugations.KEIGO_PAST_NEGATIVE: '[Keigo] Past -',
    Conjugations.KEIGO_TE: '[Keigo] Te-Form',
    Conjugations.KEIGO_TAI: '[Keigo] Tai-Form'
}

class CommandQuiz():

    def __init__(self, client, jishoApi, quizChannel, playerCount, presetQuestion):
        self.client = client
        self.jishoApi = jishoApi
        self.playerCount = playerCount
        self.quizChannel = quizChannel
        self.currentAnswer = ""
        self.playerRespondedCount = 0
        self.presetQuestionType = presetQuestion

    async def load(self, sourceChannel):
        self.list = await self.client.get_vocabulary(sourceChannel, True)
        await self.setup_next_question()

    async def end(self):
        await self.quizChannel.send(":wave:" + self.client.random_emoji() + " <( クイズが仕舞った。またね！ )")

    async def setup_next_question(self):
        # Reset
        questionMessage = ""
        self.playerRespondedCount = 0

        # Decide which question type we go for
        if self.presetQuestionType == -1:
            questionType = random.randint(0, 2)
        else:
            questionType = self.presetQuestionType

        print("questionType: " + str(questionType))

        # Loop until we found a question
        while True:
            # Assign entry
            currentEntry = self.list.pop(0)

            # Audio
            if questionType == 0:
                # Check if entry has an audio file
                audioFile = self.jishoApi.get_audio_file(currentEntry[0])

                if len(audioFile) > 0:
                    self.currentAnswer = currentEntry[1]
                    questionMessage = self.client.random_emoji() + " <( 聞いて訳してください )\n" + audioFile + "\n||" + currentEntry[0] + "||"

            # Verb-Conjugation 
            if questionType == 1 and questionMessage == "":
                # Check if it's a verb with conjugations we could ask for
                conjugations = self.jishoApi.get_conjugations(currentEntry[0])

                if len(conjugations) > 0:
                    # Determine a random conjugation
                    conjugationKey = random.choice(list(Conjugations))
                    self.currentAnswer = conjugations[conjugationKey]
                    print(CONJUGATION_STRINGS[conjugationKey] + ": " + self.currentAnswer)
                    questionMessage = ":exclamation: " + currentEntry[1] + " in **" + CONJUGATION_STRINGS[conjugationKey] + "**"

            # Normal question
            if questionType == 2 and questionMessage == "":
                # Decide if we're asking for Japanese or German
                if bool(random.getrandbits(1)):
                    # Japanese -> German
                    self.currentAnswer = currentEntry[1]
                    questionMessage = ":question: " + currentEntry[0]
                else:
                    # German -> Japanese
                    self.currentAnswer = currentEntry[0]
                    questionMessage = ":question: " + currentEntry[1]

            # If we found a question, stop
            if questionMessage != "":
                break;


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
        if self.playerRespondedCount == self.playerCount:
            await self.quizChannel.send('答え:  ** ' + self.currentAnswer + '**')

            # Check if the quiz is finished
            if not self.is_active():
                await self.end()

            else:
                await self.setup_next_question()

