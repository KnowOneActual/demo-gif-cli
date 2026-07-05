# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-04

### Added
- Core pipeline streaming raw video frames from `ffmpeg` directly to `gifski` using `yuv4mpegpipe`.
- Interactive CLI wizard with native directory and file tab autocompletion.
- Full CLI argument support (`-i`, `-o`, `-f`, `-w`, `-q`, `--no-optimize`) for scripting and automation.
- Safe scaling filter using `trunc(min(width,iw)/2)*2:-2` to prevent chroma subsampling errors on odd dimensions.
- Native `gifsicle` post-processing integration for additional lossy LZW compression.
- Package packaging configuration in `pyproject.toml` to support global installation via pip/pipx.
- Unit test suite under `tests/` covering formatting, verification, paths, and process errors.
- Clean README documentation, MIT license, and git configuration.
