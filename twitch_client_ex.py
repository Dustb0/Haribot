import random

# Wrapper for the Twitch client with advanced functionality
class TwitchClientEx:

    def __init__(self, client):
        self.client = client

    # Retrieve a channel object by a channel name
    def get_channel(self, channelName):
        for guild in self.client.guilds:
            for channel in guild.channels:
                if str(channel.type) == 'text' and str(channel).lower() == channelName:
                    return channel

    # Returns a list of tuples containing 
    async def get_vocabulary(self, channel):
        list = []
        async for msg in channel.history():
            entry = msg.content.splitlines()
            # Add Japanese entries
            if len(entry) >= 2:
                jpWord = entry[0]
                deWord = entry[1]
                list.append((jpWord, deWord))

        return list

    # Get random emoji from the server's emojis
    def random_emoji(self):
        return str(random.choice(self.client.emojis))

    def get(self):
        return self.client