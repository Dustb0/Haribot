from jisho import JishoApi
from commands.cmd_translate import process_translate_quiz
from commands.cmd_quiz import CommandQuiz

# Each channel that's currently actively engaging with the bot gets its own
# Handler instance. Its responsible for parsing input and directing it to 
# the respective commands that contain the actual bot logic.
class Handler:
    
    def __init__(self, client):
        self.jishoApi = JishoApi()
        self.client = client
        self.activeCommand = None

    # Checks if the message contains a channel name. If not responds to the user
    async def verify_channel_name_arg(self, channelName, message):
        if len(channelName) == 0:
            await message.channel.send(':point_up:' + self.client.random_emoji() + ' <( チャネルを書いてください! )')
            return False

        return True

    async def process_message(self, message):
        # Check command
        if message.content.startswith('!translateQuiz'):
            # Example sentence translation 
            channelName = message.content.replace('!translateQuiz', '').strip()

            if await self.verify_channel_name_arg(channelName, message):
                channel = self.client.get_channel(channelName)
                await process_translate_quiz(self.jishoApi, self.client, message, channel)

        if message.content.startswith('!quiz'):
            # Quiz
            if self.activeCommand is None:
                self.activeCommand = await self.instantiate_quiz(message)

            else:
                await self.end_current_command()

        elif self.activeCommand is not None:
            # There's an active command that processes all input
            await self.activeCommand.process_message(message)

            # Check if we're at the end
            if not self.activeCommand.is_active():
                self.end_current_command()
    
    async def end_current_command(self):
        await self.activeCommand.end()
        self.activeCommand = None

    async def instantiate_quiz(self, message):
        params = message.content.strip().split()
        channelName = params[1] if len(params) > 1 else ''

        # Instantiate quiz command
        if await self.verify_channel_name_arg(channelName, message):
            channel = self.client.get_channel(channelName)
            players = params[2] if len(params) > 2 and self.client.is_dm_channel(channel) else 1
            
            quiz = CommandQuiz(self.client, self.jishoApi, message.channel, players)
            await quiz.load(channel)
            return quiz
