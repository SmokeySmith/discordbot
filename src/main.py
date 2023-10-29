from DiscordEvent import discordBotEvent
import os
from pathlib import Path
from dotenv import load_dotenv
from DiscordCommand import discordBotCommands

env_path = Path('.') / ".env"
load_dotenv(dotenv_path=env_path)
#TODO expand the inventory to allow more details
#TODO add the standard 5e material for adding items to the bag
#TODO logging of the most recent 1000 requests no user info saved
#TODO logging of every recorded error
if __name__ == "__main__":
    mode = os.environ["DISCORD_MODE"]
    if mode == "EVENT":
        discordBotEvent()
    elif mode == "COMMAND": 
        discordBotCommands()
    pass