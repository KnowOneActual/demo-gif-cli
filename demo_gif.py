#!/usr/bin/env python3
"""
demo_gif.py
Interactive and CLI utility to convert video recordings into high-quality demo GIFs.
Optimized for GitHub and web documentation using FFmpeg and Gifski.

Author: Antigravity AV Assistant
"""

import os
import sys
import glob
import json
import shlex
import shutil
import argparse
import tempfile
import subprocess

# Terminal Colors
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Configure path autocompletion using readline
try:
    import readline

    def path_completer(text, state):
        expanded_text = os.path.expanduser(text)
        matches = glob.glob(expanded_text + '*')
        
        results = []
        for match in matches:
            if text.startswith('~'):
                home = os.path.expanduser('~')
                display_path = match.replace(home, '~', 1)
            else:
                display_path = match
                
            if os.path.isdir(match) and not display_path.endswith('/'):
                display_path += '/'
            results.append(display_path)
            
        return results[state] if state < len(results) else None

    # Tab autocompletion setup (Space removed from delimiters to support paths with spaces)
    readline.set_completer_delims('\t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(path_completer)
except ImportError:
    pass


def print_header():
    print(f"\n{BOLD}{CYAN}=================================================={RESET}")
    print(f"{BOLD}{CYAN}🎥    HIGH-QUALITY GIF DEMO GENERATOR (CLI)       🎥{RESET}")
    print(f"{BOLD}{CYAN}=================================================={RESET}")
    print(f"Powered by {BOLD}FFmpeg{RESET} (frames & scaling) & {BOLD}Gifski{RESET} (quality palette compression)\n")


def check_dependencies():
    """Verify that FFmpeg, FFprobe, and Gifski are installed."""
    missing = []
    for cmd in ["ffmpeg", "ffprobe", "gifski"]:
        if not shutil.which(cmd):
            missing.append(cmd)
            
    if missing:
        print(f"{RED}{BOLD}❌ Missing required dependencies:{RESET}")
        for cmd in missing:
            print(f"  - {BOLD}{cmd}{RESET}")
        print(f"\n{YELLOW}Please install them before running this script.{RESET}")
        print(f"On Debian/Ubuntu: {BOLD}sudo apt update && sudo apt install ffmpeg{RESET} and install gifski via Cargo or Snap.")
        print(f"On Fedora:        {BOLD}sudo dnf install ffmpeg gifski{RESET}")
        print(f"On macOS/Linux:   {BOLD}brew install ffmpeg gifski{RESET}")
        sys.exit(1)


def format_size(size_bytes):
    if size_bytes <= 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB")
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


def verify_and_probe_video(file_path):
    """Verify file existence and query metadata using ffprobe."""
    if not os.path.exists(file_path):
        return False, "File does not exist."
    if os.path.isdir(file_path):
        return False, "Path points to a directory, not a file."
        
    cmd = [
        "ffprobe", 
        "-v", "error", 
        "-select_streams", "v:0", 
        "-show_entries", "stream=width,height,duration,r_frame_rate,codec_name", 
        "-show_entries", "format=duration",
        "-of", "json", 
        file_path
    ]
    
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(res.stdout)
        
        if "streams" not in data or len(data["streams"]) == 0:
            return False, "No valid video stream found in this file."
            
        stream = data["streams"][0]
        
        # Parse duration
        duration_str = stream.get("duration")
        if not duration_str and "format" in data:
            duration_str = data["format"].get("duration")
        duration = float(duration_str) if duration_str else None
        
        # Parse frame rate
        fps_str = stream.get("r_frame_rate", "0/0")
        if "/" in fps_str:
            num, den = map(int, fps_str.split("/"))
            fps = round(num / den, 2) if den != 0 else 0
        else:
            fps = float(fps_str)
            
        metadata = {
            "width": stream.get("width"),
            "height": stream.get("height"),
            "duration": duration,
            "fps": fps,
            "codec": stream.get("codec_name")
        }
        return True, metadata
    except subprocess.CalledProcessError as e:
        return False, f"ffprobe could not read the file: {e.stderr.strip()}"
    except Exception as e:
        return False, f"Metadata analysis failed: {str(e)}"


def prompt_input_file():
    """Prompt the user for a valid input video file with tab autocomplete."""
    while True:
        path_input = input(f"{BOLD}Step 1: Enter path to input video file (Tab to autocomplete):{RESET}\n> ").strip()
        if not path_input:
            continue
            
        resolved_path = os.path.abspath(os.path.expanduser(path_input))
        success, info = verify_and_probe_video(resolved_path)
        
        if success:
            print(f"\n{GREEN}✓ Valid video file loaded!{RESET}")
            print(f"  {BOLD}Codec:{RESET}      {info['codec']}")
            print(f"  {BOLD}Resolution:{RESET} {info['width']}x{info['height']}")
            if info['duration']:
                print(f"  {BOLD}Duration:{RESET}   {info['duration']:.2f} seconds")
            if info['fps']:
                print(f"  {BOLD}Frame Rate:{RESET} {info['fps']} FPS")
            print(f"  {BOLD}File Size:{RESET}  {format_size(os.path.getsize(resolved_path))}\n")
            return resolved_path, info
        else:
            print(f"{RED}❌ Error: {info}{RESET}\n")


def prompt_output_file(input_path):
    """Prompt for output file path, defaulting to input filename + .gif."""
    dir_name, file_name = os.path.split(input_path)
    base_name, _ = os.path.splitext(file_name)
    default_output = os.path.join(dir_name, f"{base_name}.gif")
    
    while True:
        print(f"{BOLD}Step 2: Specify output GIF destination path:{RESET}")
        print(f"  [Default: {default_output}]")
        output_input = input("> ").strip()
            
        if not output_input:
            resolved_output = default_output
        else:
            resolved_output = os.path.abspath(os.path.expanduser(output_input))
            if not resolved_output.lower().endswith('.gif'):
                resolved_output += '.gif'
                
        # Create parent directory if it doesn't exist
        out_dir = os.path.dirname(resolved_output)
        if out_dir and not os.path.exists(out_dir):
            create = input(f"Directory '{out_dir}' does not exist. Create it? [Y/n]: ").strip().lower()
            if create != 'n':
                try:
                    os.makedirs(out_dir, exist_ok=True)
                except Exception as e:
                    print(f"{RED}Failed to create directory: {e}. Please enter another path.{RESET}")
                    continue
            else:
                continue
                
        return resolved_output


def prompt_settings(video_info):
    """Prompt for FPS, width, and quality settings."""
    # 1. FPS
    while True:
        try:
            fps_input = input(f"{BOLD}Step 3: Target frame rate (FPS) [Default: 15, range: 1-60]:{RESET} ").strip()
            if not fps_input:
                fps = 15
                break
            fps = int(fps_input)
            if 1 <= fps <= 60:
                break
            print(f"{YELLOW}Please enter an integer between 1 and 60.{RESET}")
        except ValueError:
            print(f"{YELLOW}Please enter a valid integer.{RESET}")
            
    # 2. Width (safely query original width)
    orig_width = video_info.get("width")
    if orig_width is None:
        orig_width = 800
    else:
        try:
            orig_width = int(orig_width)
        except (ValueError, TypeError):
            orig_width = 800

    default_width = min(800, orig_width)
    while True:
        try:
            width_input = input(f"{BOLD}Step 4: Maximum width in pixels (or 'original') [Default: {default_width}px]:{RESET} ").strip()
            if not width_input:
                width = default_width
                break
            if width_input.lower() == 'original':
                width = orig_width
                break
            width = int(width_input)
            if width > 0:
                break
            print(f"{YELLOW}Please enter a positive integer.{RESET}")
        except ValueError:
            print(f"{YELLOW}Please enter a valid integer or 'original'.{RESET}")
            
    # 3. Quality
    while True:
        try:
            quality_input = input(f"{BOLD}Step 5: Gifski compression quality (1-100) [Default: 90]:{RESET} ").strip()
            if not quality_input:
                quality = 90
                break
            quality = int(quality_input)
            if 1 <= quality <= 100:
                break
            print(f"{YELLOW}Please enter an integer between 1 and 100.{RESET}")
        except ValueError:
            print(f"{YELLOW}Please enter a valid integer.{RESET}")
            
    return {
        "fps": fps,
        "width": width,
        "quality": quality
    }


def optimize_with_gifsicle(gif_path):
    """Post-process optimization using gifsicle if available on the system."""
    if not shutil.which("gifsicle"):
        return False, "gifsicle is not installed."
        
    print(f"{CYAN}Running gifsicle post-optimization...{RESET}")
    temp_gif = gif_path + ".tmp"
    cmd = ["gifsicle", "-O3", "--lossy=80", "-o", temp_gif, gif_path]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if not os.path.exists(temp_gif):
            return False, "gifsicle finished but temporary file was not created."
            
        orig_size = os.path.getsize(gif_path)
        opt_size = os.path.getsize(temp_gif)
        
        if opt_size < orig_size:
            shutil.move(temp_gif, gif_path)
            saved = orig_size - opt_size
            percent = (saved / orig_size) * 100
            print(f"{GREEN}✓ Gifsicle compression saved {format_size(saved)} ({percent:.1f}% reduction){RESET}")
            return True, opt_size
        else:
            os.remove(temp_gif)
            print(f"{YELLOW}Note: gifsicle ran but did not reduce size further.{RESET}")
            return True, orig_size
    except Exception as e:
        if os.path.exists(temp_gif):
            os.remove(temp_gif)
        print(f"{RED}Warning: gifsicle optimization failed: {e}{RESET}")
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(
        description="Convert video screen recordings into high-quality demo GIFs."
    )
    parser.add_argument("-i", "--input", help="Path to input video file (triggers non-interactive mode)")
    parser.add_argument("-o", "--output", help="Path to output GIF file (defaults to input base name + .gif)")
    parser.add_argument("-f", "--fps", type=int, default=15, help="Target frame rate (default: 15)")
    parser.add_argument("-w", "--width", help="Max width in pixels (e.g., 800) or 'original' (default: 800)")
    parser.add_argument("-q", "--quality", type=int, default=90, help="Gifski quality 1-100 (default: 90)")
    parser.add_argument("--no-optimize", action="store_true", help="Bypass optional gifsicle post-optimization")
    
    args = parser.parse_args()
    
    try:
        check_dependencies()
        
        # Check if we should run in interactive mode (no input argument provided)
        interactive = (args.input is None)
        
        if interactive:
            print_header()
            input_path, video_info = prompt_input_file()
            output_path = prompt_output_file(input_path)
            settings = prompt_settings(video_info)
            optimize_gifsicle = not args.no_optimize
        else:
            input_path = os.path.abspath(os.path.expanduser(args.input))
            success, video_info = verify_and_probe_video(input_path)
            if not success:
                print(f"{RED}❌ Error: {video_info}{RESET}")
                sys.exit(1)
                
            # Parse output
            if args.output:
                output_path = os.path.abspath(os.path.expanduser(args.output))
                if not output_path.lower().endswith('.gif'):
                    output_path += '.gif'
            else:
                dir_name, file_name = os.path.split(input_path)
                base_name, _ = os.path.splitext(file_name)
                output_path = os.path.join(dir_name, f"{base_name}.gif")
                
            # Parse settings
            fps = args.fps
            if not (1 <= fps <= 60):
                print(f"{RED}❌ Error: FPS must be between 1 and 60.{RESET}")
                sys.exit(1)
                
            quality = args.quality
            if not (1 <= quality <= 100):
                print(f"{RED}❌ Error: Quality must be between 1 and 100.{RESET}")
                sys.exit(1)
                
            orig_width = video_info.get("width", 800)
            if args.width:
                if args.width.lower() == 'original':
                    width = orig_width
                else:
                    try:
                        width = int(args.width)
                        if width <= 0:
                            raise ValueError
                    except ValueError:
                        print(f"{RED}❌ Error: Width must be a positive integer or 'original'.{RESET}")
                        sys.exit(1)
            else:
                width = min(800, orig_width)
                
            settings = {
                "fps": fps,
                "width": width,
                "quality": quality
            }
            optimize_gifsicle = not args.no_optimize
            
        # Build scaling filter
        # trunc(...) ensures width and height scale to even numbers, which is essential for yuv420p
        scale_filter = f"scale='trunc(min({settings['width']},iw)/2)*2:-2'"
        
        # Construct FFmpeg command
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-vf", scale_filter,
            "-pix_fmt", "yuv420p",
            "-r", str(settings["fps"]),
            "-f", "yuv4mpegpipe",
            "-"
        ]
        
        # Construct Gifski command
        gifski_cmd = [
            "gifski",
            "-o", output_path,
            "--fps", str(settings["fps"]),
            "--quality", str(settings["quality"]),
            "-"
        ]
        
        # In interactive mode, preview conversion plan and request confirmation
        if interactive:
            print(f"\n{BOLD}{CYAN}=================================================={RESET}")
            print(f"{BOLD}🛠  CONVERSION PLAN{RESET}")
            print(f"{BOLD}{CYAN}=================================================={RESET}")
            print(f"  {BOLD}Input:{RESET}   {input_path}")
            print(f"  {BOLD}Output:{RESET}  {output_path}")
            print(f"  {BOLD}FPS:{RESET}     {settings['fps']}")
            print(f"  {BOLD}Width:{RESET}   {settings['width']}px (max)")
            print(f"  {BOLD}Quality:{RESET} {settings['quality']}")
            print(f"  {BOLD}Pipeline command:{RESET}")
            print(f"    {shlex.join(ffmpeg_cmd)} | {shlex.join(gifski_cmd)}")
            print(f"{CYAN}=================================================={RESET}\n")
            
            confirm = input(f"{BOLD}Start conversion? [Y/n]:{RESET} ").strip().lower()
            if confirm == 'n':
                print("Conversion cancelled.")
                sys.exit(0)
                
            print(f"\n{CYAN}Encoding GIF (this may take a few seconds)...{RESET}")
            
        # Run conversion
        with tempfile.TemporaryFile() as ffmpeg_err_file:
            ffmpeg_proc = subprocess.Popen(
                ffmpeg_cmd, 
                stdout=subprocess.PIPE, 
                stderr=ffmpeg_err_file, 
                text=False
            )
            
            gifski_proc = subprocess.Popen(
                gifski_cmd, 
                stdin=ffmpeg_proc.stdout, 
                stderr=None
            )
            
            ffmpeg_proc.stdout.close()
            gifski_proc.wait()
            ffmpeg_proc.wait()
            
            ffmpeg_err_file.seek(0)
            ffmpeg_err = ffmpeg_err_file.read()
            
        if gifski_proc.returncode == 0 and ffmpeg_proc.returncode == 0:
            orig_size = os.path.getsize(input_path)
            gif_size = os.path.getsize(output_path)
            
            print(f"\n{GREEN}{BOLD}✓ Success! GIF created successfully.{RESET}")
            print(f"  {BOLD}Output File:{RESET} {output_path}")
            print(f"  {BOLD}Original Size:{RESET} {format_size(orig_size)}")
            print(f"  {BOLD}GIF Size:{RESET}      {format_size(gif_size)} ({(gif_size / orig_size) * 100:.1f}% of original size)")
            
            # Gifsicle optimization
            if optimize_gifsicle and shutil.which("gifsicle"):
                success, size_res = optimize_with_gifsicle(output_path)
                if success:
                    gif_size = size_res
            elif not args.no_optimize and not shutil.which("gifsicle") and interactive:
                print(f"\n{YELLOW}Tip: Install 'gifsicle' to enable further post-processing compression!{RESET}")
                
            print(f"\n{YELLOW}Tip: You can now drag and drop this GIF directly into GitHub Markdown!{RESET}\n")
        else:
            print(f"\n{RED}❌ Error occurred during conversion.{RESET}")
            if ffmpeg_proc.returncode != 0:
                print(f"{RED}FFmpeg failed with return code {ffmpeg_proc.returncode}:{RESET}")
                print(ffmpeg_err.decode('utf-8', errors='replace').strip())
            if gifski_proc.returncode != 0:
                print(f"{RED}Gifski failed with return code {gifski_proc.returncode}.{RESET}")
                sys.exit(1)
                
    except (KeyboardInterrupt, EOFError):
        print("\n\nAborted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}❌ Failed to execute conversion pipeline: {str(e)}{RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
