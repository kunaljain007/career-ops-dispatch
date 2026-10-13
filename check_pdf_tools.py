import os
import subprocess
import shutil

print("Checking PDF export options...")

# Check comtypes or win32com
try:
    import win32com.client
    print("win32com is installed!")
    try:
        ppt = win32com.client.Dispatch("PowerPoint.Application")
        print("PowerPoint COM: SUCCESS!")
        ppt.Quit()
        ppt_com = True
    except Exception as e:
        print("PowerPoint COM failed:", e)
        ppt_com = False
except Exception as e:
    print("win32com not available:", e)
    ppt_com = False

# Check Edge
edge_paths = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
]
edge = None
for p in edge_paths:
    if os.path.exists(p):
        edge = p
        break
print("Edge executable:", edge)

# Check Chrome
chrome_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
]
chrome = None
for p in chrome_paths:
    if os.path.exists(p):
        chrome = p
        break
print("Chrome executable:", chrome)
