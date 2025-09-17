#!/usr/bin/env python3
"""
Audio Concatenation Script
==========================

This script concatenates two audio files into one output file.
Supports various audio formats and provides flexible options for audio processing.

Features:
- Concatenate two audio files sequentially
- Support for multiple audio formats (MP3, WAV, M4A, etc.)
- Audio volume adjustment for each file
- Fade in/out effects
- Crossfade between files (optional)
- Quality and bitrate control
- Progress tracking

Usage:
    python concatenate_audio.py

All parameters are configured in the CONFIGURATION section below.

Author: SMM Poster Project
"""

import os
import sys
import time
from pathlib import Path

# MoviePy imports
try:
    from moviepy.editor import AudioFileClip, concatenate_audioclips
    from moviepy.audio.fx import audio_fadein, audio_fadeout
    print("✅ MoviePy imported successfully")
except ImportError as e:
    print(f"❌ Error importing MoviePy: {e}")
    print("Please install MoviePy: pip install moviepy")
    sys.exit(1)

# =============================================================================
# CONFIGURATION - Modify these settings as needed
# =============================================================================

# Input and Output Files
INPUT_AUDIO_FILE_1 = "01.wav"  # Path to first audio file
INPUT_AUDIO_FILE_2 = "02.wav"  # Path to second audio file
OUTPUT_AUDIO_FILE = "result.wav"  # Path to output file

# Audio Processing Settings
VOLUME_1 = 1.0  # Volume multiplier for first file (1.0 = normal, 0.5 = half, 2.0 = double)
VOLUME_2 = 1.0  # Volume multiplier for second file (1.0 = normal, 0.5 = half, 2.0 = double)

# Fade Effects (in seconds, 0 = no fade)
FADE_IN_1 = 0.0   # Fade in duration for first file
FADE_OUT_1 = 0.0  # Fade out duration for first file
FADE_IN_2 = 0.0   # Fade in duration for second file
FADE_OUT_2 = 0.0  # Fade out duration for second file

# Crossfade Settings
CROSSFADE_DURATION = 0.0  # Crossfade duration between files (in seconds, 0 = no crossfade)

# Output Quality Settings
AUDIO_CODEC = "mp3"      # Audio codec: mp3, wav, aac, flac, etc.
AUDIO_BITRATE = "192k"   # Audio bitrate: 128k, 192k, 256k, 320k, etc.

# Display Settings
VERBOSE_OUTPUT = True    # Set to False for minimal output

# =============================================================================
# END CONFIGURATION
# =============================================================================

# Supported audio formats
SUPPORTED_FORMATS = ['.mp3', '.wav', '.m4a', '.aac', '.flac', '.ogg', '.wma']

def format_duration(seconds):
    """Format duration in seconds to MM:SS format"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def validate_audio_file(file_path):
    """Validate that the audio file exists and is supported"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")
    
    file_ext = Path(file_path).suffix.lower()
    if file_ext not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported audio format: {file_ext}. Supported formats: {', '.join(SUPPORTED_FORMATS)}")
    
    return True

def get_audio_info(audio_clip):
    """Get information about an audio clip"""
    return {
        'duration': audio_clip.duration,
        'fps': audio_clip.fps,
        'nchannels': audio_clip.nchannels
    }

def apply_audio_effects(audio_clip, volume=1.0, fade_in=0, fade_out=0):
    """Apply volume adjustment and fade effects to audio clip"""
    # Apply volume adjustment
    if volume != 1.0:
        audio_clip = audio_clip.volumex(volume)
    
    # Apply fade in effect
    if fade_in > 0:
        try:
            audio_clip = audio_clip.fadein(fade_in)
        except AttributeError:
            print(f"⚠️  Fade in effect not available in this MoviePy version")
        except Exception as e:
            print(f"⚠️  Could not apply fade in: {e}")
    
    # Apply fade out effect
    if fade_out > 0:
        try:
            audio_clip = audio_clip.fadeout(fade_out)
        except AttributeError:
            print(f"⚠️  Fade out effect not available in this MoviePy version")
        except Exception as e:
            print(f"⚠️  Could not apply fade out: {e}")
    
    return audio_clip

def concatenate_audio_files(input1, input2, output, 
                          volume1=1.0, volume2=1.0,
                          fade_in1=0, fade_out1=0,
                          fade_in2=0, fade_out2=0,
                          crossfade=0,
                          audio_codec="mp3",
                          audio_bitrate="192k",
                          verbose=True):
    """
    Concatenate two audio files with optional effects
    
    Args:
        input1 (str): Path to first audio file
        input2 (str): Path to second audio file
        output (str): Path to output audio file
        volume1 (float): Volume multiplier for first file (1.0 = normal)
        volume2 (float): Volume multiplier for second file (1.0 = normal)
        fade_in1 (float): Fade in duration for first file (seconds)
        fade_out1 (float): Fade out duration for first file (seconds)
        fade_in2 (float): Fade in duration for second file (seconds)
        fade_out2 (float): Fade out duration for second file (seconds)
        crossfade (float): Crossfade duration between files (seconds)
        audio_codec (str): Audio codec for output
        audio_bitrate (str): Audio bitrate for output
        verbose (bool): Enable verbose output
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    if verbose:
        print("🎵 Audio Concatenation Script")
        print("=" * 50)
        print(f"📁 Input 1: {input1}")
        print(f"📁 Input 2: {input2}")
        print(f"📁 Output: {output}")
        print()
    
    try:
        # Validate input files
        if verbose:
            print("🔍 Validating input files...")
        
        validate_audio_file(input1)
        validate_audio_file(input2)
        
        if verbose:
            print("✅ Input files validated")
        
        # Load audio files
        if verbose:
            print("📥 Loading audio files...")
        
        audio1 = AudioFileClip(input1)
        audio2 = AudioFileClip(input2)
        
        # Get audio information
        info1 = get_audio_info(audio1)
        info2 = get_audio_info(audio2)
        
        if verbose:
            print(f"🎵 Audio 1: {format_duration(info1['duration'])} | {info1['fps']}Hz | {info1['nchannels']} channels")
            print(f"🎵 Audio 2: {format_duration(info2['duration'])} | {info2['fps']}Hz | {info2['nchannels']} channels")
            print()
        
        # Apply effects to first audio
        if verbose and (volume1 != 1.0 or fade_in1 > 0 or fade_out1 > 0):
            print("🎭 Applying effects to first audio...")
        
        audio1_processed = apply_audio_effects(audio1, volume1, fade_in1, fade_out1)
        
        # Apply effects to second audio
        if verbose and (volume2 != 1.0 or fade_in2 > 0 or fade_out2 > 0):
            print("🎭 Applying effects to second audio...")
        
        audio2_processed = apply_audio_effects(audio2, volume2, fade_in2, fade_out2)
        
        # Handle crossfade if requested
        if crossfade > 0:
            if verbose:
                print(f"🔄 Applying {crossfade}s crossfade...")
            
            # For crossfade, we need to overlap the end of audio1 with the start of audio2
            # This is a simplified crossfade implementation
            if crossfade < audio1_processed.duration and crossfade < audio2_processed.duration:
                # Trim the end of audio1 and start of audio2 for crossfade
                audio1_trimmed = audio1_processed.subclip(0, audio1_processed.duration - crossfade/2)
                audio2_trimmed = audio2_processed.subclip(crossfade/2, audio2_processed.duration)
                
                # Concatenate with crossfade
                final_audio = concatenate_audioclips([audio1_trimmed, audio2_trimmed])
            else:
                if verbose:
                    print("⚠️  Crossfade duration too long, using simple concatenation")
                final_audio = concatenate_audioclips([audio1_processed, audio2_processed])
        else:
            # Simple concatenation
            if verbose:
                print("🔗 Concatenating audio files...")
            
            final_audio = concatenate_audioclips([audio1_processed, audio2_processed])
        
        # Get final audio info
        final_info = get_audio_info(final_audio)
        
        if verbose:
            print(f"🎵 Final audio: {format_duration(final_info['duration'])} | {final_info['fps']}Hz | {final_info['nchannels']} channels")
            print()
        
        # Write output file
        if verbose:
            print(f"💾 Writing output file: {output}")
            print(f"🎛️  Codec: {audio_codec} | Bitrate: {audio_bitrate}")
        
        start_time = time.time()
        
        # Write with compatibility handling for different MoviePy versions
        try:
            # Try with progress_bar parameter (newer versions)
            final_audio.write_audiofile(
                output,
                codec=audio_codec,
                bitrate=audio_bitrate,
                verbose=verbose,
                logger=None,
                progress_bar=not verbose
            )
        except TypeError as e:
            if "progress_bar" in str(e):
                # Fallback: write without progress_bar parameter (older versions)
                if verbose:
                    print("⚠️  Using compatibility mode for write_audiofile (no progress bar)")
                final_audio.write_audiofile(
                    output,
                    codec=audio_codec,
                    bitrate=audio_bitrate,
                    verbose=verbose,
                    logger=None
                )
            else:
                # Re-raise if it's a different TypeError
                raise e
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        if verbose:
            print(f"✅ Audio concatenation completed successfully!")
            print(f"⏱️  Processing time: {processing_time:.1f} seconds")
            print(f"📁 Output file: {output}")
        
        # Clean up
        audio1.close()
        audio2.close()
        final_audio.close()
        
        return True
        
    except Exception as e:
        if verbose:
            print(f"❌ Error during audio concatenation: {str(e)}")
        return False

def main():
    """Main function using configuration constants"""
    print("🎵 Audio Concatenation Script")
    print("=" * 50)
    print("📋 Configuration:")
    print(f"   Input 1: {INPUT_AUDIO_FILE_1}")
    print(f"   Input 2: {INPUT_AUDIO_FILE_2}")
    print(f"   Output: {OUTPUT_AUDIO_FILE}")
    print(f"   Volume 1: {VOLUME_1}x")
    print(f"   Volume 2: {VOLUME_2}x")
    print(f"   Fade In 1: {FADE_IN_1}s")
    print(f"   Fade Out 1: {FADE_OUT_1}s")
    print(f"   Fade In 2: {FADE_IN_2}s")
    print(f"   Fade Out 2: {FADE_OUT_2}s")
    print(f"   Crossfade: {CROSSFADE_DURATION}s")
    print(f"   Codec: {AUDIO_CODEC}")
    print(f"   Bitrate: {AUDIO_BITRATE}")
    print()
    
    # Check if input files exist
    if not os.path.exists(INPUT_AUDIO_FILE_1):
        print(f"❌ Error: Input file 1 not found: {INPUT_AUDIO_FILE_1}")
        print("💡 Please update INPUT_AUDIO_FILE_1 in the configuration section")
        sys.exit(1)
    
    if not os.path.exists(INPUT_AUDIO_FILE_2):
        print(f"❌ Error: Input file 2 not found: {INPUT_AUDIO_FILE_2}")
        print("💡 Please update INPUT_AUDIO_FILE_2 in the configuration section")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(OUTPUT_AUDIO_FILE)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        if VERBOSE_OUTPUT:
            print(f"📁 Created output directory: {output_dir}")
    
    # Run concatenation using configuration constants
    success = concatenate_audio_files(
        input1=INPUT_AUDIO_FILE_1,
        input2=INPUT_AUDIO_FILE_2,
        output=OUTPUT_AUDIO_FILE,
        volume1=VOLUME_1,
        volume2=VOLUME_2,
        fade_in1=FADE_IN_1,
        fade_out1=FADE_OUT_1,
        fade_in2=FADE_IN_2,
        fade_out2=FADE_OUT_2,
        crossfade=CROSSFADE_DURATION,
        audio_codec=AUDIO_CODEC,
        audio_bitrate=AUDIO_BITRATE,
        verbose=VERBOSE_OUTPUT
    )
    
    if success:
        print("🎉 Audio concatenation completed successfully!")
        print(f"📁 Output file: {OUTPUT_AUDIO_FILE}")
        sys.exit(0)
    else:
        print("❌ Audio concatenation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
