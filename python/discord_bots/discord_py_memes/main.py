from discord.ext import commands, tasks
from discord import (
    Intents
)

# Load configuration
from config import get_config

SETTINGS = get_config()

# Initialize Discord bot

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = "meme!",
            description = f"A simple Discord bot to generate you memes every {SETTINGS['INTERVAL']/3600} hour(s).",
            intents = Intents.default()
        )
        
        # Create threads to manage the bot
        
        self.MEME_TASKS = []
        
        self.create()
    
    def create(self):
        self.MEME_TASKS.append()