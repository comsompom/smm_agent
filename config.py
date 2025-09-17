import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Telegram Configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
    
    # Discord Configuration
    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
    
    # Facebook Configuration
    FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')
    FACEBOOK_GROUP_ID = os.getenv('FACEBOOK_GROUP_ID')
    
    # X (Twitter) Configuration
    X_API_KEY = os.getenv('X_API_KEY')
    X_API_SECRET = os.getenv('X_API_SECRET')
    X_ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
    X_ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET')
    X_BEARER_TOKEN = os.getenv('X_BEARER_TOKEN')
    
    # NASA APOD Configuration
    NASA_API_KEY = os.getenv('NASA_API_KEY')
    
    # General Configuration
    POST_DELAY = int(os.getenv('POST_DELAY', '5'))  # Delay between posts in seconds
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    
    @classmethod
    def validate_config(cls):
        """Validate that all required configuration is present"""
        required_configs = {
            'Telegram': [cls.TELEGRAM_BOT_TOKEN, cls.TELEGRAM_CHANNEL_ID],
            'Discord': [cls.DISCORD_BOT_TOKEN, cls.DISCORD_CHANNEL_ID],
            'Facebook': [cls.FACEBOOK_ACCESS_TOKEN, cls.FACEBOOK_GROUP_ID],
            'X': [cls.X_API_KEY, cls.X_API_SECRET, cls.X_ACCESS_TOKEN, cls.X_ACCESS_TOKEN_SECRET]
        }
        
        missing_configs = []
        for platform, configs in required_configs.items():
            if not all(configs):
                missing_configs.append(platform)
        
        return missing_configs
