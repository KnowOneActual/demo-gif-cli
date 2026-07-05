# Contributing to demo-gif-cli

Thanks for checking out the project! Contributions are welcome. Here is a quick guide to help you set up your local development environment, run tests, and contribute changes.

---

## 🛠️ Development setup

### 1. Requirements
Ensure you have Python 3.8+ and the following media utilities installed on your system:
- **FFmpeg & FFprobe**
- **Gifski**
- **Gifsicle** (optional, for extra compression checks)

### 2. Local environment setup
Clone the repository and set up a Python virtual environment:
```bash
git clone https://github.com/KnowOneActual/demo-gif-cli.git
cd demo-gif-cli
python -m venv .venv
source .venv/bin/activate
```

Install the package locally in editable/development mode:
```bash
pip install -e .
```

---

## 🧪 Testing

We use Python's built-in `unittest` framework. You can run all tests in the suite using:

```bash
python -m unittest discover tests
```

Always make sure all tests are passing before submitting a change!

---

## 🔍 Style and review guidelines

- **No Slop**: Keep prose simple, direct, and free of corporate jargon or padding.
- **Dependency Discipline**: Avoid adding external Python libraries. The tool is designed to run using Python's standard library and external CLI binaries.
- **Security Check**: Always use list-based arguments without `shell=True` when invoking subprocesses to prevent command injection vulnerabilities. Ensure output paths and prints use `shlex.join` to handle space characters safely.
- **Subprocess Safety**: Never wait on a stdout-only process while neglecting its stderr pipe. Write stderr streams to files (e.g. `tempfile.TemporaryFile`) to avoid OS buffer deadlocks.
