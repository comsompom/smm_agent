#!/usr/bin/env python3
"""
Video Combiner Script for Moon Home Project
Combines multiple MP4 video files into a single video file.

This script combines all scene_*.mp4 files from templates/images/ into one combined video.
"""

import os
import sys
from moviepy.editor import VideoFileClip, concatenate_videoclips
import argparse


def get_video_files(directory):
    """
    Get all MP4 video files from the specified directory.
    Returns a sorted list of video file paths.
    """
    video_extensions = ['.mp4', '.MP4']
    video_files = []
    
    for file in os.listdir(directory):
        if any(file.endswith(ext) for ext in video_extensions):
            video_files.append(os.path.join(directory, file))
    
    # Sort files to ensure consistent order (scene_200, scene_250, etc.)
    video_files.sort()
    return video_files


def combine_videos(video_files, output_path, method='concatenate'):
    """
    Combine multiple video files into one.
    
    Args:
        video_files (list): List of video file paths
        output_path (str): Output file path
        method (str): Combination method ('concatenate' or 'merge')
    """
    if not video_files:
        print("❌ No video files found!")
        return False
    
    print(f"📹 Found {len(video_files)} video files:")
    for i, video_file in enumerate(video_files, 1):
        print(f"   {i}. {os.path.basename(video_file)}")
    
    try:
        print("\n🎬 Loading video clips...")
        clips = []
        
        for video_file in video_files:
            print(f"   Loading: {os.path.basename(video_file)}")
            clip = VideoFileClip(video_file)
            clips.append(clip)
        
        print(f"\n🔗 Combining videos using {method} method...")
        
        if method == 'concatenate':
            # Concatenate videos one after another
            final_clip = concatenate_videoclips(clips, method="compose")
        else:
            # For future: could implement side-by-side or other merging methods
            final_clip = concatenate_videoclips(clips, method="compose")
        
        print(f"💾 Writing combined video to: {output_path}")
        final_clip.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            verbose=False,
            logger=None
        )
        
        # Clean up
        for clip in clips:
            clip.close()
        final_clip.close()
        
        print(f"✅ Successfully created combined video: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error combining videos: {str(e)}")
        return False


def get_video_info(video_file):
    """
    Get basic information about a video file.
    """
    try:
        clip = VideoFileClip(video_file)
        info = {
            'duration': clip.duration,
            'fps': clip.fps,
            'size': clip.size,
            'filename': os.path.basename(video_file)
        }
        clip.close()
        return info
    except Exception as e:
        print(f"❌ Error reading video info for {video_file}: {str(e)}")
        return None


def main():
    """
    Main function to combine videos.
    """
    parser = argparse.ArgumentParser(description='Combine MP4 video files into one video')
    parser.add_argument('--input-dir', '-i', 
                       default='sources',
                       help='Input directory containing video files (default: sources)')
    parser.add_argument('--output', '-o',
                       default='sources/combined_scenes.mp4',
                       help='Output video file path (default: sources/combined_scenes.mp4)')
    parser.add_argument('--method', '-m',
                       choices=['concatenate'],
                       default='concatenate',
                       help='Combination method (default: concatenate)')
    parser.add_argument('--info', action='store_true',
                       help='Show video information before combining')
    
    args = parser.parse_args()
    
    # Check if input directory exists
    if not os.path.exists(args.input_dir):
        print(f"❌ Input directory does not exist: {args.input_dir}")
        sys.exit(1)
    
    # Get video files
    video_files = get_video_files(args.input_dir)
    
    if not video_files:
        print(f"❌ No MP4 video files found in: {args.input_dir}")
        sys.exit(1)
    
    # Show video information if requested
    if args.info:
        print("📊 Video Information:")
        print("-" * 50)
        total_duration = 0
        for video_file in video_files:
            info = get_video_info(video_file)
            if info:
                print(f"📹 {info['filename']}")
                print(f"   Duration: {info['duration']:.2f} seconds")
                print(f"   FPS: {info['fps']}")
                print(f"   Size: {info['size'][0]}x{info['size'][1]}")
                print(f"   File: {video_file}")
                print()
                total_duration += info['duration']
        
        print(f"📈 Total duration: {total_duration:.2f} seconds ({total_duration/60:.2f} minutes)")
        print("-" * 50)
        print()
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Combine videos
    success = combine_videos(video_files, args.output, args.method)
    
    if success:
        print(f"\n🎉 Video combination completed successfully!")
        print(f"📁 Output file: {args.output}")
        
        # Show final video info
        if os.path.exists(args.output):
            final_info = get_video_info(args.output)
            if final_info:
                print(f"\n📊 Final Video Information:")
                print(f"   Duration: {final_info['duration']:.2f} seconds ({final_info['duration']/60:.2f} minutes)")
                print(f"   FPS: {final_info['fps']}")
                print(f"   Size: {final_info['size'][0]}x{final_info['size'][1]}")
                print(f"   File size: {os.path.getsize(args.output) / (1024*1024):.2f} MB")
    else:
        print("\n❌ Video combination failed!")
        sys.exit(1)


if __name__ == "__main__":
    print("🚀 Moon Home Video Combiner")
    print("=" * 40)
    main()
