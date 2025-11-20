"""
PWA Icon Generator Script

This script creates placeholder icons for the CuraLink PWA.
For production, replace these with professionally designed icons.

Requirements:
    pip install Pillow

Usage:
    python generate_pwa_icons.py
"""

from PIL import Image, ImageDraw, ImageFont
import os


def create_icon(size, output_path):
    """Create a simple icon with CuraLink branding"""
    # Create image with healthcare blue background
    img = Image.new('RGB', (size, size), color='#0ea5e9')
    draw = ImageDraw.Draw(img)
    
    # Draw a white circle (representing health/care)
    margin = size // 8
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill='white',
        outline='#0ea5e9'
    )
    
    # Draw a cross symbol (medical symbol)
    cross_width = size // 12
    cross_length = size // 3
    center = size // 2
    
    # Vertical bar of cross
    draw.rectangle(
        [center - cross_width//2, center - cross_length//2,
         center + cross_width//2, center + cross_length//2],
        fill='#0ea5e9'
    )
    
    # Horizontal bar of cross
    draw.rectangle(
        [center - cross_length//2, center - cross_width//2,
         center + cross_length//2, center + cross_width//2],
        fill='#0ea5e9'
    )
    
    # Save the icon
    img.save(output_path, 'PNG')
    print(f'Created icon: {output_path} ({size}x{size})')


def main():
    """Generate all required PWA icons"""
    # Create icons directory if it doesn't exist
    icons_dir = 'static/icons'
    os.makedirs(icons_dir, exist_ok=True)
    
    # Icon sizes required for PWA
    sizes = [16, 32, 72, 96, 128, 144, 152, 192, 384, 512]
    
    print('Generating PWA icons for CuraLink...\n')
    
    for size in sizes:
        output_path = os.path.join(icons_dir, f'icon-{size}x{size}.png')
        create_icon(size, output_path)
    
    print('\n✓ All icons generated successfully!')
    print(f'✓ Icons saved in: {icons_dir}/')
    print('\nNext steps:')
    print('1. Review the generated icons')
    print('2. Replace with professionally designed icons for production')
    print('3. Ensure all icon files are committed to version control')


if __name__ == '__main__':
    try:
        main()
    except ImportError:
        print('Error: Pillow library not found.')
        print('Install it with: pip install Pillow')
    except Exception as e:
        print(f'Error generating icons: {e}')
