import time
import os
import subprocess

def monitor():
    print("Dashboard Auto-Sync Active. Updating every 60 seconds...")
    while True:
        try:
            # Run the stats extractor
            subprocess.run(["python", "dashboard/extract_stats.py"], check=True)
            print(f"[{time.strftime('%H:%M:%S')}] Dashboard synced with latest swarm metrics.")
        except Exception as e:
            print(f"Sync Error: {e}")
        
        time.sleep(60)

if __name__ == "__main__":
    monitor()
