#!/usr/bin/env python3
"""
Simple Social Media Poster
Automatically posts messages from smm_message.md to all configured social media platforms,
then fetches and posts NASA APOD content
"""

import asyncio
import os
import random
import glob
from social_media_poster import SocialMediaPoster
from nasa_apod import NASAAPOD
from gg_example import create_new_message
from config import Config


def read_message_from_file():
    """Read message from smm_message.md file"""
    message_file = "smm_message.md"
    
    if not os.path.exists(message_file):
        print(f"❌ Error: {message_file} file not found!")
        print(f"Please create {message_file} with your message content.")
        return None
    
    try:
        with open(message_file, 'r', encoding='utf-8') as file:
            message = file.read().strip()
        
        if not message:
            print(f"❌ Error: {message_file} is empty!")
            return None
        
        return message
    
    except Exception as e:
        print(f"❌ Error reading {message_file}: {str(e)}")
        return None


def get_random_image():
    """Get a random image from the images folder"""
    images_folder = "images"
    
    if not os.path.exists(images_folder):
        print(f"❌ Images folder not found: {images_folder}")
        return None
    
    # Get all image files from the images folder
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.webp']
    image_files = []
    
    for extension in image_extensions:
        image_files.extend(glob.glob(os.path.join(images_folder, extension)))
        image_files.extend(glob.glob(os.path.join(images_folder, extension.upper())))
    
    if not image_files:
        print("📁 Images folder is empty")
        return None
    
    # Select a random image
    random_image = random.choice(image_files)
    print(f"🎲 Selected random image: {random_image}")
    
    return random_image


def delete_image(image_path):
    """Delete the image file after successful posting"""
    try:
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"🗑️  Deleted image: {image_path}")
            return True
        else:
            print(f"⚠️  Image file not found for deletion: {image_path}")
            return False
    except Exception as e:
        print(f"❌ Error deleting image {image_path}: {str(e)}")
        return False


async def post_daily_message_with_image(poster: SocialMediaPoster):
    """Post daily message with random image from images folder"""
    print("\n" + "="*50)
    print("📅 POSTING DAILY MESSAGE WITH RANDOM IMAGE")
    print("="*50)
    
    # Create new message using create_new_message(2)
    print("🤖 Creating new daily message...")
    create_new_message(2)
    
    # Read the newly created message
    message = read_message_from_file()
    if not message:
        print("❌ Failed to read daily message")
        return
    
    print(f"📝 Daily message: {message[:100]}{'...' if len(message) > 100 else ''}")
    
    # Get random image from images folder
    random_image = get_random_image()
    
    if random_image:
        print(f"🖼️  Posting with image: {random_image}")
        
        # Post message with image to all platforms
        print("🚀 Posting daily message with image to all platforms...")
        results = await poster.post_to_all_platforms(message, random_image)
        
        # Display posting results
        print("\n📊 Daily Message Posting Results:")
        print("-" * 40)
        
        successful_posts = 0
        failed_posts = 0
        
        for result in results:
            status = "✅ SUCCESS" if result["success"] else "❌ FAILED"
            platform = result["platform"]
            
            if result["success"]:
                successful_posts += 1
                print(f"{status} - {platform}")
            else:
                failed_posts += 1
                error = result.get("error", "Unknown error")
                print(f"{status} - {platform}: {error}")
        
        # Summary
        print("-" * 40)
        print(f"📈 Daily Message Summary: {successful_posts} successful, {failed_posts} failed")
        
        # Delete image if at least one post was successful
        if successful_posts > 0:
            print("🎉 Daily message with image posted successfully!")
            delete_image(random_image)
        else:
            print("❌ No platforms were posted to successfully. Image not deleted.")
    else:
        # No image available, post text only
        print("📝 No images available, posting text-only message...")
        
        # Post message without image to all platforms
        print("🚀 Posting daily message (text only) to all platforms...")
        results = await poster.post_to_all_platforms(message)
        
        # Display posting results
        print("\n📊 Daily Message Posting Results:")
        print("-" * 40)
        
        successful_posts = 0
        failed_posts = 0
        
        for result in results:
            status = "✅ SUCCESS" if result["success"] else "❌ FAILED"
            platform = result["platform"]
            
            if result["success"]:
                successful_posts += 1
                print(f"{status} - {platform}")
            else:
                failed_posts += 1
                error = result.get("error", "Unknown error")
                print(f"{status} - {platform}: {error}")
        
        # Summary
        print("-" * 40)
        print(f"📈 Daily Message Summary: {successful_posts} successful, {failed_posts} failed")
        
        if successful_posts > 0:
            print("🎉 Daily message posted successfully!")
        else:
            print("❌ No platforms were posted to successfully.")


async def post_nasa_apod(poster: SocialMediaPoster):
    """Fetch and post NASA APOD content"""
    print("\n" + "="*50)
    print("🔭 POSTING NASA ASTRONOMY PICTURE OF THE DAY")
    print("="*50)
    
    # Initialize NASA APOD handler
    nasa = NASAAPOD(Config.NASA_API_KEY)
    
    # Get APOD content
    apod_message, image_path = nasa.get_apod_content()
    
    if not apod_message:
        print("❌ Failed to fetch NASA APOD data")
        return
    
    print(f"📝 APOD Message: {apod_message[:100]}{'...' if len(apod_message) > 100 else ''}")
    if image_path:
        print(f"🖼️  Image: {image_path}")
    print()
    
    # Post APOD content to all platforms
    print("🚀 Posting NASA APOD to all platforms...")
    results = await poster.post_to_all_platforms(apod_message, image_path)
    
    # Display APOD posting results
    print("\n📊 APOD Posting Results:")
    print("-" * 40)
    
    successful_posts = 0
    failed_posts = 0
    
    for result in results:
        status = "✅ SUCCESS" if result["success"] else "❌ FAILED"
        platform = result["platform"]
        
        if result["success"]:
            successful_posts += 1
            print(f"{status} - {platform}")
        else:
            failed_posts += 1
            error = result.get("error", "Unknown error")
            print(f"{status} - {platform}: {error}")
    
    # APOD Summary
    print("-" * 40)
    print(f"📈 APOD Summary: {successful_posts} successful, {failed_posts} failed")
    
    if successful_posts > 0:
        print("🎉 NASA APOD posted successfully!")
    else:
        print("❌ No platforms were posted to successfully for APOD.")


async def main():
    """Main function that automatically posts to all platforms"""
    print("🚀 SOCIAL MEDIA BOT - AUTOMATIC POSTING")
    print("=" * 50)

    # Create a new message
    create_new_message(1)
    
    # Read message from file
    message = read_message_from_file()
    if not message:
        return
    
    print(f"📝 Message to post: {message[:100]}{'...' if len(message) > 100 else ''}")
    print()
    
    # Initialize poster
    poster = SocialMediaPoster()
    
    # Check available platforms
    available_platforms = list(poster.platforms.keys())
    if not available_platforms:
        print("❌ No platforms are configured!")
        print("Please check your .env file and ensure API keys are set.")
        return
    
    print(f"✅ Configured platforms: {', '.join(available_platforms)}")
    print()
    
    # STEP 1: Post initial message to all platforms
    print("🚀 Step 1: Posting initial message to all platforms...")
    results = await poster.post_to_all_platforms(message)
    
    # Display initial posting results
    print("\n📊 Initial Posting Results:")
    print("-" * 40)
    
    successful_posts = 0
    failed_posts = 0
    
    for result in results:
        status = "✅ SUCCESS" if result["success"] else "❌ FAILED"
        platform = result["platform"]
        
        if result["success"]:
            successful_posts += 1
            print(f"{status} - {platform}")
        else:
            failed_posts += 1
            error = result.get("error", "Unknown error")
            print(f"{status} - {platform}: {error}")
    
    # Initial posting summary
    print("-" * 40)
    print(f"📈 Initial Posting Summary: {successful_posts} successful, {failed_posts} failed")
    
    if successful_posts > 0:
        print("🎉 Initial message posted successfully!")
    else:
        print("❌ No platforms were posted to successfully for initial message.")
    
    # STEP 2: Post NASA APOD content
    await post_nasa_apod(poster)
    
    # STEP 3: Post daily message with random image
    await post_daily_message_with_image(poster)
    
    print("\n" + "="*50)
    print("🎉 ALL POSTING COMPLETED!")
    print("="*50)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Script interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("Please check your configuration and try again.")
