import cv2
import os
import time
import numpy as np
import pygame
import tempfile
from moviepy.editor import VideoFileClip

def convert_frame_to_ascii(frame, width=80):
    """
    Convert a frame to ASCII art using a character set based on brightness
    Optimized for speed
    """
    ascii_chars = " .:-=+*#%@"
    
    # Calculate height maintaining aspect ratio
    height = int(frame.shape[0] * width / frame.shape[1] / 2) 
    if height == 0:
        height = 1
        
    # Resize frame
    resized_frame = cv2.resize(frame, (width, height))

    # Convert to grayscale if needed
    if len(resized_frame.shape) > 2:
        gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
    else:
        gray_frame = resized_frame
    
    # Optimized conversion using numpy
    normalized = gray_frame.astype(np.float32) / 255.0
    char_indices = (normalized * (len(ascii_chars) - 1)).astype(np.int32)
    
    # Convert to ASCII string efficiently
    ascii_frame = ""
    for row in char_indices:
        ascii_frame += ''.join(ascii_chars[i] for i in row) + "\n"
    
    return ascii_frame

def extract_and_play_audio_with_moviepy(video_path):
    """
    Extract audio from video using moviepy and play with pygame
    """
    try:
        # Create temporary audio file
        temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_audio.close()
        
        # Extract audio using moviepy
        video = VideoFileClip(video_path)
        if video.audio is not None:
            video.audio.write_audiofile(temp_audio.name, verbose=False, logger=None)
            video.close()
            
            # Play with pygame
            pygame.mixer.init()
            pygame.mixer.music.load(temp_audio.name)
            pygame.mixer.music.play()
            
            return temp_audio.name
        else:
            print("No audio track found in video.")
            video.close()
            return None
            
    except Exception as e:
        print(f"MoviePy audio error: {e}")
        return None

def play_video_in_terminal(video_path, width=80, fps=30):
    """
    Play a video in the terminal using ASCII characters with synchronized audio
    """
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file '{video_path}'.")
        return
    
    # Get video properties dynamically
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_duration = total_frames / video_fps if video_fps > 0 else 0
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Use provided FPS if video FPS is invalid, otherwise use video FPS
    if video_fps <= 0 or fps > 0:
        display_fps = fps if fps > 0 else 30
        frame_delay = 1.0 / display_fps
        print(f"Using custom FPS: {display_fps}")
    else:
        display_fps = video_fps
        frame_delay = 1.0 / video_fps
        print(f"Using video FPS: {display_fps}")
    
    print(f"Video: {video_width}x{video_height}, {video_duration:.2f}s, {total_frames} frames")
    
    # Try to play audio using MoviePy + Pygame
    audio_playing = False
    temp_audio_file = None
    
    print("Attempting to play audio...")
    temp_audio_file = extract_and_play_audio_with_moviepy(video_path)
    if temp_audio_file:
        print("✓ Audio playing with MoviePy + Pygame...")
        audio_playing = True
    else:
        print("✗ No audio track found. Playing video without audio.")
    
    try:
        # Start timing for synchronization
        start_time = time.time()
        frame_count = 0
        
        print(f"Starting playback...")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Calculate when this frame should be displayed based on display FPS
            target_time = frame_count * frame_delay
            
            # Convert frame to ASCII
            ascii_art = convert_frame_to_ascii(frame, width)
            
            # Wait until it's time to show this frame
            current_time = time.time() - start_time
            if current_time < target_time:
                time.sleep(target_time - current_time)
            
            # Display the frame
            os.system('cls' if os.name == 'nt' else 'clear')
            print(ascii_art)
            
            frame_count += 1
            
            # Show progress every 30 frames or every 1 second, whichever is less
            progress_interval = min(30, max(1, int(display_fps)))
            if frame_count % progress_interval == 0:
                current_video_time = frame_count / display_fps
                current_real_time = time.time() - start_time
                sync_diff = current_real_time - current_video_time
                print(f"Frame {frame_count}/{total_frames} - Time: {current_video_time:.1f}s - Sync: {sync_diff:+.3f}s")
            
    except KeyboardInterrupt:
        print("\nVideo playback interrupted.")
    
    finally:
        if audio_playing and temp_audio_file:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            # Clean up temporary audio file
            try:
                os.unlink(temp_audio_file)
            except:
                pass
        cap.release()

if __name__ == "__main__":
    print("ASCII Art Video Player with Audio")
    print("=" * 40)
    
    video_path = input("Enter the path to the video file: ").strip()
    
    if not video_path:
        print("No video file specified. Exiting.")
        exit(1)
    
    try:
        width = int(input("Enter terminal width (default 80): ") or "80")
    except ValueError:
        width = 80

    try:
        fps_input = input("Enter FPS (default: use video FPS): ").strip()
        fps = int(fps_input) if fps_input else 0
    except ValueError:
        fps = 0
    
    print(f"\nPlaying: {video_path}")
    print(f"Terminal width: {width}")
    print(f"FPS: {'Video FPS' if fps == 0 else fps}")
    print("Press Ctrl+C to stop playback")
    print("-" * 40)
    
    play_video_in_terminal(video_path, width, fps)