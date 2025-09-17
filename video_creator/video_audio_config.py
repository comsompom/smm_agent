#!/usr/bin/env python3
"""
Configuration file for Video-Audio Combiner

Edit the values below to configure your video and audio files.
"""

# =============================================================================
# FILE PATHS - Edit these to match your files
# =============================================================================

# Video file path (relative to script location or absolute path)
VIDEO_FILE = "sources/combined_scenes.mp4"

# Audio file path (relative to script location or absolute path)  
AUDIO_FILE = "result.wav"

# Output file name (will be created in the same directory as the script)
OUTPUT_FILE = "scene_full.mp4"

# =============================================================================
# AUDIO SETTINGS
# =============================================================================

# Audio volume (0.0 = silent, 1.0 = original volume, 1.5 = 50% louder)
AUDIO_VOLUME = 0.7

# Fade in duration in seconds (0 = no fade in)
AUDIO_FADE_IN = 1.0

# Fade out duration in seconds (0 = no fade out)
AUDIO_FADE_OUT = 1.0

# =============================================================================
# VIDEO SETTINGS
# =============================================================================

# Video codec for output (libx264, libx265, etc.)
VIDEO_CODEC = "libx264"

# Audio codec for output (aac, mp3, etc.)
AUDIO_CODEC = "aac"

# Video quality: "low", "medium", "high"
# - low: 500k bitrate, 128k audio (smaller file, lower quality)
# - medium: 1000k bitrate, 192k audio (balanced)
# - high: 2000k bitrate, 320k audio (larger file, higher quality)
VIDEO_QUALITY = "medium"

# =============================================================================
# ADVANCED SETTINGS (usually no need to change)
# =============================================================================

# Whether to overwrite existing output file without asking
AUTO_OVERWRITE = False

# Whether to show detailed progress during processing
VERBOSE_OUTPUT = False
