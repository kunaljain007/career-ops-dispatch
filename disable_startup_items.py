import os
import winreg
import json
import shutil

print("Backing up and disabling unnecessary startup programs...")

backup_dir = r"C:\Users\My\.gemini\antigravity\scratch\startup_backup"
os.makedirs(backup_dir, exist_ok=True)

# 1. Backup and remove HKCU Run entries
hkcu_run_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, hkcu_run_path, 0, winreg.KEY_ALL_ACCESS)

entries_to_remove = [
    "IDMan",
    "MicrosoftEdgeAutoLaunch_A2213BB742C1743A198C39EFC005C625",
    "CCleaner Smart Cleaning",
    "GoogleChromeAutoLaunch_D774BE52BAAAACD3F0D1E03770A7B344"
]

backup_data = {}
for entry in entries_to_remove:
    try:
        val_data, val_type = winreg.QueryValueEx(key, entry)
        backup_data[entry] = {"data": val_data, "type": val_type}
        winreg.DeleteValue(key, entry)
        print(f"Disabled HKCU Run entry: {entry}")
    except FileNotFoundError:
        print(f"Entry not found or already disabled: {entry}")
    except Exception as e:
        print(f"Error disabling {entry}: {e}")

winreg.CloseKey(key)

# Save backup to file
with open(os.path.join(backup_dir, "hkcu_run_backup.json"), "w", encoding="utf-8") as f:
    json.dump(backup_data, f, indent=2)
print("Saved registry backup to hkcu_run_backup.json")

# 2. Check AnyDesk.lnk in All Users Startup
all_startup = os.path.expandvars(r'%ALLUSERSPROFILE%\Microsoft\Windows\Start Menu\Programs\Startup')
anydesk_lnk = os.path.join(all_startup, "AnyDesk.lnk")
if os.path.exists(anydesk_lnk):
    try:
        shutil.move(anydesk_lnk, os.path.join(backup_dir, "AnyDesk.lnk"))
        print(f"Moved AnyDesk.lnk from startup to backup: {backup_dir}")
    except Exception as e:
        print(f"Error moving AnyDesk.lnk (may need admin): {e}")
else:
    print("AnyDesk.lnk not found in All Users Startup folder.")

print("Startup optimization complete!")
