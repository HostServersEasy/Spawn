def get_config():return({
    
    # ALter the settings below ONLY.
    
    "SERVER": 0x0000000000000000, # Your server ID.
    "MEMES_CHANNEL": { 
        # Use the name of the channel:
        # 'name': '...'
        # OR use the ID of the channel:
        # 'id': 0
        
        'id': 0x0000000000000000,
        'name': 'memes'
        # Remove the identify method you don't want to use above.
    },
    "API": {
        "ENDPOINT": "https://memeapi.zachl.tech/pic/json" # Modify this if you want to use your own API for memes instead.
    },
    "INTERVAL": 3600, # Interval in seconds the bot will send memes requests to the API. Could get you rate limited if done too frequently.
    "TOKEN": "", # Keep safe and secure! Do not share this token with others you don't trust at ALL!
    
    # Alter the settings above ONLY.
    
})