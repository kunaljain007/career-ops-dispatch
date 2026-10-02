import os
import sys
import win32com.client

sys.stdout.reconfigure(encoding='utf-8')

pptx_path = os.path.abspath(r"C:\Users\My\Desktop\HEATBOLT_Defence_Strategic_Briefing.pptx")
pdf_path = os.path.abspath(r"C:\Users\My\Desktop\jaishreeram.pdf")

print(f"Converting PPTX to PDF...")
print(f"Source: {pptx_path}")
print(f"Target: {pdf_path}")

powerpoint = win32com.client.Dispatch("PowerPoint.Application")
# Keep window minimized/hidden if possible
try:
    deck = powerpoint.Presentations.Open(pptx_path, WithWindow=False)
    # ppSaveAsPDF = 32
    deck.SaveAs(pdf_path, 32)
    deck.Close()
    print("SUCCESS: PDF exported successfully using native PowerPoint engine!")
except Exception as e:
    print("Error during export:", e)
finally:
    powerpoint.Quit()

if os.path.exists(pdf_path):
    size_bytes = os.path.getsize(pdf_path)
    print(f"Verified PDF exists! Size: {size_bytes:,} bytes ({size_bytes / (1024*1024):.2f} MB)")
else:
    print("ERROR: Target PDF not found on disk!")
