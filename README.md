# 🎬 demo-gif-cli

Hey! This is a simple terminal tool to convert your screen recordings (MP4, MOV, WebM, etc.) into high-quality, smooth GIFs. It's built to make demo GIFs for GitHub READMEs or docs without bloated web tools, watermarks, or giant file sizes.

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
* **Optional Post-Optimization (`gifsicle`)**: If you have `gifsicle` installed on your system, the tool automatically runs a post-processing pass using lossy LZW compression (`gifsicle -O3 --lossy=80`), reducing file sizes by an extra 20–40% without losing quality.

---

## 🚀 Installation and quick start

### 1. Grab the tools
You need `ffmpeg`, `ffprobe`, and `gifski` in your system's path. Optionally, install `gifsicle` for extra compression:

* **macOS / Linux (Homebrew)**:
  ```bash
  brew install ffmpeg gifski gifsicle
  ```
* **Debian / Ubuntu**:
  ```bash
  sudo apt update && sudo apt install ffmpeg gifsicle
  sudo snap install gifski # or cargo install gifski
  ```
* **Fedora**:
  ```bash
  sudo dnf install ffmpeg gifski gifsicle
  ```

### 2. Global Installation
You can install this tool globally so it's available as the command `demo-gif` from any folder in your terminal. Run this from the root of the project:
```bash
pip install .
# or if you prefer isolated user installations:
pipx install .
```

---

## 📖 Usage

### Option A: Interactive Wizard (Just run it)
If you run the command without any arguments, it starts the interactive path prompts:
```bash
demo-gif
```

Follow the prompts to select your file (press `Tab` to autocomplete), destination, and custom FPS/width settings.

### Option B: Script Mode (CLI Arguments)
To bypass the prompts completely (ideal for CLI scripting and workflows), pass the `--input` flag:
```bash
demo-gif -i screen_recording.mp4
```

#### Available Flags:
| Flag | Alternative | Description | Default |
|------|-------------|-------------|---------|
| `-i` | `--input` | Path to the source video file | (Required for CLI mode) |
| `-o` | `--output` | Destination path for the `.gif` | `[input_filename].gif` |
| `-f` | `--fps` | Target frame rate (1-60) | `15` |
| `-w` | `--width` | Max width in pixels or `original` | `800` |
| `-q` | `--quality` | Compression quality for `gifski` (1-100) | `90` |
| `--no-optimize` | | Disable optional `gifsicle` optimization pass | `False` |

#### Example:
```bash
demo-gif -i recording.mov -o demo.gif -f 12 -w 640 -q 85
```

---

## 📄 License
This project is under the MIT License - feel free to use it however you want.
