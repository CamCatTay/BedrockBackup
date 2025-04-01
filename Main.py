import os
import shutil
import time
import tkinter as tk ## For GUI
from tkinter import filedialog
import json
from tkinter import messagebox

# Constants
CONFIG_FILE = "config.json"
DEFAULT_INTERVAL = 30 ## Default backup interval is 30 minutes
DEFAULT_MAX_BACKUPS = 10 ## Default amount of backups that are in rotation

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"worlds_folder": "", "backup_folder": "", "interval": DEFAULT_INTERVAL, "max_backups": DEFAULT_MAX_BACKUPS}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def backup_world(target_world_folder, backup_folder, max_backups):
        if not os.path.exists(target_world_folder):
            print("World not found!")
            return

        world_name = os.path.basename(target_world_folder)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_folder, f"{world_name}_{timestamp}.zip")

        shutil.make_archive(backup_path[:-4], 'zip', target_world_folder)
        print(f"Backup created: {backup_path}")

        # Rotate backups
        backups = sorted([os.path.join(backup_folder, file) for file in os.listdir(backup_folder) if file.startswith(world_name) and file.endswith(".zip")])
        
        while len(backups) > max_backups:
            os.remove(backups.pop(0))
            print("Old backup deleted.")

def select_folder(initial_path):
    folderPath = filedialog.askdirectory(title="Select a folder", initialdir=initial_path)
    if folderPath:
        return folderPath
    else:
        return None
    
def find_minecraft_worlds_path():
    user_profile = os.path.expanduser("~")  # This returns "C:/Users/<username>"

    worlds_folder = os.path.join(user_profile, "AppData", "Local", "Packages",
                                    "Microsoft.MinecraftUWP_8wekyb3d8bbwe", "LocalState",
                                    "games", "com.mojang", "minecraftWorlds")

    if os.path.exists(worlds_folder):
        print("Minecraft Worlds Folder Found.")
        return worlds_folder
    else:
        print("Minecraft worlds folder not found.")
        return None
    
def initialize_gui(config):

    def select_world_folder():
        folderPath = select_folder(find_minecraft_worlds_path())
        if folderPath:
            config["worlds_folder"] = folderPath
            worlds_label.config(text=folderPath)

    def select_backup_folder():
        folderPath = select_folder()
        if folderPath:
            config["backup_folder"] = folderPath
            backup_label.config(text=folderPath)

    def save_settings():
            try:
                interval = int(interval_entry.get())
                if interval <= 0:
                    raise ValueError("Interval must be greater than 0.")
                config["interval"] = interval
                save_config(config)
                messagebox.showinfo("Settings Saved", "Settings have been saved successfully!")
            except ValueError:
                messagebox.showerror("Invalid Input", "Backup interval must be a positive integer.")

    root = tk.Tk()
    root.title("Bedrock Backup")

    worlds_label = tk.Label(root, text=f"Worlds Folder: {config['worlds_folder']}")
    worlds_label.grid(row = 0, column = 1, padx = 10, pady = 10)

    button = tk.Button(root, text = "Select Minecraft World Folder", command = select_world_folder)
    button.grid(row = 0, column = 0, padx = 10, pady = 10)

    backup_label = tk.Label(root, text=f"Backup Folder: {config['backup_folder']}")
    backup_label.grid(row = 1, column = 1, padx = 10, pady = 10)

    button = tk.Button(root, text = "Select Backup Folder", command = select_backup_folder)
    button.grid(row = 1, column = 0, padx = 10, pady = 10)

    interval_label = tk.Label(root, text="Backup Interval (Minutes)")
    interval_label.grid(row = 2, column = 0, padx = 10, pady = 10)

    interval_entry = tk.Entry(root)
    interval_entry.insert(0, str(config["interval"]))
    interval_entry.grid(row = 2, column = 1, padx = 10, pady = 10)

    button = tk.Button(root, text = "Save Settings", command = save_settings)
    button.grid(row = 3, column = 0, padx = 10, pady = 10)

    root.mainloop()

def initialize():
    config = load_config()
    initialize_gui(config)


initialize()