# 🎬 demo-gif-cli

`demo-gif-cli` is an interactive terminal application designed to convert video recordings (MP4, MOV, WebM, etc.) into high-quality, smooth demo GIFs optimized for GitHub readmes, documentation, and web sharing.

It automates the YUV4MPEG2 frame pipeline using **FFmpeg** and **Gifski**:
```bash
ffmpeg -i input.mp4 -pix_fmt yuv420p -r 15 -f yuv4mpegpipe - | gifski -o output.gif -
```

---

## ✨ Features

- **Tab Autocompletion**: Integrated file path autocompletion using Python's `readline` library.
- **Dependency Checking**: Verifies that `ffmpeg`, `ffprobe`, and `gifski` are installed in your `$PATH`.
- **Validation**: Probes the video using `ffprobe` to verify the codec, resolution, frame rate, and readability before conversion.
- **Optimal Scaling**: Automatically downscales to a recommended width (e.g. `800px` default for READMEs) using a smart FFmpeg filter (`scale='min(800,iw):-2'`), which preserves aspect ratios, ensures height divisibility by 2, and cuts down raw transfer data by **over 80%** (making encoding twice as fast).
- **Clean CLI Console**: Redirects verbose decoding logs to keep the display clean, showing only `gifski`'s single-line progress indicator.
- **Analytics**: Displays a summary comparing the output GIF size and format to the original source.

---

## 🚀 Installation

### 1. Prerequisites
Ensure you have Python 3 installed. You also need to install the following media tools:

#### On macOS/Linux (via Homebrew):
```bash
brew install ffmpeg gifski
```

#### On Debian/Ubuntu:
```bash
sudo apt update && sudo apt install ffmpeg
# For gifski, install via cargo or snap:
cargo install gifski
# or
sudo snap install gifski
```

#### On Fedora:
```bash
sudo dnf install ffmpeg gifski
```

### 2. Download and Setup
Clone the repository (or copy the files) and make the script executable:
```bash
git clone https://github.com/your-username/demo-gif-cli.git
cd demo-gif-cli
chmod +x demo_gif.py
```

---

## 📖 Usage

Run the utility:
```bash
./demo_gif.py
```

Follow the interactive prompts:
1. **Source Video**: Enter the path to your recording (e.g., `~/Downloads/demo.mp4`). You can use the **`Tab`** key to autocomplete file paths.
2. **Output GIF Destination**: Press `Enter` to save the GIF next to the source video, or specify a custom path.
3. **Settings Customization**: Customize frame rate (default: `15 FPS`), maximum width (default: `800px`), and quality (default: `90`), or press `Enter` to accept all recommended defaults.
4. **Conversion**: Review the conversion plan and type `y` to start the encode.

```
Step 1: Enter path to input video file (Tab to autocomplete):
> ~/Downloads/gorae_demo.mp4

✓ Valid video file loaded!
  Codec:      h264
  Resolution: 1920x1080
  Duration:   12.40 seconds
  Frame Rate: 60.0 FPS
  File Size:  3.10 MB

Step 2: Specify output GIF destination path:
  [Default: ~/Downloads/gorae_demo.gif]
> 

Step 3: Target frame rate (FPS) [Default: 15, range: 1-60]: 15
Step 4: Maximum width in pixels (or 'original') [Default: 800px]: 800
Step 5: Gifski compression quality (1-100) [Default: 90]: 90

==================================================
🛠️  CONVERSION PLAN
==================================================
  Input:   ~/Downloads/gorae_demo.mp4
  Output:  ~/Downloads/gorae_demo.gif
  FPS:     15
  Width:   800px (max)
  Quality: 90
  Pipeline command:
    ffmpeg -y -i ~/Downloads/gorae_demo.mp4 -vf scale='min(800,iw):-2' -pix_fmt yuv420p -r 15 -f yuv4mpegpipe - | gifski -o ~/Downloads/gorae_demo.gif --fps 15 --quality 90 -
==================================================

Start conversion? [Y/n]: y

Encoding GIF (this may take a few seconds)...
[12/186] Frame 12... [Progress updates dynamically]

✓ Success! GIF created successfully.
  Output File: ~/Downloads/gorae_demo.gif
  Original Size: 3.10 MB
  GIF Size:      5.45 MB (175.8% of original size)
```

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
