#!/usr/bin/env python3
"""Adjust the position of the 'As complexity grows...' text in the image."""

from PIL import Image, ImageDraw, ImageFont
import os

img_path = "25_same_problem_ladder.png"
backup_path = "25_same_problem_ladder_backup.png"

# Load image
img = Image.open(img_path)
width, height = img.size
print(f"Image dimensions: {width}x{height}")

# Create backup
img.save(backup_path)
print(f"Backup created: {backup_path}")

# The text we need to move
text = "As complexity grows, the script stays readable — the formula doesn't."

# Load image fresh for drawing
img = Image.open(img_path)
draw = ImageDraw.Draw(img)

# Try to find and use the font that matches the image
# If not available, use default
try:
    # Try common system fonts
    font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 18)
except:
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except:
        font = ImageFont.load_default()

# Text color (grayish, italicized look)
text_color = (128, 128, 128)

# Get bounding box to center horizontally
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]

# Center horizontally
x = (width - text_width) // 2

# Current position appears to be around y=875
# Move down to y=920 to create breathing room from footer
y = 920

# Draw text at new position
draw.text((x, y), text, font=font, fill=text_color)

# Save modified image
img.save(img_path)
print(f"Image updated successfully!")
print(f"Text repositioned to y={y}")
print(f"Saved to: {img_path}")
