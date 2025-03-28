import os
import shutil
import time
from datetime import datetime
from threading import Thread
import tkinter as tk
from tkinter import messagebox
import psutil

## Constants
backupTime = 1800
failedBackupRetryTime = 5

source_path = r"C:\Users\camer\AppData\Local\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\minecraftWorlds" # World names are gibberish look in file for world name files
backup_path = r"C:\Users\camer\MinecraftBackups"  # Backup location

running = False  
monitoring = True 

def attempt_backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = os.path.join(backup_path, f"Backup_{timestamp}")
    success = False
    while not success and running:
        try:
            shutil.copytree(source_path, destination)
            print(f"Backup completed at {timestamp}")
            success = True
        except PermissionError:
            print("File is locked, retrying...")
            time.sleep(failedBackupRetryTime) 
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
            break
    manage_backups()

def manage_backups():
    backup_folders = sorted(
        [f for f in os.listdir(backup_path) if os.path.isdir(os.path.join(backup_path, f))],
        key=lambda x: os.path.getctime(os.path.join(backup_path, x))
    )
    while len(backup_folders) > 10:
        oldest_backup = backup_folders.pop(0)
        shutil.rmtree(os.path.join(backup_path, oldest_backup))
        print(f"Deleted old backup: {oldest_backup}")

def monitor_minecraft():
    global running
    while monitoring:
        minecraft_running = any(proc.name() == "Minecraft.Windows.exe" for proc in psutil.process_iter())
        if minecraft_running and not running:
            print("Minecraft detected! Starting backups.")
            running = True
            Thread(target=backup_loop).start()
        elif not minecraft_running and running:
            print("Minecraft closed! Stopping backups.")
            running = False
        time.sleep(5) 

def backup_loop():
    while running:
        attempt_backup()
        time.sleep(backupTime)

def start_monitoring():
    global monitoring
    monitoring = True
    Thread(target=monitor_minecraft).start()
    status_label.config(text="Status: Monitoring Minecraft")

def stop_monitoring():
    global monitoring, running
    monitoring = False
    running = False
    status_label.config(text="Status: Stopped")
    print("Monitoring and backups stopped.")

# GUI
root = tk.Tk()
root.title("Minecraft Backup Manager")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

status_label = tk.Label(frame, text="Status: Not Monitoring", font=("Arial", 12))
status_label.pack(pady=5)

start_button = tk.Button(frame, text="Start Monitoring", command=start_monitoring, width=20)
start_button.pack(pady=5)

stop_button = tk.Button(frame, text="Stop Monitoring", command=stop_monitoring, width=20)
stop_button.pack(pady=5)

exit_button = tk.Button(frame, text="Exit", command=root.quit, width=20)
exit_button.pack(pady=5)

# Start the GUI main loop
root.mainloop()
