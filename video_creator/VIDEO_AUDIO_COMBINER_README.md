# Video-Audio Combiner for Moon Home Project

This tool allows you to combine video and audio files, adding audio to the beginning of your video. Perfect for adding background music, narration, or sound effects to your Moon Home project videos.

## 🌙 Features

- **Smart Audio Placement**: Adds audio to the beginning of the video
- **Length Preservation**: If video is longer than audio, maintains original video length
- **Volume Control**: Adjustable audio volume levels
- **Fade Effects**: Optional fade in/out for smooth audio transitions
- **Quality Settings**: Multiple quality presets (low, medium, high)
- **Progress Tracking**: Real-time progress updates during processing
- **Error Handling**: Comprehensive error checking and user feedback

## 📋 Requirements

- Python 3.6 or higher
- MoviePy library (`pip install moviepy`)
- Video file (MP4, AVI, MOV, etc.)
- Audio file (MP3, WAV, AAC, etc.)

## 🚀 Quick Start

### Option 1: Simple Script
1. Edit the file paths in `combine_video_audio.py`
2. Run: `python combine_video_audio.py`

### Option 2: Advanced Script (Recommended)
1. Edit settings in `video_audio_config.py`
2. Run: `python combine_video_audio_advanced.py`

### Option 3: Windows Batch File
1. Double-click `combine_video_audio.bat`
2. Follow the on-screen instructions

## ⚙️ Configuration

Edit `video_audio_config.py` to customize your settings:

```python
# File paths
VIDEO_FILE = "templates/images/scene_400.mp4"
AUDIO_FILE = "templates/images/background_music.mp3"
OUTPUT_FILE = "scene_full.mp4"

# Audio settings
AUDIO_VOLUME = 0.7  # 0.0 = silent, 1.0 = original, 1.5 = 50% louder
AUDIO_FADE_IN = 1.0  # Fade in duration in seconds
AUDIO_FADE_OUT = 1.0  # Fade out duration in seconds

# Video settings
VIDEO_QUALITY = "medium"  # "low", "medium", "high"
```

## 📊 Quality Settings

| Quality | Video Bitrate | Audio Bitrate | File Size | Use Case |
|---------|---------------|---------------|-----------|----------|
| Low     | 500k          | 128k          | Small     | Web preview, quick sharing |
| Medium  | 1000k         | 192k          | Medium    | General use, balanced |
| High    | 2000k         | 320k          | Large     | High quality, archival |

## 🎯 How It Works

### Audio Shorter Than Video
- Audio is added to the beginning
- Remaining video duration is silent
- **Output length = Original video length**

### Audio Longer Than Video
- Audio is trimmed to match video length
- **Output length = Original video length**

### Audio Same Length as Video
- Audio is added to the entire video
- **Output length = Original video length**

## 📁 File Structure

```
moon_home/
├── combine_video_audio.py              # Simple script
├── combine_video_audio_advanced.py     # Advanced script (recommended)
├── video_audio_config.py               # Configuration file
├── combine_video_audio.bat             # Windows batch file
├── VIDEO_AUDIO_COMBINER_README.md      # This documentation
└── templates/images/
    ├── scene_400.mp4                   # Example video file
    └── background_music.mp3            # Example audio file
```

## 🔧 Installation

1. **Install Python** (if not already installed):
   - Download from [python.org](https://python.org)
   - Make sure to check "Add Python to PATH" during installation

2. **Install MoviePy**:
   ```bash
   pip install moviepy
   ```

3. **Verify Installation**:
   ```bash
   python -c "import moviepy; print('MoviePy version:', moviepy.__version__)"
   ```

## 📖 Usage Examples

### Example 1: Basic Usage
```python
# In video_audio_config.py
VIDEO_FILE = "my_video.mp4"
AUDIO_FILE = "background_music.mp3"
AUDIO_VOLUME = 0.5  # 50% volume
```

### Example 2: High Quality with Fade Effects
```python
# In video_audio_config.py
VIDEO_QUALITY = "high"
AUDIO_FADE_IN = 2.0   # 2-second fade in
AUDIO_FADE_OUT = 2.0  # 2-second fade out
AUDIO_VOLUME = 0.8    # 80% volume
```

### Example 3: Silent Video with Narration
```python
# In video_audio_config.py
AUDIO_VOLUME = 1.2    # 20% louder for narration
AUDIO_FADE_IN = 0.5   # Quick fade in
AUDIO_FADE_OUT = 0.5  # Quick fade out
```

## 🎬 Supported Formats

### Video Formats
- MP4 (recommended)
- AVI
- MOV
- MKV
- WMV
- FLV

### Audio Formats
- MP3 (recommended)
- WAV
- AAC
- M4A
- OGG
- FLAC

## ⚠️ Troubleshooting

### Common Issues

**"MoviePy is not installed"**
```bash
pip install moviepy
```

**"File not found"**
- Check file paths in `video_audio_config.py`
- Use absolute paths if relative paths don't work
- Ensure files exist and are accessible

**"Permission denied"**
- Close any applications using the output file
- Run as administrator (Windows)
- Check file permissions

**"Out of memory"**
- Use lower quality settings
- Process smaller video files
- Close other applications

### Performance Tips

1. **Use MP4 format** for best compatibility and performance
2. **Lower quality settings** for faster processing
3. **Close other applications** to free up memory
4. **Use SSD storage** for faster file I/O

## 🔄 Integration with Moon Home

After creating your combined video:

1. **Move to project folder**:
   ```bash
   mv scene_full.mp4 templates/images/
   ```

2. **Update HTML templates**:
   ```html
   <video controls>
       <source src="/static/images/combined_video_with_audio.mp4" type="video/mp4">
   </video>
   ```

3. **Update Flask routes** (if needed):
   ```python
   @app.route('/static/images/<filename>')
   def serve_image(filename):
       return send_from_directory('templates/images', filename)
   ```

## 📈 Advanced Features

### Custom Audio Placement
For more control over audio placement, modify the script:

```python
# Add audio at specific time
audio_clip = audio_clip.set_start(5.0)  # Start at 5 seconds

# Loop audio to match video length
audio_clip = audio_clip.loop(duration=video_duration)
```

### Multiple Audio Tracks
```python
# Combine multiple audio files
audio1 = AudioFileClip("music.mp3")
audio2 = AudioFileClip("narration.mp3")
combined_audio = CompositeAudioClip([audio1, audio2])
```

## 🆘 Support

If you encounter issues:

1. **Check the error message** - it usually indicates the problem
2. **Verify file paths** in the configuration
3. **Test with smaller files** first
4. **Check MoviePy documentation** for advanced features
5. **Review the console output** for detailed information

## 📝 License

This tool is part of the Moon Home project for the Lunar Republic.

## 🚀 Future Enhancements

- GUI interface for easier use
- Batch processing multiple files
- Audio waveform visualization
- Real-time preview
- Cloud processing integration
- Advanced audio effects

---

**Happy video editing! 🌙✨**
