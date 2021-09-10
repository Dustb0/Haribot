from jisho import JishoApi
from commands.cmd_translate import process_translate_quiz

# Each channel that's currently actively engaging with the bot gets its own
# Handler instance. Its responsible for parsing input and directing it to 
# the respective commands that contain the actual bot logic.
class Handler:
    
    def __init__(self, client):
        self.jishoApi = JishoApi()
        self.activeCommands = {}

    def process_message(self, message):
        # Check command
        if message.content.startswith('!translateQuiz'):
            channelName = message.content.replace('!translateQuiz', '').strip()
            process_translate_quiz(self.jishoApi, message, channelName)