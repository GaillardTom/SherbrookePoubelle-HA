#!/usr/bin/env python3
"""
Script to create a simple brand icon for HACS.

This creates a basic icon.png using PIL/Pillow.
If you want a more professional icon, use a design tool or icon generator.

Usage:
    python scripts/create-icon.py

Requirements:
    pip install pillow
"""

import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Error: Pillow is not installed.")
    print("Install it with: pip install pillow")
    sys.exit(1)


def create_trash_icon(size=256):
    """Create a simple trash/recycle icon."""
    # Create transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    trash_color = (44, 62, 80, 255)  # #2c3e50 - dark blue-gray
    recycle_color = (39, 174, 96, 255)  # #27ae60 - green

    # Scale factor
    s = size / 24  # Base on 24x24 viewbox

    # Draw trash can body (simplified)
    # Main body rectangle
    body_x1 = int(6 * s)
    body_y1 = int(7 * s)
    body_x2 = int(18 * s)
    body_y2 = int(20 * s)
    draw.rounded_rectangle(
        [body_x1, body_y1, body_x2, body_y2],
        radius=int(1 * s),
        fill=trash_color
    )

    # Draw lid
    lid_x1 = int(5 * s)
    lid_y1 = int(4 * s)
    lid_x2 = int(19 * s)
    lid_y2 = int(6 * s)
    draw.rounded_rectangle(
        [lid_x1, lid_y1, lid_x2, lid_y2],
        radius=int(0.5 * s),
        fill=trash_color
    )

    # Draw handle on lid
    handle_x1 = int(10 * s)
    handle_y1 = int(2 * s)
    handle_x2 = int(14 * s)
    handle_y2 = int(4 * s)
    draw.rounded_rectangle(
        [handle_x1, handle_y1, handle_x2, handle_y2],
        radius=int(0.5 * s),
        fill=trash_color
    )

    # Add recycling symbol (simplified as three dots)
    dot_positions = [
        (12, 10),  # Top
        (9, 14),   # Bottom left
        (15, 14),  # Bottom right
    ]

    for x, y in dot_positions:
        dot_x = int(x * s)
        dot_y = int(y * s)
        radius = int(1.5 * s)
        draw.ellipse(
            [dot_x - radius, dot_y - radius, dot_x + radius, dot_y + radius],
            fill=recycle_color
        )

    return img


def main():
    """Create the icon and save it."""
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent

    # Target locations (check both possible locations)
    possible_targets = [
        project_dir / "custom_components" / "sherbrooke_poubelle" / "brands",
        project_dir / "brands",
    ]

    target_dir = None
    for target in possible_targets:
        target.mkdir(parents=True, exist_ok=True)
        target_dir = target
        break

    if not target_dir:
        print("Error: Could not determine target directory")
        sys.exit(1)

    # Create icon
    print(f"Creating brand icon...")
    icon = create_trash_icon(256)

    # Save icon.png
    icon_path = target_dir / "icon.png"
    icon.save(icon_path, "PNG")
    print(f"✅ Created: {icon_path}")

    # Also create @2x version
    icon_2x = create_trash_icon(512)
    icon_2x_path = target_dir / "icon@2x.png"
    icon_2x.save(icon_2x_path, "PNG")
    print(f"✅ Created: {icon_2x_path}")

    print(f"\n🎉 Brand icons created successfully!")
    print(f"\nNext steps:")
    print(f"  1. If you want a more professional icon, replace these files")
    print(f"  2. Consider creating dark_icon.png (white version)")
    print(f"  3. Consider creating logo.png (wider format with text)")
    print(f"\nIcon location: {target_dir}")


if __name__ == "__main__":
    main()
