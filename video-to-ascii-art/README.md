# ASCII Art Video Player with Audio

A Python script that converts video files to ASCII art and plays them in the terminal with synchronized audio.

## Features

- **ASCII Art Conversion**: Converts video frames to ASCII characters based on brightness
- **Audio Playback**: Synchronized audio using MoviePy + Pygame
- **Dynamic Synchronization**: Automatically adapts to any video's FPS and duration
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Optimized Performance**: Fast ASCII conversion with NumPy
- **Clean Code**: Minimal dependencies, easy to maintain

## Installation

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

1. Activate the virtual environment:
```bash
venv\Scripts\activate
```

2. Run the script:
```bash
python ascii_video_player.py
```

3. Enter the path to your video file when prompted
4. Set terminal width (default: 80)
5. Set FPS (default: use video FPS)

## How It Works

### Audio Processing
- **MoviePy**: Extracts audio from video files to temporary WAV format
- **Pygame**: Plays the extracted audio with precise timing
- **Synchronization**: Keeps audio and video perfectly in sync using frame-based timing

### Video Processing
- **OpenCV**: Reads video frames and extracts properties (FPS, duration, resolution)
- **NumPy**: Optimized ASCII conversion for fast performance
- **Dynamic Timing**: Automatically calculates frame delays based on video FPS

## Requirements

### Core Dependencies
- **Python 3.7+**
- **OpenCV** (opencv-python) - Video processing
- **NumPy** - Fast array operations for ASCII conversion
- **Pygame** - Audio playback
- **MoviePy** - Audio extraction from videos

### Installation
All dependencies are listed in `requirements.txt` and can be installed with:
```bash
pip install -r requirements.txt
```

## Supported Video Formats

The player supports all video formats that OpenCV can read:
- **MP4** (H.264, H.265)
- **AVI** (various codecs)
- **MOV** (QuickTime)
- **MKV** (Matroska)
- **WebM**
- **FLV**
- And many more...

## Controls

- **Ctrl+C**: Stop playback
- **Enter**: Use default values for prompts
- **Terminal Width**: Adjust ASCII resolution (higher = better quality, slower)
- **FPS**: Override video FPS (0 = use video's native FPS)

## Troubleshooting

### No Audio
- Ensure your video file has an audio track
- Check system audio settings and volume
- Verify MoviePy is properly installed
- Try a different video file to test

### Poor ASCII Quality
- Increase terminal width for better resolution (try 120-150)
- Use a monospace font in your terminal (Consolas, Courier New)
- Adjust terminal size for optimal display
- Ensure terminal supports Unicode characters

### Performance Issues
- Reduce terminal width (try 60-80)
- Lower FPS setting (try 15-30)
- Use smaller video files or shorter clips
- Close other applications to free up system resources

### Synchronization Issues
- The script automatically detects video FPS and syncs accordingly
- If audio/video drift occurs, try restarting the script
- Ensure your system can handle the video's native FPS

## Example

```bash
(venv) PS C:\path\to\project> python ascii_video_player.py
ASCII Art Video Player with Audio
========================================
Enter the path to the video file: vid.mp4
Enter terminal width (default 80): 100
Enter FPS (default: use video FPS): 

Playing: vid.mp4
Terminal width: 100
FPS: Video FPS
Press Ctrl+C to stop playback
----------------------------------------
Using video FPS: 60.0
Video: 700x784, 13.67s, 820 frames
Attempting to play audio...
✓ Audio playing with MoviePy + Pygame...
Starting playback...
Frame 60/820 - Time: 1.0s - Sync: +0.002s
Frame 120/820 - Time: 2.0s - Sync: +0.001s
[ASCII art displays with synchronized audio]
```

## Project Structure

```
assci-art/
├── ascii_video_player.py    # Main script
├── requirements.txt         # Dependencies
├── README.md               # Documentation
├── venv/                   # Virtual environment
└── vid.mp4                 # Test video (optional)
```

## License

This project is open source and available under the MIT License.
