import os
import tkinter as tk ## For GUI
from tkinter import filedialog
import json

# Constants
CONFIG_FILE = "config.json"
DEFAULT_INTERVAL = 30 ## Default save interval is 30 minutes

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"worlds_folder": "", "backup_folder": "", "interval": 30}


def select_folder():
    folderPath = filedialog.askdirectory("Select a folder")
    if folderPath:
        return folderPath
    else:
        return None
    
def select_world_folder(world_label):
    folderPath = select_folder()
    if folderPath:
        CONFIG_FILE["worlds_folder"] = folderPath
        world_label.config(text=folderPath)

def select_backup_folder(backup_label):
    folderPath = select_folder()
    if folderPath:
        CONFIG_FILE["backup_folder"] = folderPath
        backup_label.config(text=folderPath)

def LoadDirectory(dirName):
    try:
        with open(CONFIG_FILE, "r") as file:
            for line in file:
                data = json.loads(line.strip())
                print(data)
            return None
    except FileNotFoundError:
        return None    
    
def SetupGUI(config):
    root = tk.Tk()
    root.title("Bedrock Backup")

    button = tk.Button(root, text = "Select Minecraft World Folder", command = select_world_folder(worlds_label))
    button.grid(row = 0, column = 0, padx = 10, pady = 10)

    worlds_label = tk.Label(root, text=f"Worlds Folder: {config['worlds_folder']}")
    worlds_label.grid(row = 0, column = 1, padx = 10, pady = 10)

    button = tk.Button(root, text = "Select Backup Folder", command = select_backup_folder(backup_label))
    button.grid(row = 1, column = 0, padx = 10, pady = 10)

    backup_label = tk.Label(root, text=f"Backup Folder: {config['backup_folder']}")
    backup_label.grid(row = 1, column = 1, padx = 10, pady = 10)

    root.mainloop()

def Initialize():

    SetupGUI()


Initialize()