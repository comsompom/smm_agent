# SMM Poster - Social Media Management Suite

A comprehensive Python suite for automated social media management, content generation, and multimedia processing. This project provides tools for posting to multiple social media platforms, AI-powered content generation, video/audio processing, and YouTube uploads.

## 🌟 Features

### 📱 **Social Media Posting**
- 🚀 **Multi-platform posting**: Post to all platforms at once or choose specific ones
- 🔧 **Easy configuration**: Simple environment variable setup
- 📱 **Platform support**: Telegram, Discord, Facebook, X (Twitter)
- ⚡ **Async support**: Efficient handling of multiple platforms
- 🛡️ **Error handling**: Comprehensive error handling and logging
- ⏱️ **Rate limiting**: Built-in delays to avoid API rate limits
- 🌌 **NASA APOD integration**: Automatically fetches and posts NASA's daily space image
- 🖼️ **Image support**: Post both text and images to supported platforms

### 🤖 **AI Content Generation**
- 🧠 **Google Gemini integration**: Generate engaging social media content using AI
- 📝 **Automatic SQL generation**: Creates database entries for generated content
- 🏷️ **Smart hashtag extraction**: Automatically extracts and formats hashtags
- 📊 **Content management**: Updates master content files with new AI-generated posts

### 🎬 **Video & Audio Processing**
- 🎵 **Audio concatenation**: Combine multiple audio files with fade effects and crossfades
- 🎥 **Video-audio combination**: Add audio tracks to video files with advanced controls
- 🎞️ **Video concatenation**: Merge multiple video files seamlessly
- 🔊 **Text-to-speech**: Convert text to audio using AI models
- ⚙️ **Configurable processing**: Volume adjustment, fade effects, quality control

### 📺 **YouTube Integration**
- 📤 **Automated uploads**: Upload videos directly to YouTube
- 🔐 **OAuth authentication**: Secure Google API integration
- 📋 **Metadata management**: Set titles, descriptions, and categories
- 🎯 **Batch processing**: Handle multiple video uploads

### 🗄️ **Database Management**
- 💾 **MySQL integration**: Store and manage social media content
- 📊 **Content tracking**: Track posting history and performance
- 🔄 **Automated SQL generation**: Create database entries from content
- 📈 **Data analytics**: Query and analyze posting patterns

## Prerequisites

- Python 3.7 or higher
- API keys and tokens for the platforms you want to use
- Basic knowledge of setting up social media developer accounts

## Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd smm_bot
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment variables**
   - Copy `env_example.txt` to `.env`
   - Fill in your actual API keys and tokens

## Configuration

### 1. Telegram Setup
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Get the bot token
4. Add the bot to your channel
5. Get the channel ID (e.g., `@channelname` or numeric ID)

### 2. Discord Setup
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section and create a bot
4. Copy the bot token
5. Invite the bot to your server with proper permissions
6. Get the channel ID (right-click channel → Copy ID)

### 3. Facebook Setup
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app
3. Get an access token with proper permissions
4. Get your group ID from the group URL

### 4. X (Twitter) Setup
1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new app
3. Get API keys and access tokens
4. Ensure your app has write permissions

### 5. NASA APOD Setup
1. **Optional**: Get your free API key from [https://api.nasa.gov/](https://api.nasa.gov/)
2. A default API key is provided and will work immediately
3. You can replace it with your own key in the `.env` file

## 🚀 Usage

### 📱 **Social Media Posting**

#### Quick Start
Run the interactive script:
```bash
python simple_poster.py
```

The script will:
1. **Step 1**: Post your message from `smm_message.md` to all configured platforms
2. **Step 2**: Automatically fetch NASA's Astronomy Picture of the Day and post it with the image
3. **Step 3**: Generate AI content and post with random images

#### Programmatic Usage
```python
from social_media_poster import SocialMediaPoster
from nasa_apod import NASAAPOD
import asyncio

async def main():
    poster = SocialMediaPoster()
    
    # Post to all platforms
    results = await poster.post_to_all_platforms("Hello, World!")
    
    # Post NASA APOD content
    nasa = NASAAPOD(Config.NASA_API_KEY)
    apod_message, image_path = nasa.get_apod_content()
    await poster.post_to_all_platforms(apod_message, image_path)

asyncio.run(main())
```

### 🤖 **AI Content Generation**

Generate engaging social media content using Google Gemini:
```bash
python gg_example.py
```

Features:
- Creates timestamped SQL files for database storage
- Updates master content files automatically
- Extracts hashtags and formats content properly

### 🎬 **Video & Audio Processing**

#### Audio Concatenation
```bash
cd video_creator
python concatenate_audio.py
```
Edit the configuration section in the script to set your input/output files and processing options.

#### Video-Audio Combination
```bash
cd video_creator
python combine_video_audio_advanced.py
```

#### Text-to-Speech
```bash
cd video_creator
python audio_from_text.py
```

### 📺 **YouTube Uploads**

Upload videos to YouTube:
```bash
cd youtube_up
python youtube_uploader.py
```

### 🗄️ **Database Management**

Store and manage social media content:
```bash
# Execute SQL scripts
cd db_utils
python -c "import mysql.connector; # Your database operations"
```

### Command Line Options
- **Post to all platforms**: Choose option 1
- **Post to specific platform**: Choose option 2
- **Exit**: Choose option 3

## 📁 Project Structure

```
smm_poster/
├── 📱 Social Media Core
│   ├── social_media_poster.py    # Main posting logic with image support
│   ├── simple_poster.py          # User-friendly interactive script
│   ├── nasa_apod.py             # NASA APOD API integration
│   ├── config.py                # Configuration management
│   ├── utils.py                 # Utility functions
│   └── example_usage.py         # Usage examples
│
├── 🤖 AI Content Generation
│   ├── gg_example.py            # Google Gemini AI integration
│   └── gg_api_key               # API key storage
│
├── 🗄️ Database Management
│   └── db_utils/
│       ├── constants.py         # Database connection settings
│       ├── table_sql.txt        # Database schema
│       ├── moon_post.md         # Content storage
│       └── insert_moon_posts.sql # SQL insertion scripts
│
├── 🎬 Video & Audio Processing
│   └── video_creator/
│       ├── combine_video_audio_advanced.py  # Video-audio combination
│       ├── concatenate_audio.py            # Audio concatenation
│       ├── combine_videos.py               # Video concatenation
│       ├── audio_from_text.py              # Text-to-speech
│       ├── video_audio_config.py           # Processing configuration
│       └── sources/                        # Video source files
│
├── 📺 YouTube Integration
│   └── youtube_up/
│       ├── youtube_uploader.py  # YouTube upload functionality
│       ├── client_secret.json   # Google OAuth credentials
│       └── upload_file.md       # Upload documentation
│
├── 📚 Documentation
│   ├── docs/
│   │   ├── facebook_app.md      # Facebook app setup
│   │   ├── x_twiter_app.md      # X/Twitter app setup
│   │   └── name_cheap_cron.md   # Cron job setup
│   └── discord_debug/           # Discord troubleshooting tools
│
├── 🖼️ Media Assets
│   └── images/                  # Downloaded NASA APOD images
│
├── ⚙️ Configuration
│   ├── requirements.txt         # Python dependencies
│   ├── env_example.txt         # Environment variables template
│   └── smm_message.md          # Custom message content
│
└── 📖 README.md                # This documentation
```

## ⚙️ Environment Variables

Create a `.env` file with the following variables:

```env
# Social Media Platforms
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHANNEL_ID=your_channel_id
DISCORD_BOT_TOKEN=your_bot_token
DISCORD_CHANNEL_ID=your_channel_id
FACEBOOK_ACCESS_TOKEN=your_access_token
FACEBOOK_GROUP_ID=your_group_id
X_API_KEY=your_api_key
X_API_SECRET=your_api_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
X_BEARER_TOKEN=your_bearer_token

# External APIs
NASA_API_KEY=your_nasa_api_key
GOOGLE_GEMINI_API_KEY=your_gemini_api_key

# Database (MySQL)
DB_HOST=localhost
DB_PORT=5522
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database

# General Settings
POST_DELAY=5
MAX_RETRIES=3
```

## 📦 Dependencies

The project uses the following main dependencies:

### Core Social Media
- `python-telegram-bot` - Telegram API integration
- `discord.py` - Discord API integration
- `facebook-sdk` - Facebook API integration
- `tweepy` - X/Twitter API integration
- `aiohttp` - Async HTTP requests
- `requests` - HTTP library

### AI & Content Generation
- `google-generativeai` - Google Gemini AI integration
- `torch` & `torchaudio` - Text-to-speech models

### Video & Audio Processing
- `moviepy` - Video and audio manipulation
- `pathlib2` - Enhanced path handling

### YouTube Integration
- `google-api-python-client` - YouTube API client
- `google-auth-oauthlib` - OAuth authentication
- `google-auth-httplib2` - HTTP transport for auth

### Database & Utilities
- `mysql-connector-python` - MySQL database connection
- `python-dotenv` - Environment variable management
- `schedule` - Task scheduling
- `protobuf` - Protocol buffer support

Install all dependencies with:
```bash
pip install -r requirements.txt
```

## NASA APOD Integration

The bot now automatically fetches and posts NASA's Astronomy Picture of the Day:

- **Automatic fetching**: Gets the latest APOD data from NASA's API
- **Image download**: Downloads the high-resolution image locally
- **Multi-platform posting**: Posts both text and image to all configured platforms
- **Smart formatting**: Truncates long explanations and adds relevant hashtags
- **Error handling**: Gracefully handles API failures and image download issues

### APOD Message Format
```
🌌 NASA Astronomy Picture of the Day - 2025-01-XX

📸 [Image Title]

📝 [Truncated explanation...]

📸 Credit: [Photographer Name]

#NASA #APOD #Astronomy #Space #Science #Cosmos #Astrophotography #SpaceExploration
```

## Troubleshooting

### Common Issues

1. **"No platforms are configured"**
   - Check your `.env` file exists and has correct values
   - Ensure API keys are valid and not expired

2. **"Channel not found" (Discord)**
   - Run `python discord_debug.py` to diagnose the issue
   - Run `python get_channel_id.py` to find the correct channel ID
   - Verify the bot is in the server and has proper permissions
   - Make sure Developer Mode is enabled to get the correct channel ID
   - Channel ID should be a long number (18+ digits), not a channel name

3. **Discord posting hangs or doesn't work**
   - The bot now uses Discord's REST API instead of the gateway connection
   - Make sure your bot token is valid and has proper permissions
   - Test with the provided `test_discord.py` script

4. **"Unauthorized" (Facebook)**
   - Check access token permissions
   - Verify group ID is correct
   - Ensure token hasn't expired

5. **"Rate limit exceeded"**
   - Increase `POST_DELAY` in your `.env` file
   - Wait before posting again

6. **NASA APOD failures**
   - Check internet connection
   - Verify NASA API key is valid
   - Check if images directory is writable

### Getting Help

- Check the logs for detailed error messages
- Verify all API keys and tokens are correct
- Ensure your social media apps have proper permissions
- Check platform-specific documentation for API changes

## Security Notes

- **Never commit your `.env` file** to version control
- Keep your API keys secure and private
- Regularly rotate your access tokens
- Use environment variables instead of hardcoding credentials

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this project.

## License

This project is open source and available under the [MIT License](LICENSE).

## Disclaimer

This tool is for educational and personal use. Please comply with each platform's Terms of Service and API usage guidelines. The authors are not responsible for any misuse of this tool.

---

### **Part 1: How to Get Your Telegram Channel ID**

The channel ID is a unique numerical identifier. It's essential for using the Telegram Bot API to send messages or perform other actions in your channel. This ID is different from the channel's username (e.g., `@mychannel`).

The easiest and most reliable method works for both **public** and **private** channels.

#### **Steps using a Helper Bot:**

1.  **Find a "Get ID" Bot**
    *   Open your Telegram app (Desktop or Mobile).
    *   In the search bar, type **`@userinfobot`** and select it from the results.
    *   Press the **Start** button to begin a chat with the bot.

    *(Alternative bots you can use: `@RawDataBot`, `@myidbot`)*

2.  **Go to Your Channel**
    *   Navigate to the channel whose ID you want to find.
    *   If the channel is new and has no messages, post a temporary message like "hello".

3.  **Forward a Message from Your Channel**
    *   **On Mobile:** Tap and hold on any message in your channel, then tap the **Forward** icon.
    *   **On Desktop:** Right-click on any message in your channel and select **Forward message**.

    

4.  **Send the Forwarded Message to the Bot**
    *   In the recipient list, search for and select the bot you started in Step 1 (e.g., **`@userinfobot`**).
    *   Send the message.

5.  **Copy Your Channel ID**
    *   The bot will immediately reply with information about the original sender.
    *   Look for the line **"Forwarded from channel"**. The number next to **`id:`** is your Channel ID.
    *   It will be a negative number starting with `-100`. For example: `-1001234567890`.

    

> **Important Note:** You must include the full number, including the `-100` prefix, when using it in APIs or other services.

---

### **Part 2: How to Add a Telegram Bot to Your Channel**

For a bot to be able to post messages or manage your channel, you must add it as a member and then promote it to an administrator.

**Prerequisite:** You must be the **owner** or an **administrator** of the channel with permission to add new admins.

#### **Steps to Add and Promote a Bot:**

1.  **Open Your Channel Info**
    *   Go to your Telegram channel.
    *   Click on the channel's name at the top to open its profile/info page.

2.  **Add the Bot as a Member**
    *   **On Desktop:** Click on the "Members" or "Subscribers" section. Then click **"Add Members"**.
    *   **On Mobile:** Tap on the "Subscribers" section. Then tap **"Add Subscriber"**.

    

3.  **Search for the Bot**
    *   In the search bar that appears, type the bot's full username, including the `@` symbol (e.g., `@your_bot_username`).
    *   The bot will appear in the search results.

4.  **Confirm the Addition**
    *   Click on the bot's name and confirm that you want to add it to the channel. The bot is now a member.

5.  **Promote the Bot to Administrator**
    *   A bot cannot do anything until it has admin permissions.
    *   Go back to the channel's info page.
    *   Click on **"Administrators"**.
    *   Click on **"Add Admin"**.
    *   Select the bot you just added from the list of members.

    

6.  **Set Bot Permissions**
    *   A new screen will appear showing a list of admin rights.
    *   **Crucially, enable the permissions the bot needs.** For most bots that just post content, you only need to enable **"Post Messages"**.
    *   Only grant the permissions your bot absolutely requires. For example:
        *   **Post Messages:** Allows the bot to send new messages to the channel.
        *   **Edit Messages of Others:** Allows the bot to edit messages.
        *   **Delete Messages of Others:** Allows the bot to delete messages.
    *   Once you've selected the permissions, click the **Save** or **check-mark icon** to confirm.

**Congratulations!** Your bot is now an administrator in your channel and can perform actions based on the permissions you granted it.

## How to get Discord Channel ID:

### Step 1: Enable Developer Mode in Discord

Developer Mode allows you to easily copy IDs for channels, users, messages, and guilds (servers).

1.  **Open Discord:** Launch the Discord desktop application or go to the Discord web client (discord.com/app).
2.  **Go to User Settings:** Click on the **User Settings** (gear icon) in the bottom-left corner, next to your username and avatar.
3.  **Navigate to Advanced Settings:** In the left-hand menu, scroll down until you see **App Settings**, then click on **Advanced**.
4.  **Toggle Developer Mode On:** Find the "Developer Mode" option and toggle it to **On**.
5.  **Close Settings:** You can now close the User Settings window by clicking the `Esc` key or the 'X' in the top right.

---

### Step 2: Copy the Channel ID

Now that Developer Mode is enabled, you can easily copy any channel's ID.

1.  **Go to the Desired Channel:** Navigate to the specific text or voice channel you want to get the ID for in your Discord server.
2.  **Right-Click the Channel:** Right-click on the name of the channel in the left-hand sidebar.
3.  **Click "Copy ID":** From the context menu that appears, select **"Copy ID"**.

    *   **For Mobile Users (iOS/Android):**
        1.  Long-press (tap and hold) on the channel name.
        2.  A menu will appear; scroll down and tap **"Copy ID"**.

---

### What the Channel ID Looks Like

The ID you copied will be a long string of numbers (usually 18 digits).
**Example:** `123456789012345678`

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License

```
MIT License

Copyright (c) 2025 SMM Poster Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Search existing [Issues](https://github.com/yourusername/smm_poster/issues)
3. Create a new issue with detailed information about your problem

## ⚠️ Disclaimer

This tool is for educational and personal use. Please comply with each platform's Terms of Service and API usage guidelines. The authors are not responsible for any misuse of this tool.

---

**Made with ❤️ for the social media community** 