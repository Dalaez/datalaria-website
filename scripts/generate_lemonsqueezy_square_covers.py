#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_lemonsqueezy_square_covers.py
======================================
Adapts all 17 executive cover images in packages/00_DISTRIBUCION_LEMONSQUEEZY/Images
into high-resolution square (1200x1200px) cards optimized for Lemon Squeezy.

Features:
- Seamless dark slate background (#0B1120) with fine executive grid pattern.
- Guaranteed safe zones: immune to 4:3 checkout modal cropping (~150px top/bottom)
  and circular store avatar obstruction (~80px at bottom-center).
- High quality Lanczos resampling with crisp, anti-aliased borders.
"""

import os
from PIL import Image, ImageDraw

SRC_DIR = r"c:\Users\dalae\OneDrive\Emprendiendo\datalaria\packages\00_DISTRIBUCION_LEMONSQUEEZY\Images"
DST_DIR = r"c:\Users\dalae\OneDrive\Emprendiendo\datalaria\packages\00_DISTRIBUCION_LEMONSQUEEZY\Images_Square"

CANVAS_W = 1200
CANVAS_H = 1200

# Base dark slate background
BG_COLOR = (11, 17, 32)
GRID_LINE_COLOR = (18, 27, 44)
GRID_CROSS_COLOR = (35, 48, 68)
BORDER_COLOR = (56, 189, 248) # Cyan-blue accent

def create_grid_background(w, h):
    canvas = Image.new("RGB", (w, h), BG_COLOR)
    draw = ImageDraw.Draw(canvas)
    
    # 40px grid lines
    step = 40
    for x in range(0, w, step):
        draw.line([(x, 0), (x, h)], fill=GRID_LINE_COLOR, width=1)
    for y in range(0, h, step):
        draw.line([(0, y), (w, y)], fill=GRID_LINE_COLOR, width=1)
        
    # 120px subtle intersection crosses
    for x in range(60, w, 120):
        for y in range(60, h, 120):
            draw.line([(x - 3, y), (x + 3, y)], fill=GRID_CROSS_COLOR, width=1)
            draw.line([(x, y - 3), (x, y + 3)], fill=GRID_CROSS_COLOR, width=1)
            
    return canvas

def process_image(src_path, dst_path):
    im = Image.open(src_path).convert("RGB")
    orig_w, orig_h = im.size
    
    canvas = create_grid_background(CANVAS_W, CANVAS_H)
    draw = ImageDraw.Draw(canvas)
    
    # Check if this is an isometric illustration (5Porter, SWOT) vs programmatic slide
    is_isometric = ("5Porter" in src_path or "SWOT" in src_path)
    
    if is_isometric:
        # Scale to fill square nicely while staying in safe zone
        scale = min(1120 / orig_w, 1020 / orig_h)
        new_w = int(orig_w * scale)
        new_h = int(orig_h * scale)
        im_resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        paste_x = (CANVAS_W - new_w) // 2
        # Slight upward offset for bottom avatar
        paste_y = (CANVAS_H - new_h) // 2 - 20
        
        canvas.paste(im_resized, (paste_x, paste_y))
    else:
        # Programmatic 1200x630 slide
        # Target width ~1080px (safe margin: 60px on each side)
        # Scaled height: 630 * (1080 / 1200) = 567px
        scale = 1080 / orig_w
        new_w = int(orig_w * scale)
        new_h = int(orig_h * scale)
        im_resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        paste_x = (CANVAS_W - new_w) // 2
        # Center vertically in the 4:3 safe zone (between y=150 and y=1050)
        # Midpoint of safe zone is y=600. Card center at y=575 (slightly up for avatar)
        paste_y = 575 - (new_h // 2)
        
        # Paste slide
        canvas.paste(im_resized, (paste_x, paste_y))
        
        # Executive framed border
        draw.rectangle(
            [(paste_x - 1, paste_y - 1), (paste_x + new_w, paste_y + new_h)],
            outline=BORDER_COLOR,
            width=1
        )
        
    canvas.save(dst_path, "PNG", quality=95)
    print(f"Processed: {os.path.basename(src_path)} -> {os.path.basename(dst_path)}")

def main():
    os.makedirs(DST_DIR, exist_ok=True)
    images = sorted([f for f in os.listdir(SRC_DIR) if f.endswith(".png")])
    print(f"Found {len(images)} images to process...")
    for img_name in images:
        src = os.path.join(SRC_DIR, img_name)
        dst = os.path.join(DST_DIR, img_name)
        process_image(src, dst)
    print("All images processed successfully!")

if __name__ == "__main__":
    main()
