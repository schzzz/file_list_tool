# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, messagebox
import os

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_entry.delete(0, tk.END)
        folder_path_entry.insert(0, folder_path)

def list_files():
    folder_path = folder_path_entry.get()
    include_subfolders = include_subfolders_var.get()
    sort_by_name = sort_by_name_var.get()
    sort_by_creation = sort_by_creation_var.get()
    sort_by_modification = sort_by_modification_var.get()
    sort_by_size = sort_by_size_var.get()

    if not folder_path:
        messagebox.showwarning("警告", "請選擇一個資料夾")
        return

    file_list = []
    if include_subfolders:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_list.append(os.path.join(root, file))
    else:
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                file_list.append(file_path)
    
    if sort_by_name:
        file_list.sort()
    elif sort_by_creation:
        file_list.sort(key=lambda x: os.path.getctime(x))
    elif sort_by_modification:
        file_list.sort(key=lambda x: os.path.getmtime(x))
    elif sort_by_size:
        file_list.sort(key=lambda x: os.path.getsize(x))

    result_text.delete(1.0, tk.END)
    for file in file_list:
        result_text.insert(tk.END, file + '\n')

    if export_var.get():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not file_path:
            messagebox.showwarning("警告", "請輸入檔案名稱")
            return
        with open(file_path, "w", encoding="utf-8") as f:
            for file in file_list:
                f.write(file + '\n')
        messagebox.showinfo("導出成功", f"檔案列表已成功導出至 {file_path}")

app = tk.Tk()
app.title("檔案列表工具")

frame = tk.Frame(app)
frame.pack(pady=10)

folder_path_label = tk.Label(frame, text="選擇資料夾：")
folder_path_label.grid(row=0, column=0, padx=5, pady=5)

folder_path_entry = tk.Entry(frame, width=50)
folder_path_entry.grid(row=0, column=1, padx=5, pady=5)

browse_button = tk.Button(frame, text="瀏覽", command=browse_folder)
browse_button.grid(row=0, column=2, padx=5, pady=5)

include_subfolders_var = tk.BooleanVar()
include_subfolders_check = tk.Checkbutton(frame, text="包含子資料夾", variable=include_subfolders_var)
include_subfolders_check.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

sort_by_name_var = tk.BooleanVar()
sort_by_name_check = tk.Checkbutton(frame, text="依名稱排序", variable=sort_by_name_var)
sort_by_name_check.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

sort_by_creation_var = tk.BooleanVar()
sort_by_creation_check = tk.Checkbutton(frame, text="依創建日期排序", variable=sort_by_creation_var)
sort_by_creation_check.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

sort_by_modification_var = tk.BooleanVar()
sort_by_modification_check = tk.Checkbutton(frame, text="依修改日期排序", variable=sort_by_modification_var)
sort_by_modification_check.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

sort_by_size_var = tk.BooleanVar()
sort_by_size_check = tk.Checkbutton(frame, text="依檔案大小排序", variable=sort_by_size_var)
sort_by_size_check.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

export_var = tk.BooleanVar()
export_check = tk.Checkbutton(frame, text="是否將結果另存為新檔", variable=export_var)
export_check.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

list_button = tk.Button(frame, text="列出檔案", command=list_files)
list_button.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

result_text = tk.Text(app, width=80, height=20)
result_text.pack(pady=10)

app.mainloop()
