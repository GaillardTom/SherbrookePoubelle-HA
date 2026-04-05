#!/bin/bash
# Script to prepare brand assets for Home Assistant Brands submission
# Usage: ./scripts/prepare-brands.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BRANDS_DIR="$PROJECT_DIR/brands"
OUTPUT_DIR="$PROJECT_DIR/dist/brands-submission"

echo "Preparing brand assets for Home Assistant Brands submission..."

# Create output directory
mkdir -p "$OUTPUT_DIR/custom_integrations/domotique-sherbrooke"

# Copy all brand files
cp "$BRANDS_DIR"/*.svg "$OUTPUT_DIR/custom_integrations/domotique-sherbrooke/"

echo "✅ Brand assets prepared in: $OUTPUT_DIR/custom_integrations/domotique-sherbrooke/"
echo ""
echo "Next steps:"
echo "1. Fork https://github.com/home-assistant/brands"
echo "2. Copy the contents of $OUTPUT_DIR/custom_integrations/ to your fork"
echo "3. Submit a Pull Request to home-assistant/brands"
echo ""
echo "Directory structure to submit:"
find "$OUTPUT_DIR" -type f | sed 's|.*dist/||'
