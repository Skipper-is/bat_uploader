import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import StringVar
import shutil
import os

class FileMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Mover")
        
        self.source_folder = ""
        self.source_folderSV = StringVar()
        self.destination_folderSV = StringVar()
        self.destination_folder = ""

        self.source_file_box = None
        self.dest_file_box = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # Source folder label and button
        source_label = tk.Label(self.root, text="Source Folder:")
        source_label.grid(row=0, column=0, padx=10, pady=10)

        self.source_file_box = tk.Entry(self.root, width=50, textvariable=self.source_folderSV, validate="all", validatecommand=self.callback)
        self.source_file_box.grid(row=0, column=1, padx=10, pady=10)

        source_button = tk.Button(self.root, text="Browse", command=self.select_source_folder)
        source_button.grid(row=0, column=2, padx=10, pady=10)
        
        # Destination folder label and button
        dest_label = tk.Label(self.root, text="Destination Folder:")
        dest_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.dest_file_box = tk.Entry(self.root, width=50, textvariable=self.destination_folderSV, validate="all", validatecommand=self.callback)
        self.dest_file_box.grid(row=1, column=1, padx=10, pady=10)

        dest_button = tk.Button(self.root, text="Browse", command=self.select_destination_folder)
        dest_button.grid(row=1, column=2, padx=10, pady=10)
        
        # Move button
        move_button = tk.Button(self.root, text="Move", command=self.move_files)
        move_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, length=200)
        progress_bar.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        
    def select_source_folder(self):
        self.source_folder = filedialog.askdirectory()
        self.source_folderSV.set(self.source_folder)
        self.callback()

        
    def select_destination_folder(self):
        self.destination_folder = filedialog.askdirectory()
        self.destination_folderSV.set(self.destination_folder)
        self.callback()
    
    def callback(self):
        self.source_folder = self.source_file_box.get()
        self.destination_folder = self.dest_file_box.get()
        print(self.source_folder)
        print(self.destination_folder)

    def move_files(self):
        self.callback()
        if not self.source_folder or not self.destination_folder:
            messagebox.showerror("Error", "Please select both source and destination folders!")
            return
        
        self.total_files = 0
        self.moved_files = 0

        self.move_files_recursive(self.source_folder, "")
        
        messagebox.showinfo("Success", "Files moved successfully!")

    def move_files_recursive(self, folder, relative_path):
        files = os.listdir(folder)

        for file in files:
            src = os.path.join(folder, file)
            dest = os.path.join(self.destination_folder, relative_path, file)

            if os.path.isfile(src):
                shutil.move(src, dest)
                self.moved_files += 1
            elif os.path.isdir(src):
                new_relative_path = os.path.join(relative_path, file)
                os.makedirs(os.path.join(self.destination_folder, new_relative_path), exist_ok=True)
                self.move_files_recursive(src, new_relative_path)
        self.total_files += len(files)
        try:
            progress = (self.moved_files / self.total_files) * 100
        except ZeroDivisionError:
            progress = 0
        self.progress_var.set(progress)
        self.root.update()

# Create the Tkinter root window
root = tk.Tk()

# Create an instance of the FileMoverApp
app = FileMoverApp(root)

# Start the Tkinter event loop
root.mainloop()
