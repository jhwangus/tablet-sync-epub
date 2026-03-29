import shutil
from pathlib import Path

try:
    import win32com.client

    HAS_WIN32COM = True
except ImportError:
    HAS_WIN32COM = False


class DeviceFileSystem:
    """
    Abstracts filesystem operations for standard drives and Android MTP paths.
    MTP virtual nested paths are handled via a custom '[MTP]' prefix.
    """

    def __init__(self, path_str: str):
        self.path_str = path_str
        self.is_shell_path = False
        self.shell = None
        self.shell_folder = None

        if HAS_WIN32COM:
            try:
                self.shell = win32com.client.Dispatch("Shell.Application")

                if self.path_str.startswith("[MTP] "):
                    self.is_shell_path = True
                    parts = self.path_str[6:].split("/")
                    # Top level is This PC (17)
                    curr_folder = self.shell.NameSpace(17)

                    for part in parts:
                        found = False
                        if curr_folder:
                            for item in curr_folder.Items():
                                if item.Name == part:
                                    curr_folder = item.GetFolder
                                    found = True
                                    break
                        if not found:
                            curr_folder = None
                            break

                    if curr_folder:
                        self.shell_folder = curr_folder
                else:
                    # Normal paths mapped to shell (optional mostly for standard paths)
                    folder = self.shell.NameSpace(self.path_str)
                    if folder and (
                        self.path_str.startswith("::{")
                        or "\\?\\usb" in self.path_str.lower()
                    ):
                        self.is_shell_path = True
                        self.shell_folder = folder
            except Exception:
                pass

        # Fallback to standard Path
        if not self.is_shell_path:
            self.path = Path(path_str)

    def exists(self) -> bool:
        if self.is_shell_path:
            return self.shell_folder is not None
        return self.path.exists()

    def get_files_and_dirs(self) -> tuple[list[str], list[str]]:
        if self.is_shell_path and self.shell_folder:
            files = []
            dirs = []
            for item in self.shell_folder.Items():
                if item.IsFolder:
                    if item.Name.endswith(".dir"):
                        dirs.append(item.Name)
                else:
                    files.append(item.Name)
            return files, dirs

        if not self.exists():
            return [], []
        files = [f.name for f in self.path.iterdir() if f.is_file()]
        dirs = [
            d.name
            for d in self.path.iterdir()
            if d.is_dir() and d.name.endswith(".dir")
        ]
        return files, dirs

    def delete_item(self, item_name: str) -> bool:
        if self.is_shell_path and self.shell_folder:
            for item in self.shell_folder.Items():
                if item.Name == item_name:
                    item.InvokeVerb("delete")
                    return True
            return False

        target_path = self.path / item_name
        if target_path.is_dir():
            shutil.rmtree(target_path, ignore_errors=True)
            return True
        elif target_path.exists():
            target_path.unlink()
            return True
        return False

    def copy_file_to(self, src_file: str | Path, dest_name: str) -> bool:
        if self.is_shell_path and self.shell_folder:
            abs_src = str(Path(src_file).resolve())
            self.shell_folder.CopyHere(abs_src, 16)
            return True

        dest_file = self.path / dest_name
        shutil.copyfile(src_file, dest_file)
        return True


def browse_for_device_folder(initial_dir: str = "") -> str:
    if HAS_WIN32COM:
        try:
            shell = win32com.client.Dispatch("Shell.Application")
            # 0x40 = BIF_NEWDIALOGSTYLE
            # 17 = CSIDL_DRIVES (This PC)
            folder = shell.BrowseForFolder(0, "Select Device Path", 0x40, 17)

            if folder:
                path_str = folder.Self.Path
                if path_str.startswith("::{") or "\\?\\usb" in path_str.lower():
                    # It's an MTP device! Build the display hierarchy
                    parts = []
                    curr = folder
                    while curr:
                        parts.insert(0, curr.Title)
                        try:
                            parent = curr.ParentFolder
                            if (
                                not parent
                                or getattr(parent, "Title", None) == curr.Title
                            ):
                                break
                            curr = parent
                        except Exception:
                            break

                    if "This PC" in parts:
                        idx = parts.index("This PC")
                        return "[MTP] " + "/".join(parts[idx + 1 :])
                    else:
                        # Fallback parsing
                        return "[MTP] " + "/".join(parts[-3:])
                else:
                    # Regular drive path
                    return path_str
            return ""
        except Exception as e:
            print(f"Shell.Application error: {e}")

    import tkinter.filedialog

    return tkinter.filedialog.askdirectory(initialdir=initial_dir)
