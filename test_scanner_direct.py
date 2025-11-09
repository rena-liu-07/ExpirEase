import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from scanner import analyze_image

# Test with absolute path
image_path = r"C:\Users\ezhan\OneDrive\ExpirEase\ExpirEase-4\pictures\test_apple.jpg"

print(f"Testing scanner with: {image_path}")
print(f"File exists: {os.path.exists(image_path)}")

try:
    items = analyze_image(image_path)
    print(f"\nDetected {len(items)} items:")
    for item in items:
        print(f"  {item}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
