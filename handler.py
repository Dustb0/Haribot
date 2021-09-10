from jisho import JishoApi
from commands.cmd_translate import process_translate_quiz

class Handler:
    
    def __init__(self, client):
        self.jishoApi = JishoApi()
        self.activeCommands = {}

    def process_message(self, message):
        # Check command
        if message.content.startswith('!translateQuiz'):
            process_translate_quiz(self.jishoApi, message)