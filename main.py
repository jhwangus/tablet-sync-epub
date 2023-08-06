# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os, sys, getopt, shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from ttkwidgets import CheckboxTreeview

global kindle_path, ref_path, window
kindle_sys = 1
android_sys = 2

def set_path(sys_type):
    # Allow user to select a directory and store it in global var
    # called android_path
    global android_path, kindle_path
    if sys_type == kindle_sys:
        filename = filedialog.askdirectory(initialdir=kindle_path.get())
        kindle_path.set(filename)
    else:
        filename = filedialog.askdirectory(initialdir=android_path.get())
        android_path.set(filename)

def set_ref_path():
    # Allow user to select a directory and store it in global var
    # called ref_path
    global ref_path
    filename = filedialog.askdirectory(initialdir=ref_path.get())
    ref_path.set(filename)

def is_kindle_path(str):
    # print(str)
    if str.find(':/DK_Documents/') != -1:
        return True
    else:
        return False

def kindle_path_error(str):
    messagebox.showerror('Kindle Path Error', str + ' is not a path to a DK-Kindle.\n\n' +
                         'The path should be underneath DK_Documents folder.\n\nPlease set Kindle Path correctly!')

def separate_listdir(kp):
    file_list = []
    dir_list = []
    dir_str ='.dir'
    for f in os.listdir(kp):
        t = kp+'/'+f
        if os.path.isfile(t):
            file_list.append(f)
        elif os.path.isdir(t) and f.endswith(dir_str):
            dir_list.append(f)
    return (file_list, dir_list)


def del_file_dir(ct, sys_type):
    c_list = ct.get_checked()
    if sys_type == kindle_sys:
        kp = kindle_path.get()
    else:
        kp = android_path.get()
    for id in c_list:
        name = kp + '/' + ct.item(id, option='text')
        if name.endswith('.dir'):
            shutil.rmtree(name, ignore_errors=True)
        else:
            os.remove(name)
        print(name)
        ct.delete(id)
    print('Done cleaning read books.')
    return

def select_del_list(s_list,sys_type):
    global top
    win = Toplevel(top)
    win.title("Delete files and book directories")
    ct = CheckboxTreeview(win, show='tree') # hide tree headings
    ct.grid(column=0, row=0)
    style = ttk.Style(win)
    # remove the indicator in the treeview
    style.layout('Checkbox.Treeview.Item',
             [('Treeitem.padding',
               {'sticky': 'nswe',
                'children': [('Treeitem.image', {'side': 'left', 'sticky': ''}),
                             ('Treeitem.focus', {'side': 'left', 'sticky': '',
                                                 'children': [('Treeitem.text',
                                                               {'side': 'left', 'sticky': ''})]})]})])
    # make it look more like a listbox
    style.configure('Checkbox.Treeview', borderwidth=1, relief='sunken')
    # add items in treeview
    for value in s_list:
        print(value)
        id = ct.insert('', 'end', text=value)
        ct.change_state(id, 'checked')
    ttk.Button(win, text = 'Cancel', command = win.destroy).grid(column=0, row=1)
    ttk.Button(win, text = 'Delete', command = lambda: del_file_dir(ct, sys_type)).grid(column=1, row=1)

def clean_read_books(sys_type):
    global kindle_path, android_path
    read_list = []
    file_list = []
    dir_list = []
    del_list = []
    rp = ref_path.get()
    if sys_type == kindle_sys:
        kp = kindle_path.get()
        if not is_kindle_path(kp):
            kindle_path_error(kp)
            return
    else:
        kp = android_path.get()
    for f in os.listdir(rp):
        t = rp + '/' + f
        if f.startswith('V_') and os.path.isfile(t):
            read_list.append(f.removeprefix('V_'))
    file_list, dir_list = separate_listdir(kp)
    for f in read_list:
        if f in file_list:
            t = kp + '/' + f
            del_list.append(f)
            # os.remove(t)
            # print('--' + kp + '/' + f)
        if f + '.dir' in dir_list:
            del_list.append(f + '.dir')
            # shutil.rmtree(kp + '/' + f + '.dir', ignore_errors=True)
            # print('--' + kp + '/' + f + '.dir')
    select_del_list(del_list, sys_type)

def clean_book_dir(sys_type):
    global kindle_path
    if sys_type != kindle_sys:
        return
    file_list = []
    dir_list = []
    dir_str = '.dir'
    kp = kindle_path.get()
    if not is_kindle_path(kp):
        kindle_path_error(kp)
        return
    file_list, dir_list = separate_listdir(kp)
    for d in dir_list:
        if d.removesuffix(dir_str) not in file_list:
            shutil.rmtree(kp+'/'+d, ignore_errors=True)
            print('--'+ kp + '/' + d)
    print('Done cleaning .dir.')

def sync_file(ct, sys_type):
    c_list = ct.get_checked()
    if sys_type == kindle_sys:
        kp = kindle_path.get()
    else:
        kp = android_path.get()
    rp = ref_path.get()
    for id in c_list:
        k_name = kp + '/' + ct.item(id, option='text')
        r_name = rp + '/' + ct.item(id, option='text')
        shutil.copyfile(r_name, k_name)
        print(k_name)
        ct.delete(id)
    print('Done transferring.')
    return

def select_sync_list(s_list, sys_type):
    global top
    if sys_type == kindle_sys:
        txt_str = "Transfer files to Kindle"
    else:
        txt_str = "Transfer files to Android"
    win = Toplevel(top)
    win.title(txt_str)
    ct = CheckboxTreeview(win, show='tree') # hide tree headings
    ct.grid(column=0, row=0)
    style = ttk.Style(win)
    # remove the indicator in the treeview
    style.layout('Checkbox.Treeview.Item',
             [('Treeitem.padding',
               {'sticky': 'nswe',
                'children': [('Treeitem.image', {'side': 'left', 'sticky': ''}),
                             ('Treeitem.focus', {'side': 'left', 'sticky': '',
                                                 'children': [('Treeitem.text',
                                                               {'side': 'left', 'sticky': ''})]})]})])
    # make it look more like a listbox
    style.configure('Checkbox.Treeview', borderwidth=1, relief='sunken')
    # add items in treeview
    for value in s_list:
        id = ct.insert('', 'end', text=value)
        ct.change_state(id, 'checked')

    ttk.Button(win, text = 'Cancel', command = win.destroy).grid(column=0, row=1)
    ttk.Button(win, text = 'Sync', command = lambda: sync_file(ct, sys_type)).grid(column=1, row=1)

def sync_books(sys_type):
    global kingle_path, android_path
    ref_list = []
    file_list = []
    dir_list = []
    sync_list = []

    rp = ref_path.get()
    if sys_type == kindle_sys:
        kp = kindle_path.get()
        if not is_kindle_path(kp):
            kindle_path_error(kp)
            return
    else:
        kp = android_path.get()

    for f in os.listdir(rp):
        t = rp + '/' + f
        if not f.startswith('V_') and f.endswith('.epub') and os.path.isfile(t):
            ref_list.append(f)
    file_list, dir_list = separate_listdir(kp)
    for f in ref_list:
        if not (f in file_list):
            t = kp + '/' + f
            sync_list.append(f)
    select_sync_list(sync_list, sys_type)
    return

def create_path_frame(container, sys_type):
    global kindle_path, android_path, ref_path

    if sys_type == kindle_sys:
        device_path = 'H:/DK_Documents'
        kindle_path = tk.StringVar(container, device_path)
    else:
        device_path = 'H:/Books'
        android_path = tk.StringVar(container, device_path)
    ebook_path = 'F:/Documents/eBook'
    ref_path = tk.StringVar(container, ebook_path)

    frame = ttk.Frame(container)
    frame.columnconfigure(0, weight = 1)
    frame.columnconfigure(1, weight= 3)

    # desktop_path = os.path.join(os.path.expanduser('~'), "Desktop")
    ttk.Label(frame, text='Android path:').grid(column=0, row=0, sticky=tk.W)
    if sys_type == kindle_sys:
        txt_path = ttk.Entry(frame, width=60, textvariable=kindle_path)
    else:
        txt_path = ttk.Entry(frame, width=60, textvariable=android_path)
    txt_path.grid(column=1, row=0, sticky=tk.W)

    ttk.Label(frame, text='Ref. path:').grid(column=0, row=1, sticky=tk.W)
    txt_ref_path = ttk.Entry(frame, width=60, textvariable = ref_path)
    txt_ref_path.grid(column = 1, row=1, sticky=tk.W)
    for widget in frame.winfo_children():
        widget.grid(padx=10, pady=7)
    return frame

def create_button_frame(container, sys_type):
    frame = ttk.Frame(container)
    # frame.columnconfigure(0, weight = 1)
    if sys_type == kindle_sys:
        txt_str = 'Set Kindle Path'
    else:
        txt_str = 'Set Android Path'
    ttk.Button(frame, text=txt_str, command=lambda: set_path(sys_type)).grid(column=0, row=0)
    ttk.Button(frame, text = 'Set Ref. Path', command = set_ref_path).grid(column=0, row=1)
    ttk.Button(frame, text = 'Clean read books', command = lambda:clean_read_books(sys_type)).grid(column=0, row=2)
    if sys_type == kindle_sys:
        ttk.Button(frame, text = 'Clean book .dir', command = lambda:clean_book_dir(sys_type)).grid(column=0, row=3)
    ttk.Button(frame, text = 'Sync books', command = lambda: sync_books(sys_type)).grid(column=0, row=4)
    ttk.Button(frame, text = 'Exit', command = container.destroy).grid(column=0, row=5)
    for widget in frame.winfo_children():
        widget.grid(padx=10, pady=7)
        widget.configure(width=20)
    return frame

def create_win(sys_type):
    win = Toplevel(top)
    if sys_type == kindle_sys:
        win.title("Kindle Duokan Sync")
    else:
        win.title("Android MoonReader Sync")
    style = ttk.Style(win)
    path_frame = create_path_frame(win, sys_type)
    path_frame.grid(row=0, column=0, sticky='ne', pady=10)
    # path_frame.place(x=20, y=20)
    # path_frame.grid(row=0, column=0)
    button_frame = create_button_frame(win, sys_type)
    # button_frame.place(x=480, y=20)
    button_frame.grid(row=0, column=1, rowspan=2, pady=10)
    # win.grab_set()

def main(argv):
    global top
    myargs = []
    try:
        opts, args = getopt.getopt(argv, "aehvilrp:t:q:")
    except getopt.GetoptError:
        usage()
        sys.exit(2)
        
    top = tk.Tk()
    top.title("eBook Synch")
    top.resizable(0, 0)
    # windows only (remove the minimize/maximize button)
    top.attributes('-toolwindow', True)
    frame = ttk.Frame(top)
    ttk.Button(frame, text = 'Kindle 多看', command = lambda: create_win(kindle_sys)).grid(column=0, row=0)
    ttk.Button(frame, text = 'Android MoonReader', command = lambda: create_win(android_sys)).grid(column=1, row=0)
    frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10)
    for widget in frame.winfo_children():
        widget.grid(padx=10, pady=7)
        widget.configure(width=24)

    top.mainloop()

# provide alternative execution path
if __name__ == "__main__":
    main(sys.argv[1:])
