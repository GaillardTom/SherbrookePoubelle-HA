# Brand Assets for HACS

This directory contains brand assets for the HACS (Home Assistant Community Store) integration.

## Required Files

| File | Required | Size | Format |
|------|----------|------|--------|
| `icon.png` | **Yes** | 256x256px | PNG |
| `icon@2x.png` | No | 512x512px | PNG |
| `logo.png` | No | Any | PNG |
| `dark_icon.png` | No | 256x256px | PNG (white icon) |
| `dark_logo.png` | No | Any | PNG (white text) |

## Icon Design Guidelines

1. **Format**: PNG (not SVG for custom integrations in HACS)
2. **Size**: 256x256px for icon.png
3. **Style**: Simple, recognizable at small sizes
4. **Background**: Transparent
5. **Colors**: Should work in both light and dark themes

## Creating the Icon

### Option 1: Online Icon Generator

Use a tool like:
- [Icon Kitchen](https://icon.kitchen/)
- [Material Design Icons](https://materialdesignicons.com/)
- [Flaticon](https://www.flaticon.com/)

Search for "trash" or "recycle" icons, download as PNG at 256x256px.

### Option 2: Convert from SVG

If you have an SVG icon, convert it to PNG:

```bash
# Using ImageMagick
convert -background none -resize 256x256 icon.svg icon.png

# Using Inkscape
inkscape icon.svg --export-filename=icon.png --export-width=256 --export-height=256
```

### Option 3: Design Your Own

Create a simple icon that represents:
- Waste collection (trash can)
- Recycling (recycle symbol)
- The City of Sherbrooke (optional - could use colors or a simple map outline)

Suggested colors based on the integration:
- Garbage bin: #2c3e50 (dark blue-gray)
- Recycling symbol: #27ae60 (green)
- Compost symbol: #8B4513 (brown)

## Where These Files Go

### For HACS (Recommended)
Place the files **in this directory** (`brands/` inside your integration folder). HACS will find them automatically.

```
custom_components/sherbrooke_poubelle/
├── brands/
│   ├── icon.png
│   └── logo.png
└── ...
```

### For Home Assistant Core (Optional)
If you want the icon in the official brands repository, submit to:
https://github.com/home-assistant/brands

Create: `custom_integrations/domotique-sherbrooke/icon.png`

## Verification

After adding your icon, run the validation tests:

```bash
python tests/test_validation.py
```

## Resources

- [HACS Publish Documentation](https://hacs.xyz/docs/publish/include#brands)
- [Home Assistant Design Guidelines](https://design.home-assistant.io/)
