# YouTube Manim

Repository for mathematical animations created with [Manim](https://github.com/3b1b/manim) for YouTube videos.

## About

This repository contains Python-based animation scripts using Manim, a Python library for creating mathematical animations. These animations are created for YouTube video production.

## Technology Stack

- **Python** (99.6%) - Main language for Manim scripts
- **Shell** (0.4%) - Build and utility scripts

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Manim library
- FFmpeg (required by Manim for video rendering)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/sjchem/youtube-manim.git
cd youtube-manim
```

2. Install Manim:
```bash
pip install manim
```

3. Install FFmpeg (if not already installed):
   - **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Usage

To render animations from this repository:

```bash
manim -pql scene_file.py SceneName
```

- `-p`: Play the video after rendering
- `-q`: Quality (l = low, m = medium, h = high)
- `-l`: Low quality (fastest rendering)

## Project Structure

```
youtube-manim/
├── README.md
├── scenes/          # Animation scene files
└── ...
```

## Contributing

Feel free to explore the code and animations. If you'd like to contribute or have suggestions, feel free to open an issue or pull request.

## License

This project is provided as-is for educational and entertainment purposes.

## Resources

- [Manim Documentation](https://docs.manim.community/)
- [3Blue1Brown Manim GitHub](https://github.com/3b1b/manim)
- [Manim Community](https://www.manim.community/)

---

Created for YouTube video content.
