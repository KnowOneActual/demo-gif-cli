# 🎬 demo-gif-cli

This is a simple terminal tool to convert your screen recordings (MP4, MOV, WebM, etc.) into high-quality, smooth GIFs. It's built to make demo GIFs for GitHub READMEs or docs without bloated web tools, watermarks, or giant file sizes.

It automates a neat pipeline using `ffmpeg` and `gifski`:
```bash
ffmpeg -i input.mp4 -pix_fmt yuv420p -r 15 -f yuv4mpegpipe - | gifski -o output.gif -
```

---

## 🤔 Why use this? (And why is it better?)

If you've ever tried to make a demo GIF for a repository, you've probably run into two problems:
1. **The "256 Color" limit**: Standard GIF encoders make text look blurry and colors look dithered and washed out.
2. **Huge file sizes**: High-resolution screen recordings converted straight to GIF can easily end up being 50MB+, which is way too heavy for a web page.

Here is why this tool makes things easier:

* **Insane Quality (`gifski`)**: `gifski` uses smart color quantization. Your GIFs will look crisp, colors will stay true, and text remains clean and readable.
* **No Disk Mess (Piping)**: We stream raw frames directly through system memory, keeping your disk clean and avoiding thousands of temporary PNG files.
* **Auto-Downscaling**: We default to `800px` width and `15 FPS`. Downscaling first cuts the data stream by **over 80%**, making conversion twice as fast.
* **Typo Safety (Verification)**: The tool runs `ffprobe` first to check if your video is valid. It prints the size and duration, so you don't waste time on a typo.
* **Tab Autocomplete**: Real-world path typing is slow. We set up `readline` so you can press `Tab` to autocomplete paths and folders.

---

## 🚀 Quick Start

### 1. Grab the tools
You need `ffmpeg`, `ffprobe`, and `gifski` in your system's path:

* **macOS / Linux (Homebrew)**:
  ```bash
  brew install ffmpeg gifski
  ```
* **Debian / Ubuntu**:
  ```bash
  sudo apt update && sudo apt install ffmpeg
  sudo snap install gifski # or cargo install gifski
  ```
* **Fedora**:
  ```bash
  sudo dnf install ffmpeg gifski
  ```

### 2. Run the script
Clone the repo, make the script executable, and run it:
```bash
chmod +x demo_gif.py
./demo_gif.py
```

### 3. How it looks in action
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
[12/186] Frame 12... 

✓ Success! GIF created successfully.
  Output File: ~/Downloads/gorae_demo.gif
  Original Size: 3.10 MB
  GIF Size:      5.45 MB (175.8% of original size)
```

---

## 📄 License
This project is under the MIT License - feel free to use it however you want.
