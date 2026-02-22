import unittest
from pathlib import Path
import tempfile
import shutil
import os
import sys

# Add src to path so we can import EBookSyncApp (though it's a GUI class, we can test some methods)
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from main import EBookSyncApp, KINDLE_SYS, ANDROID_SYS
import tkinter as tk

class TestEBookSyncLogic(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = EBookSyncApp(self.root)
        self.test_dir = Path(tempfile.mkdtemp())
        self.ref_dir = self.test_dir / "ref"
        self.device_dir = self.test_dir / "device" / "DK_Documents"
        
        self.ref_dir.mkdir()
        self.device_dir.mkdir(parents=True)
        
        self.app.ref_path.set(str(self.ref_dir))
        self.app.kindle_path.set(str(self.device_dir))

    def tearDown(self):
        self.root.destroy()
        shutil.rmtree(self.test_dir)

    def test_kindle_path_validation(self):
        self.assertTrue(self.app.is_kindle_path_valid("H:/DK_Documents"))
        self.assertTrue(self.app.is_kindle_path_valid("C:/SomePath/DK_Documents/Other"))
        self.assertFalse(self.app.is_kindle_path_valid("C:/SomePath/Books"))

    def test_get_files_and_dirs(self):
        (self.device_dir / "book1.epub").touch()
        (self.device_dir / "book1.epub.dir").mkdir()
        (self.device_dir / "other_dir").mkdir()
        
        files, dirs = self.app.get_files_and_dirs(self.device_dir)
        
        self.assertIn("book1.epub", files)
        self.assertIn("book1.epub.dir", dirs)
        self.assertNotIn("other_dir", dirs) # only .dir directories should be returned

if __name__ == "__main__":
    unittest.main()
