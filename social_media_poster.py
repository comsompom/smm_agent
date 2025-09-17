import asyncio
import time
import logging
from typing import List, Dict, Optional
import requests
import tweepy
import facebook
from telegram import Bot
import discord
from discord.ext import commands
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TelegramPoster:
    """Handles posting to Telegram channels"""
    
    def __init__(self):
        self.bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
        self.channel_id = Config.TELEGRAM_CHANNEL_ID
    
    async def post_message(self, message: str, image_path: str = None) -> Dict[str, bool]:
        """Post message to Telegram channel with optional image"""
        try:
            if image_path:
                # Telegram has a 1024 character limit for captions
                # Truncate message if it's too long for caption
                if len(message) > 1024:
                    # Try to truncate at a word boundary
                    truncated_message = message[:1021]  # Leave room for "..."
                    last_space = truncated_message.rfind(' ')
                    if last_space > 900:  # If we can find a good word boundary
                        truncated_message = message[:last_space] + "..."
                    else:
                        truncated_message = message[:1021] + "..."
                    
                    logger.info(f"Message truncated for Telegram caption: {len(message)} -> {len(truncated_message)} chars")
                    caption = truncated_message
                else:
                    caption = message
                
                # Post with image
                with open(image_path, 'rb') as photo:
                    await self.bot.send_photo(
                        chat_id=self.channel_id,
                        photo=photo,
                        caption=caption
                    )
                logger.info(f"Successfully posted image + message to Telegram: {caption[:50]}...")
            else:
                # Post text only (no character limit for text messages)
                await self.bot.send_message(chat_id=self.channel_id, text=message)
                logger.info(f"Successfully posted to Telegram: {message[:50]}...")
            
            return {"success": True, "platform": "Telegram"}
        except Exception as e:
            logger.error(f"Failed to post to Telegram: {str(e)}")
            return {"success": False, "platform": "Telegram", "error": str(e)}


class DiscordPoster:
    """Handles posting to Discord channels using webhook API"""
    
    def __init__(self):
        if not Config.DISCORD_CHANNEL_ID or not Config.DISCORD_BOT_TOKEN:
            raise ValueError("Discord configuration missing. Please set DISCORD_BOT_TOKEN and DISCORD_CHANNEL_ID in your .env file")
        
        try:
            self.channel_id = int(Config.DISCORD_CHANNEL_ID)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid Discord channel ID: {Config.DISCORD_CHANNEL_ID}. Channel ID must be a numeric string.")
        
        self.token = Config.DISCORD_BOT_TOKEN
        self.base_url = "https://discord.com/api/v10"
    
    async def validate_channel_access(self) -> bool:
        """Validate that the bot can access the specified channel"""
        try:
            import aiohttp
            
            headers = {
                "Authorization": f"Bot {self.token}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/channels/{self.channel_id}",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        channel_data = await response.json()
                        logger.info(f"Discord channel validation successful: #{channel_data.get('name', 'Unknown')}")
                        return True
                    elif response.status == 404:
                        logger.error(f"Discord channel not found (ID: {self.channel_id}). Please check:")
                        logger.error("1. The channel ID is correct")
                        logger.error("2. The bot has access to the channel")
                        logger.error("3. The bot has the necessary permissions")
                        return False
                    else:
                        error_text = await response.text()
                        logger.error(f"Discord channel validation failed (HTTP {response.status}): {error_text}")
                        return False
        except Exception as e:
            logger.error(f"Error validating Discord channel access: {str(e)}")
            return False
    
    async def post_message(self, message: str, image_path: str = None) -> Dict[str, bool]:
        """Post message to Discord channel with optional image"""
        try:
            # First validate channel access
            if not await self.validate_channel_access():
                return {"success": False, "platform": "Discord", "error": "Channel validation failed. Please check your Discord configuration."}
            
            import aiohttp
            import base64
            
            headers = {
                "Authorization": f"Bot {self.token}",
                "Content-Type": "application/json"
            }
            
            # Prepare the payload
            payload = {
                "content": message
            }
            
            # If there's an image, we need to use multipart form data
            if image_path:
                # Validate image file exists and is readable
                import os
                if not os.path.exists(image_path):
                    raise Exception(f"Image file not found: {image_path}")
                
                if not os.path.isfile(image_path):
                    raise Exception(f"Path is not a file: {image_path}")
                
                # Check file size (Discord has a 8MB limit for most servers)
                file_size = os.path.getsize(image_path)
                max_size = 8 * 1024 * 1024  # 8MB
                if file_size > max_size:
                    raise Exception(f"Image file too large: {file_size} bytes (max: {max_size} bytes)")
                
                # For images, we'll use a different approach with files
                data = aiohttp.FormData()
                data.add_field('content', message)
                
                # Read the file content and add it to form data
                try:
                    with open(image_path, 'rb') as f:
                        file_content = f.read()
                    
                    # Determine content type based on file extension
                    import mimetypes
                    content_type, _ = mimetypes.guess_type(image_path)
                    if not content_type:
                        content_type = 'image/jpeg'  # Default fallback
                    
                    # Get filename from path
                    filename = os.path.basename(image_path)
                    data.add_field('file', file_content, filename=filename, content_type=content_type)
                    
                except Exception as e:
                    logger.error(f"Error reading image file {image_path}: {str(e)}")
                    raise Exception(f"Failed to read image file: {str(e)}")
                
                headers = {"Authorization": f"Bot {self.token}"}
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{self.base_url}/channels/{self.channel_id}/messages",
                        headers=headers,
                        data=data
                    ) as response:
                        if response.status == 200:
                            logger.info(f"Successfully posted image + message to Discord: {message[:50]}...")
                            return {"success": True, "platform": "Discord"}
                        else:
                            error_text = await response.text()
                            raise Exception(f"HTTP {response.status}: {error_text}")
            else:
                # Text only message
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{self.base_url}/channels/{self.channel_id}/messages",
                        headers=headers,
                        json=payload
                    ) as response:
                        if response.status == 200:
                            logger.info(f"Successfully posted to Discord: {message[:50]}...")
                            return {"success": True, "platform": "Discord"}
                        else:
                            error_text = await response.text()
                            raise Exception(f"HTTP {response.status}: {error_text}")
            
        except Exception as e:
            logger.error(f"Failed to post to Discord: {str(e)}")
            return {"success": False, "platform": "Discord", "error": str(e)}


class FacebookPoster:
    """Handles posting to Facebook groups"""
    
    def __init__(self):
        self.graph = facebook.GraphAPI(access_token=Config.FACEBOOK_ACCESS_TOKEN, version="3.1")
        self.group_id = Config.FACEBOOK_GROUP_ID
    
    def post_message(self, message: str, image_path: str = None) -> Dict[str, bool]:
        """Post message to Facebook group with optional image"""
        try:
            if image_path:
                # Post with image
                with open(image_path, 'rb') as image_file:
                    response = self.graph.put_object(
                        parent_object=self.group_id,
                        connection_name="photos",
                        message=message,
                        source=image_file
                    )
                logger.info(f"Successfully posted image + message to Facebook: {message[:50]}...")
            else:
                # Post text only
                response = self.graph.put_object(
                    parent_object=self.group_id,
                    connection_name="feed",
                    message=message
                )
                logger.info(f"Successfully posted to Facebook: {message[:50]}...")
            
            return {"success": True, "platform": "Facebook", "post_id": response.get('id')}
        except Exception as e:
            logger.error(f"Failed to post to Facebook: {str(e)}")
            return {"success": False, "platform": "Facebook", "error": str(e)}


class XPoster:
    """Handles posting to X (Twitter)"""
    
    def __init__(self):
        self.client = tweepy.Client(
            consumer_key=Config.X_API_KEY,
            consumer_secret=Config.X_API_SECRET,
            access_token=Config.X_ACCESS_TOKEN,
            access_token_secret=Config.X_ACCESS_TOKEN_SECRET
        )
    
    def post_message(self, message: str, image_path: str = None) -> Dict[str, bool]:
        """Post message to X (Twitter) with optional image"""
        try:
            # Ensure message length is within Twitter's limit
            if len(message) > 280:
                message = message[:277] + "..."
            
            # Note: X/Twitter image posting requires additional setup with media upload
            # For now, we'll post text only and log a note about images
            if image_path:
                logger.warning("Image posting to X/Twitter requires media upload setup - posting text only")
            
            response = self.client.create_tweet(text=message)
            logger.info(f"Successfully posted to X: {message[:50]}...")
            return {"success": True, "platform": "X", "tweet_id": response.data['id']}
        except Exception as e:
            logger.error(f"Failed to post to X: {str(e)}")
            return {"success": False, "platform": "X", "error": str(e)}


class SocialMediaPoster:
    """Main class that coordinates posting to all platforms"""
    
    def __init__(self):
        self.platforms = {
            "Telegram": TelegramPoster(),
            "Discord": DiscordPoster(),
            # "Facebook": FacebookPoster(),
            "X": XPoster()
        }
        
        # Validate configuration
        missing_configs = Config.validate_config()
        if missing_configs:
            logger.warning(f"Missing configuration for: {', '.join(missing_configs)}")
            # Remove platforms with missing config
            for platform in missing_configs:
                if platform in self.platforms:
                    del self.platforms[platform]
    
    async def post_to_all_platforms(self, message: str, image_path: str = None) -> List[Dict[str, bool]]:
        """Post message and optional image to all configured platforms"""
        results = []
        
        for platform_name, poster in self.platforms.items():
            try:
                if platform_name in ["Telegram", "Discord"]:
                    # Async platforms
                    result = await poster.post_message(message, image_path)
                else:
                    # Sync platforms
                    result = poster.post_message(message, image_path)
                
                results.append(result)
                
                # Add delay between posts to avoid rate limiting
                if platform_name != list(self.platforms.keys())[-1]:  # Not the last platform
                    time.sleep(Config.POST_DELAY)
                    
            except Exception as e:
                logger.error(f"Error posting to {platform_name}: {str(e)}")
                results.append({
                    "success": False,
                    "platform": platform_name,
                    "error": str(e)
                })
        
        return results
    
    def post_to_specific_platform(self, platform_name: str, message: str, image_path: str = None) -> Dict[str, bool]:
        """Post message and optional image to a specific platform"""
        if platform_name not in self.platforms:
            return {"success": False, "platform": platform_name, "error": "Platform not configured"}
        
        try:
            poster = self.platforms[platform_name]
            if platform_name in ["Telegram", "Discord"]:
                # For async platforms, we'll need to handle this differently in the main script
                return {"success": False, "platform": platform_name, "error": "Use async method for this platform"}
            else:
                return poster.post_message(message, image_path)
        except Exception as e:
            logger.error(f"Error posting to {platform_name}: {str(e)}")
            return {"success": False, "platform": platform_name, "error": str(e)}


def read_message_from_file(filename: str = "smm_message.md") -> str:
    """Read message from a markdown file"""
    import os
    
    if not os.path.exists(filename):
        logger.warning(f"Message file {filename} not found")
        return None
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            message = file.read().strip()
        
        if not message:
            logger.warning(f"Message file {filename} is empty")
            return None
        
        return message
    
    except Exception as e:
        logger.error(f"Error reading {filename}: {str(e)}")
        return None


async def post_real_content():
    """Post real content from message file and NASA APOD"""
    poster = SocialMediaPoster()
    
    # Try to read message from file
    message = read_message_from_file()
    
    if message:
        print(f"📝 Posting message from file: {message[:100]}{'...' if len(message) > 100 else ''}")
        print("=" * 50)
        
        # Post message to all platforms
        results = await poster.post_to_all_platforms(message)
        
        # Display results
        print("\nMessage Posting Results:")
        print("-" * 30)
        for result in results:
            status = "✅ SUCCESS" if result["success"] else "❌ FAILED"
            platform = result["platform"]
            if result["success"]:
                print(f"{status} - {platform}")
            else:
                error = result.get("error", "Unknown error")
                print(f"{status} - {platform}: {error}")
    
    # Post NASA APOD content
    try:
        from nasa_apod import NASAAPOD
        nasa = NASAAPOD(Config.NASA_API_KEY)
        apod_message, image_path = nasa.get_apod_content()
        
        if apod_message:
            print(f"\n🔭 Posting NASA APOD: {apod_message[:100]}{'...' if len(apod_message) > 100 else ''}")
            if image_path:
                print(f"🖼️  With image: {image_path}")
            print("=" * 50)
            
            # Post APOD to all platforms
            apod_results = await poster.post_to_all_platforms(apod_message, image_path)
            
            # Display APOD results
            print("\nNASA APOD Posting Results:")
            print("-" * 30)
            for result in apod_results:
                status = "✅ SUCCESS" if result["success"] else "❌ FAILED"
                platform = result["platform"]
                if result["success"]:
                    print(f"{status} - {platform}")
                else:
                    error = result.get("error", "Unknown error")
                    print(f"{status} - {platform}: {error}")
    except ImportError:
        logger.warning("NASA APOD module not available")
    except Exception as e:
        logger.error(f"Error posting NASA APOD: {str(e)}")


async def main(message: str = None):
    """Main function to demonstrate usage"""
    poster = SocialMediaPoster()
    
    # Use provided message or create a meaningful default
    if not message:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"""🚀 Social Media Bot Update - {timestamp}

📱 Automated posting to multiple platforms
🔧 Powered by Python and social media APIs
📊 Real-time content distribution

#SocialMedia #Automation #Python #Bot #Tech"""
    
    print(f"Posting message: {message[:100]}{'...' if len(message) > 100 else ''}")
    print("=" * 50)
    
    # Post to all platforms
    results = await poster.post_to_all_platforms(message)
    
    # Display results
    print("\nPosting Results:")
    print("-" * 30)
    for result in results:
        status = "✅ SUCCESS" if result["success"] else "❌ FAILED"
        platform = result["platform"]
        if result["success"]:
            print(f"{status} - {platform}")
        else:
            error = result.get("error", "Unknown error")
            print(f"{status} - {platform}: {error}")


if __name__ == "__main__":
    import sys
    
    # Check if configuration is valid
    missing_configs = Config.validate_config()
    if missing_configs:
        print(f"⚠️  Warning: Missing configuration for: {', '.join(missing_configs)}")
        print("Please check your .env file and ensure all required API keys are set.")
        print()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--real":
            # Post real content from files
            print("🚀 Posting real content from message file and NASA APOD...")
            asyncio.run(post_real_content())
        elif sys.argv[1] == "--message" and len(sys.argv) > 2:
            # Post custom message
            custom_message = " ".join(sys.argv[2:])
            print(f"🚀 Posting custom message: {custom_message[:100]}{'...' if len(custom_message) > 100 else ''}")
            asyncio.run(main(custom_message))
        else:
            print("Usage:")
            print("  python social_media_poster.py                    # Post default message")
            print("  python social_media_poster.py --real             # Post real content from files")
            print("  python social_media_poster.py --message 'text'   # Post custom message")
    else:
        # Run the main function with default message
        asyncio.run(main())
