from pathlib import Path
import sys
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

if len(sys.argv) != 2:
    raise SystemExit("Usage: python scripts/prep_photo.py source-photo.jpg")
img = Image.open(sys.argv[1]).convert("RGB")
img = ImageOps.fit(img, (1000, 700), method=Image.Resampling.LANCZOS, centering=(0.5, 0.48))
gray = ImageOps.grayscale(img)
gray = ImageEnhance.Contrast(gray).enhance(1.65)
gray = ImageEnhance.Sharpness(gray).enhance(1.25)
gray.filter(ImageFilter.GaussianBlur(0.15)).save("source-prepped.png")
print("Wrote source-prepped.png")
