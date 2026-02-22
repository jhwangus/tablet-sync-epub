import os
import sys
import shutil
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from ttkwidgets import CheckboxTreeview

# System Type Constants
KINDLE_SYS = 1
ANDROID_SYS = 2
SETTINGS_PATH = Path(".gemini/settings.json")

class EBookSyncApp:
    def __init__(self, root):
        self.root = root
        self.root.title("eBook Synch")
        self.root.resizable(False, False)
        
        # Windows only: remove minimize/maximize buttons
        if sys.platform == "win32":
            self.root.attributes('-toolwindow', True)

        # Default paths
        self.defaults = {
            "kindle_path": "H:/DK_Documents",
            "android_path": "H:/Books",
            "ref_path": "F:/Documents/eBook"
        }
        self.load_settings()

        self.kindle_path = tk.StringVar(value=self.settings.get("kindle_path", self.defaults["kindle_path"]))
        self.android_path = tk.StringVar(value=self.settings.get("android_path", self.defaults["android_path"]))
        self.ref_path = tk.StringVar(value=self.settings.get("ref_path", self.defaults["ref_path"]))

        self.setup_main_ui()

    def load_settings(self):
        self.settings = {}
        if SETTINGS_PATH.exists():
            try:
                with open(SETTINGS_PATH, 'r') as f:
                    self.settings = json.load(f)
            except Exception as e:
                print(f"Error loading settings: {e}")

    def save_settings(self):
        self.settings.update({
            "kindle_path": self.kindle_path.get(),
            "android_path": self.android_path.get(),
            "ref_path": self.ref_path.get()
        })
        SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(SETTINGS_PATH, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def setup_main_ui(self):
        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, padx=10, pady=10)

        kindle_btn = ttk.Button(
            frame, 
            text='Kindle 多看', 
            command=lambda: self.create_sync_window(KINDLE_SYS)
        )
        kindle_btn.grid(column=0, row=0, padx=10, pady=7)
        kindle_btn.configure(width=24)

        android_btn = ttk.Button(
            frame, 
            text='Android MoonReader', 
            command=lambda: self.create_sync_window(ANDROID_SYS)
        )
        android_btn.grid(column=1, row=0, padx=10, pady=7)
        android_btn.configure(width=24)

    def set_device_path(self, sys_type):
        current_path = self.kindle_path.get() if sys_type == KINDLE_SYS else self.android_path.get()
        filename = filedialog.askdirectory(initialdir=current_path)
        if filename:
            if sys_type == KINDLE_SYS:
                self.kindle_path.set(filename)
            else:
                self.android_path.set(filename)
            self.save_settings()

    def set_ref_path(self):
        filename = filedialog.askdirectory(initialdir=self.ref_path.get())
        if filename:
            self.ref_path.set(filename)
            self.save_settings()

    def is_kindle_path_valid(self, path_str):
        return '/DK_Documents/' in path_str or path_str.endswith('/DK_Documents')

    def show_kindle_path_error(self, path_str):
        messagebox.showerror(
            'Kindle Path Error', 
            f'{path_str} is not a valid path to a DK-Kindle.\n\n'
            'The path should be the DK_Documents folder.\n\nPlease set Kindle Path correctly!'
        )

    def get_files_and_dirs(self, path):
        p = Path(path)
        if not p.exists():
            return [], []
        files = [f.name for f in p.iterdir() if f.is_file()]
        dirs = [d.name for d in p.iterdir() if d.is_dir() and d.name.endswith('.dir')]
        return files, dirs

    def delete_selected(self, ct, sys_type, window):
        checked_items = ct.get_checked()
        base_path = Path(self.kindle_path.get() if sys_type == KINDLE_SYS else self.android_path.get())
        
        for item_id in checked_items:
            item_name = ct.item(item_id, option='text')
            target_path = base_path / item_name
            
            if target_path.is_dir():
                shutil.rmtree(target_path, ignore_errors=True)
            elif target_path.exists():
                target_path.unlink()
            
            print(f"Deleted: {target_path}")
            ct.delete(item_id)
        
        messagebox.showinfo("Done", "Selected items deleted successfully.")
        window.destroy()

    def sync_selected(self, ct, sys_type, window):
        checked_items = ct.get_checked()
        target_base = Path(self.kindle_path.get() if sys_type == KINDLE_SYS else self.android_path.get())
        ref_base = Path(self.ref_path.get())
        
        for item_id in checked_items:
            item_name = ct.item(item_id, option='text')
            src_file = ref_base / item_name
            dest_file = target_base / item_name
            
            shutil.copyfile(src_file, dest_file)
            print(f"Synced: {dest_file}")
            ct.delete(item_id)
            
        messagebox.showinfo("Done", "Selected items transferred successfully.")
        window.destroy()

    def create_list_window(self, title, items, action_func):
        win = tk.Toplevel(self.root)
        win.title(title)
        
        ct = CheckboxTreeview(win, show='tree')
        ct.grid(column=0, row=0, columnspan=2, padx=10, pady=10)
        
        style = ttk.Style(win)
        style.layout('Checkbox.Treeview.Item',
                     [('Treeitem.padding',
                       {'sticky': 'nswe',
                        'children': [('Treeitem.image', {'side': 'left', 'sticky': ''}),
                                     ('Treeitem.focus', {'side': 'left', 'sticky': '',
                                                         'children': [('Treeitem.text',
                                                                       {'side': 'left', 'sticky': ''})]})]})])
        style.configure('Checkbox.Treeview', borderwidth=1, relief='sunken')

        for item in items:
            node_id = ct.insert('', 'end', text=item)
            ct.change_state(node_id, 'checked')

        ttk.Button(win, text='Cancel', command=win.destroy).grid(column=0, row=1, pady=10)
        ttk.Button(win, text='Proceed', command=lambda: action_func(ct, win)).grid(column=1, row=1, pady=10)

    def clean_read_books(self, sys_type):
        ref_p = Path(self.ref_path.get())
        device_p_str = self.kindle_path.get() if sys_type == KINDLE_SYS else self.android_path.get()
        
        if sys_type == KINDLE_SYS and not self.is_kindle_path_valid(device_p_str):
            self.show_kindle_path_error(device_p_str)
            return

        read_prefixes = [f.name.removeprefix('V_') for f in ref_p.iterdir() if f.is_file() and f.name.startswith('V_')]
        device_files, device_dirs = self.get_files_and_dirs(device_p_str)
        
        del_list = []
        for book in read_prefixes:
            if book in device_files:
                del_list.append(book)
            if f"{book}.dir" in device_dirs:
                del_list.append(f"{book}.dir")

        if not del_list:
            messagebox.showinfo("Info", "No read books found to clean.")
            return

        self.create_list_window(
            "Delete Read Books", 
            del_list, 
            lambda ct, win: self.delete_selected(ct, sys_type, win)
        )

    def clean_empty_dirs(self, sys_type):
        if sys_type != KINDLE_SYS:
            return
        
        device_p_str = self.kindle_path.get()
        if not self.is_kindle_path_valid(device_p_str):
            self.show_kindle_path_error(device_p_str)
            return

        files, dirs = self.get_files_and_dirs(device_p_str)
        orphaned_dirs = [d for d in dirs if d.removesuffix('.dir') not in files]

        if not orphaned_dirs:
            messagebox.showinfo("Info", "No orphaned .dir directories found.")
            return

        for d in orphaned_dirs:
            shutil.rmtree(Path(device_p_str) / d, ignore_errors=True)
            print(f"Removed orphaned dir: {d}")
        
        messagebox.showinfo("Done", f"Cleaned {len(orphaned_dirs)} orphaned directories.")

    def sync_books(self, sys_type):
        ref_p = Path(self.ref_path.get())
        device_p_str = self.kindle_path.get() if sys_type == KINDLE_SYS else self.android_path.get()

        if sys_type == KINDLE_SYS and not self.is_kindle_path_valid(device_p_str):
            self.show_kindle_path_error(device_p_str)
            return

        ref_files = [f.name for f in ref_p.iterdir() if f.is_file() and not f.name.startswith('V_') and f.suffix == '.epub']
        device_files, _ = self.get_files_and_dirs(device_p_str)
        
        sync_list = [f for f in ref_files if f not in device_files]

        if not sync_list:
            messagebox.showinfo("Info", "All books are already synchronized.")
            return

        self.create_list_window(
            "Sync New Books", 
            sync_list, 
            lambda ct, win: self.sync_selected(ct, sys_type, win)
        )

    def create_sync_window(self, sys_type):
        win = tk.Toplevel(self.root)
        win.title("Kindle Duokan Sync" if sys_type == KINDLE_SYS else "Android MoonReader Sync")

        # Path Frame
        path_frame = ttk.Frame(win)
        path_frame.grid(row=0, column=0, sticky='nw', padx=10, pady=10)

        device_label = 'Kindle path:' if sys_type == KINDLE_SYS else 'Android path:'
        device_var = self.kindle_path if sys_type == KINDLE_SYS else self.android_path

        ttk.Label(path_frame, text=device_label).grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(path_frame, width=50, textvariable=device_var).grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)

        ttk.Label(path_frame, text='Ref. path:').grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(path_frame, width=50, textvariable=self.ref_path).grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)

        # Button Frame
        btn_frame = ttk.Frame(win)
        btn_frame.grid(row=0, column=1, sticky='ne', padx=10, pady=10)

        actions = [
            (f"Set {'Kindle' if sys_type == KINDLE_SYS else 'Android'} Path", lambda: self.set_device_path(sys_type)),
            ("Set Ref. Path", self.set_ref_path),
            ("Clean read books", lambda: self.clean_read_books(sys_type)),
        ]

        if sys_type == KINDLE_SYS:
            actions.append(("Clean book .dir", lambda: self.clean_empty_dirs(sys_type)))

        actions.extend([
            ("Sync books", lambda: self.sync_books(sys_type)),
            ("Exit", lambda: (self.save_settings(), win.destroy()))
        ])

        for i, (text, cmd) in enumerate(actions):
            btn = ttk.Button(btn_frame, text=text, command=cmd)
            btn.grid(column=0, row=i, padx=5, pady=5, sticky='ew')
            btn.configure(width=20)

def main():
    root = tk.Tk()
    app = EBookSyncApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
