import unittest
from pathlib import Path
import tempfile
import shutil
import os
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from tablet_sync_epub.app import EBookSyncApp, KOREADER_SYS, ANDROID_SYS
import tkinter as tk

class TestEBookSyncLogic(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = EBookSyncApp(self.root)
        self.test_dir = Path(tempfile.mkdtemp())
        self.ref_dir = self.test_dir / "ref"
        self.device_dir = self.test_dir / "device"
        
        self.ref_dir.mkdir()
        self.device_dir.mkdir(parents=True)
        
        self.app.ref_path.set(str(self.ref_dir))
        self.app.koreader_path.set(str(self.device_dir))

    def tearDown(self):
        self.root.destroy()
        shutil.rmtree(self.test_dir)

    def test_koreader_path_validation(self):
        self.assertTrue(self.app.is_koreader_path_valid(str(self.device_dir)))
        self.assertFalse(self.app.is_koreader_path_valid("Z:/NonExistentPath"))

    def test_get_files_and_dirs(self):
        (self.device_dir / "book1.epub").touch()
        (self.device_dir / "book1.epub.dir").mkdir()
        
        files, dirs = self.app.get_files_and_dirs(self.device_dir)
        
        self.assertIn("book1.epub", files)
        self.assertIn("book1.epub.dir", dirs)

if __name__ == "__main__":
    unittest.main()
