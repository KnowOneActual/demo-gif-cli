import os
import sys
import unittest
import subprocess
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import demo_gif

class TestDemoGif(unittest.TestCase):
    def test_format_size(self):
        self.assertEqual(demo_gif.format_size(0), "0 B")
        self.assertEqual(demo_gif.format_size(1024), "1.0 KB")
        self.assertEqual(demo_gif.format_size(1048576), "1.0 MB")
        self.assertEqual(demo_gif.format_size(1073741824), "1.0 GB")
        
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('subprocess.run')
    def test_verify_and_probe_video_valid(self, mock_run, mock_isdir, mock_exists):
        mock_exists.return_value = True
        mock_isdir.return_value = False
        
        # Mock ffprobe JSON output
        mock_res = MagicMock()
        mock_res.stdout = '{"streams": [{"width": 1920, "height": 1080, "duration": "10.50", "r_frame_rate": "30/1", "codec_name": "h264"}]}'
        mock_res.returncode = 0
        mock_run.return_value = mock_res
        
        success, info = demo_gif.verify_and_probe_video("dummy.mp4")
        self.assertTrue(success)
        self.assertEqual(info["width"], 1920)
        self.assertEqual(info["height"], 1080)
        self.assertEqual(info["duration"], 10.5)
        self.assertEqual(info["fps"], 30.0)
        self.assertEqual(info["codec"], "h264")

    @patch('os.path.exists')
    def test_verify_and_probe_video_not_found(self, mock_exists):
        mock_exists.return_value = False
        success, err = demo_gif.verify_and_probe_video("nonexistent.mp4")
        self.assertFalse(success)
        self.assertEqual(err, "File does not exist.")

    @patch('os.path.exists')
    @patch('os.path.isdir')
    def test_verify_and_probe_video_is_dir(self, mock_isdir, mock_exists):
        mock_exists.return_value = True
        mock_isdir.return_value = True
        success, err = demo_gif.verify_and_probe_video("some_dir")
        self.assertFalse(success)
        self.assertEqual(err, "Path points to a directory, not a file.")

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('subprocess.run')
    def test_verify_and_probe_video_process_error(self, mock_run, mock_isdir, mock_exists):
        mock_exists.return_value = True
        mock_isdir.return_value = False
        
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd="ffprobe",
            stderr="ffprobe error output"
        )
        
        success, err = demo_gif.verify_and_probe_video("corrupt.mp4")
        self.assertFalse(success)
        self.assertIn("ffprobe could not read the file", err)


if __name__ == "__main__":
    unittest.main()
