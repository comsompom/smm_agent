#!/usr/bin/env python3
"""
Advanced Video-Audio Combiner Script for Moon Home Project

This script combines a video file with an audio file, adding the audio to the beginning
of the video. If the video is longer than the audio, the output video maintains the
original video length.

Features:
- Configurable via external config file
- Multiple audio placement options
- Audio volume and fade controls
- Quality settings
- Progress tracking
- Error handling

Requirements:
- moviepy library (pip install moviepy)
- Input video file (MP4, AVI, MOV, etc.)
- Input audio file (MP3, WAV, AAC, etc.)

Usage:
1. Edit video_audio_config.py with your file paths and settings
2. Run: python combine_video_audio_advanced.py

Author: Moon Home Development Team
Date: January 2025
"""

import os
import sys
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
from datetime import datetime
import time


# Import configuration
try:
    from video_audio_config import *
except ImportError:
    print("❌ Error: video_audio_config.py not found!")
    print("Please make sure the configuration file exists in the same directory.")
    sys.exit(1)


def check_file_exists(file_path, file_type):
    """Check if a file exists and return absolute path."""
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_type} file not found: {file_path}")
        return None
    
    abs_path = os.path.abspath(file_path)
    print(f"✅ Found {file_type} file: {abs_path}")
    return abs_path


def get_file_info(file_path):
    """Get basic file information."""
    try:
        stat = os.stat(file_path)
        size_mb = stat.st_size / (1024 * 1024)
        return {
            'size_mb': round(size_mb, 2),
            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        print(f"⚠️  Warning: Could not get file info for {file_path}: {e}")
        return None


def format_duration(seconds):
    """Format duration in seconds to MM:SS format."""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


def combine_video_audio(video_path, audio_path, output_path):
    """Combine video and audio files with advanced options."""
    print("\n🎬 Starting video-audio combination process...")
    start_time = time.time()
    
    try:
        # Load video and audio files
        print("📹 Loading video file...")
        video_clip = VideoFileClip(video_path)
        
        print("🎵 Loading audio file...")
        audio_clip = AudioFileClip(audio_path)
        
        # Get durations
        video_duration = video_clip.duration
        audio_duration = audio_clip.duration
        
        print(f"📊 Video duration: {format_duration(video_duration)}")
        print(f"🎵 Audio duration: {format_duration(audio_duration)}")
        
        # Adjust audio volume and add fade effects
        if AUDIO_VOLUME != 1.0:
            print(f"🔊 Adjusting audio volume to {AUDIO_VOLUME}x")
            audio_clip = audio_clip.volumex(AUDIO_VOLUME)
        
        if AUDIO_FADE_IN > 0:
            print(f"🎭 Adding {AUDIO_FADE_IN}s fade in")
            try:
                # Try the standard fadein method
                audio_clip = audio_clip.fadein(AUDIO_FADE_IN)
            except AttributeError:
                # Fallback: skip fade in if method not available
                print("⚠️  Fade in method not available in this MoviePy version")
                print("   Continuing without fade in effect...")
            except Exception as e:
                print(f"⚠️  Could not apply fade in: {e}")
                print("   Continuing without fade in effect...")
        
        if AUDIO_FADE_OUT > 0:
            print(f"🎭 Adding {AUDIO_FADE_OUT}s fade out")
            try:
                # Try the standard fadeout method
                audio_clip = audio_clip.fadeout(AUDIO_FADE_OUT)
            except AttributeError:
                # Fallback: skip fade out if method not available
                print("⚠️  Fade out method not available in this MoviePy version")
                print("   Continuing without fade out effect...")
            except Exception as e:
                print(f"⚠️  Could not apply fade out: {e}")
                print("   Continuing without fade out effect...")
        
        # Handle different scenarios
        if audio_duration <= video_duration:
            # Audio is shorter or equal to video - add audio to beginning, keep original video length
            print("🎯 Audio is shorter than video - adding audio to beginning, keeping original video length")
            
            # Create a silent audio track for the remaining video duration
            from moviepy.audio.AudioClip import AudioClip
            silent_duration = video_duration - audio_duration
            silent_audio = AudioClip(lambda t: 0, duration=silent_duration)
            
            # Combine audio with silent track
            final_audio = CompositeAudioClip([audio_clip, silent_audio.set_start(audio_duration)])
            
        else:
            # Audio is longer than video - trim audio to video length
            print("🎯 Audio is longer than video - trimming audio to video length")
            final_audio = audio_clip.subclip(0, video_duration)
        
        # Set the audio to the video
        print("🔗 Combining video with audio...")
        final_video = video_clip.set_audio(final_audio)
        
        # Write the output file
        print(f"💾 Writing output file: {output_path}")
        
        # Set quality parameters based on VIDEO_QUALITY setting
        quality_params = {
            "low": {"bitrate": "500k", "audio_bitrate": "128k"},
            "medium": {"bitrate": "1000k", "audio_bitrate": "192k"},
            "high": {"bitrate": "2000k", "audio_bitrate": "320k"}
        }
        
        params = quality_params.get(VIDEO_QUALITY, quality_params["medium"])
        
        # Write video with progress callback
        def progress_callback(t):
            if VERBOSE_OUTPUT:
                progress = (t / video_duration) * 100
                print(f"⏳ Progress: {progress:.1f}% ({format_duration(t)}/{format_duration(video_duration)})")
        
        # Write video with compatibility handling for different MoviePy versions
        try:
            # Try with progress_bar parameter (newer versions)
            final_video.write_videofile(
                output_path,
                codec=VIDEO_CODEC,
                audio_codec=AUDIO_CODEC,
                bitrate=params["bitrate"],
                audio_bitrate=params["audio_bitrate"],
                verbose=VERBOSE_OUTPUT,
                logger=None,
                progress_bar=not VERBOSE_OUTPUT
            )
        except TypeError as e:
            if "progress_bar" in str(e):
                # Fallback: write without progress_bar parameter (older versions)
                print("⚠️  Using compatibility mode for write_videofile (no progress bar)")
                final_video.write_videofile(
                    output_path,
                    codec=VIDEO_CODEC,
                    audio_codec=AUDIO_CODEC,
                    bitrate=params["bitrate"],
                    audio_bitrate=params["audio_bitrate"],
                    verbose=VERBOSE_OUTPUT,
                    logger=None
                )
            else:
                # Re-raise if it's a different TypeError
                raise e
        
        # Clean up
        video_clip.close()
        audio_clip.close()
        final_video.close()
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"✅ Video-audio combination completed successfully!")
        print(f"⏱️  Processing time: {processing_time:.1f} seconds")
        return True
        
    except Exception as e:
        print(f"❌ Error during video-audio combination: {e}")
        return False


def main():
    """Main function."""
    print("🌙 Moon Home - Advanced Video-Audio Combiner")
    print("=" * 60)
    
    # Check if moviepy is installed
    try:
        import moviepy
        print(f"✅ MoviePy version: {moviepy.__version__}")
    except ImportError:
        print("❌ Error: MoviePy is not installed!")
        print("Please install it with: pip install moviepy")
        sys.exit(1)
    
    # Display configuration
    print(f"\n⚙️  Configuration:")
    print(f"   Video file: {VIDEO_FILE}")
    print(f"   Audio file: {AUDIO_FILE}")
    print(f"   Output file: {OUTPUT_FILE}")
    print(f"   Audio volume: {AUDIO_VOLUME}x")
    print(f"   Video quality: {VIDEO_QUALITY}")
    print(f"   Audio fade in: {AUDIO_FADE_IN}s")
    print(f"   Audio fade out: {AUDIO_FADE_OUT}s")
    
    # Check input files
    print("\n📁 Checking input files...")
    video_path = check_file_exists(VIDEO_FILE, "Video")
    audio_path = check_file_exists(AUDIO_FILE, "Audio")
    
    if not video_path or not audio_path:
        print("\n❌ Cannot proceed without both video and audio files.")
        print("Please check the file paths in video_audio_config.py")
        sys.exit(1)
    
    # Get file information
    print("\n📊 File Information:")
    video_info = get_file_info(video_path)
    audio_info = get_file_info(audio_path)
    
    if video_info:
        print(f"   Video: {video_info['size_mb']} MB, modified: {video_info['modified']}")
    if audio_info:
        print(f"   Audio: {audio_info['size_mb']} MB, modified: {audio_info['modified']}")
    
    # Check if output file already exists
    if os.path.exists(OUTPUT_FILE):
        if AUTO_OVERWRITE:
            print(f"⚠️  Output file '{OUTPUT_FILE}' exists. Auto-overwriting...")
        else:
            response = input(f"\n⚠️  Output file '{OUTPUT_FILE}' already exists. Overwrite? (y/N): ")
            if response.lower() != 'y':
                print("❌ Operation cancelled.")
                sys.exit(0)
    
    # Combine video and audio
    success = combine_video_audio(video_path, audio_path, OUTPUT_FILE)
    
    if success:
        # Get output file information
        output_info = get_file_info(OUTPUT_FILE)
        if output_info:
            print(f"\n📊 Output file: {OUTPUT_FILE}")
            print(f"   Size: {output_info['size_mb']} MB")
            print(f"   Created: {output_info['modified']}")
        
        print(f"\n🎉 Success! Combined video saved as: {OUTPUT_FILE}")
        print("🌙 Ready for use in your Moon Home project!")
        
        # Suggest next steps
        print(f"\n💡 Next steps:")
        print(f"   1. Test the output video: {OUTPUT_FILE}")
        print(f"   2. If satisfied, you can move it to your project's images folder")
        print(f"   3. Update your HTML templates to use the new video")
        
    else:
        print("\n❌ Failed to combine video and audio.")
        sys.exit(1)


if __name__ == "__main__":
    main()
