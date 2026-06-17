#!/usr/bin/env python3
import os
import sys
import argparse
import xml.etree.ElementTree as ET

def check_dependencies():
    """Verify that required python libraries are installed, else prompt/install."""
    try:
        import qrcode
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Required libraries (qrcode, pillow) not found. Installing now...")
        import subprocess
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "qrcode", "pillow"])
            print("Libraries installed successfully!")
        except Exception as e:
            try:
                print("Standard pip install failed. Attempting with --break-system-packages...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "qrcode", "pillow", "--break-system-packages"])
                print("Libraries installed successfully with system overrides!")
            except Exception as ex:
                print(f"Error installing dependencies: {ex}")
                print("Please run manually: pip install qrcode pillow")
                sys.exit(1)

# Check and install deps
check_dependencies()

import qrcode
import qrcode.image.svg
from PIL import Image, ImageDraw, ImageFont

def get_macos_font(size):
    """Find a standard macOS font for Pillow rendering."""
    font_paths = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Verdana.ttf"
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except IOError:
                continue
    # Fallback
    print("Warning: macOS system fonts not found. Using default low-res font.")
    return ImageFont.load_default()

def generate_qr_codes(url, output_dir):
    """Generate the raw QR codes (PNG & SVG) without labels."""
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Generate PNG QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,  # Large box size for high resolution
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_png_path = os.path.join(output_dir, "qr_code.png")
    qr_img.save(qr_png_path)
    print(f"✓ Raw PNG QR generated: {qr_png_path}")
    
    # 2. Generate SVG QR
    factory = qrcode.image.svg.SvgPathImage
    qr_svg = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=4,
    )
    qr_svg.add_data(url)
    qr_svg.make(fit=True)
    
    svg_img = qr_svg.make_image(image_factory=factory)
    qr_svg_path = os.path.join(output_dir, "qr_code.svg")
    with open(qr_svg_path, "wb") as f:
        svg_img.save(f)
    print(f"✓ Raw SVG QR generated: {qr_svg_path}")
    
    return qr_png_path, qr_svg_path

def generate_png_sticker(qr_png_path, output_dir):
    """Create a print-ready PNG sticker with a border and text below the QR."""
    qr_image = Image.open(qr_png_path)
    qr_width, qr_height = qr_image.size
    
    # Set canvas sizes: We want some padding and space for text at the bottom
    padding = 40
    text_area_height = 120
    border_thickness = 4
    
    canvas_width = qr_width + (padding * 2)
    canvas_height = qr_height + (padding * 2) + text_area_height
    
    # Create white canvas
    sticker = Image.new("RGB", (canvas_width, canvas_height), "white")
    draw = ImageDraw.Draw(sticker)
    
    # Paste QR Code
    sticker.paste(qr_image, (padding, padding))
    
    # Draw double rounded borders for a premium printed look
    draw.rectangle(
        [border_thickness, border_thickness, canvas_width - border_thickness, canvas_height - border_thickness],
        outline="black",
        width=border_thickness
    )
    # Inner border
    draw.rectangle(
        [border_thickness * 3, border_thickness * 3, canvas_width - (border_thickness * 3), canvas_height - (border_thickness * 3)],
        outline="black",
        width=int(border_thickness / 2)
    )
    
    # Draw Text
    font = get_macos_font(32)
    text = "Scan to Contact Vehicle Owner"
    
    # Measure text size using draw.textbbox (Pillow 8+) or fallback
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        # Fallback for older Pillow versions
        text_width, text_height = draw.textsize(text, font=font)
        
    text_x = (canvas_width - text_width) // 2
    text_y = qr_height + padding + ((text_area_height - text_height) // 2) + 10
    
    draw.text((text_x, text_y), text, fill="black", font=font)
    
    sticker_png_path = os.path.join(output_dir, "sticker_design.png")
    sticker.save(sticker_png_path, dpi=(300, 300))  # Set high printing DPI
    print(f"✓ Print-ready PNG Sticker generated: {sticker_png_path}")

def generate_svg_sticker(qr_svg_path, url, output_dir):
    """Generate a vector SVG sticker with a border and text below the QR."""
    # We parse the QR code SVG to extract its path elements, and wrap them in our custom layout
    try:
        tree = ET.parse(qr_svg_path)
        root = tree.getroot()
        
        # QR SVG size attributes
        qr_width_str = root.attrib.get('width', '500')
        qr_height_str = root.attrib.get('height', '500')
        
        # Clean numeric values
        qr_w = int(qr_width_str.replace('mm', '').replace('px', '').split('.')[0])
        qr_h = int(qr_height_str.replace('mm', '').replace('px', '').split('.')[0])
        
        # Sticker dimensions
        padding = 40
        text_area_h = 100
        border_w = 4
        
        sticker_w = qr_w + (padding * 2)
        sticker_h = qr_h + (padding * 2) + text_area_h
        
        # Create new SVG root element
        new_root = ET.Element('svg', {
            'xmlns': 'http://www.w3.org/2000/svg',
            'viewBox': f'0 0 {sticker_w} {sticker_h}',
            'width': f'{sticker_w}px',
            'height': f'{sticker_h}px'
        })
        
        # Add white background
        ET.SubElement(new_root, 'rect', {
            'x': '0',
            'y': '0',
            'width': str(sticker_w),
            'height': str(sticker_h),
            'fill': 'white'
        })
        
        # Add outer border rectangle
        ET.SubElement(new_root, 'rect', {
            'x': str(border_w),
            'y': str(border_w),
            'width': str(sticker_w - (border_w * 2)),
            'height': str(sticker_h - (border_w * 2)),
            'fill': 'none',
            'stroke': 'black',
            'stroke-width': str(border_w)
        })
        
        # Add inner border rectangle
        ET.SubElement(new_root, 'rect', {
            'x': str(border_w * 3),
            'y': str(border_w * 3),
            'width': str(sticker_w - (border_w * 6)),
            'height': str(sticker_h - (border_w * 6)),
            'fill': 'none',
            'stroke': 'black',
            'stroke-width': str(border_w / 2)
        })
        
        # Create a container group for the QR paths and translate it by padding
        qr_group = ET.SubElement(new_root, 'g', {
            'transform': f'translate({padding}, {padding})'
        })
        
        # Copy elements from original QR SVG into our group
        for elem in root:
            # Recreate path or elements inside our group
            # We copy tag and attrib
            tag = elem.tag.split('}')[-1] # Remove XML namespace if present
            new_elem = ET.SubElement(qr_group, tag, elem.attrib)
            # copy text/children if any
            if elem.text:
                new_elem.text = elem.text
                
        # Add Text element at the bottom
        text_y = qr_h + padding + (text_area_h // 2) + 10
        text_elem = ET.SubElement(new_root, 'text', {
            'x': str(sticker_w // 2),
            'y': str(text_y),
            'font-family': 'Arial, Helvetica, sans-serif',
            'font-size': '26px',
            'font-weight': 'bold',
            'text-anchor': 'middle',
            'fill': 'black'
        })
        text_elem.text = "Scan to Contact Vehicle Owner"
        
        # Write file
        sticker_svg_path = os.path.join(output_dir, "sticker_design.svg")
        new_tree = ET.ElementTree(new_root)
        new_tree.write(sticker_svg_path, encoding='utf-8', xml_declaration=True)
        print(f"✓ Print-ready SVG Sticker generated: {sticker_svg_path}")
        
    except Exception as e:
        print(f"Error generating SVG sticker: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Vehicle QR codes & print stickers.")
    parser.add_argument(
        "--url", 
        type=str, 
        default="https://satyam-vehicle-qr.vercel.app", 
        help="The URL that the QR code will scan and redirect to."
    )
    parser.add_argument(
        "--output-dir", 
        type=str, 
        default="assets", 
        help="Directory to save generated files."
    )
    args = parser.parse_args()
    
    print(f"Generating QR Codes for URL: {args.url}")
    qr_png, qr_svg = generate_qr_codes(args.url, args.output_dir)
    generate_png_sticker(qr_png, args.output_dir)
    generate_svg_sticker(qr_svg, args.url, args.output_dir)
    print("\n🎉 All QR assets generated successfully in the 'assets' directory!")
