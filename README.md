# Sherbrooke Waste Collection - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

A custom Home Assistant integration for the City of Sherbrooke's waste collection calendar. Automatically shows which bin to put out based on your address.

## Bin Colors

| Type | Color | Icon |
|----------|-------|------|
| **Garbage** | Black | `mdi:trash-can` |
| **Recycling** | Green | `mdi:recycle` |
| **Compost** | Brown | `mdi:leaf` |

## Features

- 🔍 **Address-based setup**: Enter your address and select from matching results
- **ICS Calendar sync**: Automatically fetches your collection schedule
- **Color-coded bins**: Green=Recycling, Brown=Compost, Black=Garbage
- **Countdown sensor**: Shows days until next collection
- **Automatic notifications**: Get reminded the day before collection
- **Dashboard cards**: Beautiful pre-made card examples
- **Bilingual**: English and French support

## Installation

### HACS (Recommended)

1. Add this repository to HACS as a custom repository
2. Install "Sherbrooke Waste Collection"
3. Restart Home Assistant
4. Go to Settings > Devices & Services > Add Integration

### Manual Installation

1. Copy `custom_components/sherbrooke_poubelle` to your Home Assistant `config/custom_components` directory
2. Restart Home Assistant
3. Add the integration via Settings > Devices & Services > Add Integration

## Setup

1. Search for "Sherbrooke Waste" or "Poubelle Sherbrooke" in the integrations list
2. Enter your **address number** (e.g., `1165`)
3. Enter your **street name** (e.g., `L` or `Larocque`)
4. Select your exact address from the results
5. Done! The sensors will be created automatically

## Sensors

Two sensors are created:

### Next Collection
- **State**: Shows the waste type (`Garbage`, `Recycling`, or `Compost`)
- **Icon**: Changes based on waste type 
- **Attributes**:
  - `collection_date`: ISO date of next pickup
  - `waste_type`: Type of waste being collected
  - `days_until`: Days until collection
  - `raw_summary`: Original calendar event text

### Collection Countdown
- **State**: Number of days until next collection
- **Unit**: `days`
- **Icon**: Changes based on how close the collection is

## Notifications

Automatic notifications are sent at **7:00 PM the day before** collection. You can use this in automations:

```yaml
automation:
  - alias: "Waste Collection Reminder"
    trigger:
      - platform: state
        entity_id: sensor.sherbrooke_poubelle_next_collection
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "Waste Collection Reminder"
          message: "Put out the {{ states('sensor.sherbrooke_poubelle_next_collection') }} bin!"
```

## Dashboard Cards

See [dashboard-examples.md](dashboard-examples.md) for beautiful pre-made cards like:

### Simple Color-Coded Card
```yaml
type: entity
entity: sensor.sherbrooke_poubelle_next_collection
name: Next Collection
card_mod:
  style: |
    ha-card {
      {% if states('sensor.sherbrooke_poubelle_next_collection') == 'Recycling' %}
        background-color: #27ae60;
      {% elif states('sensor.sherbrooke_poubelle_next_collection') == 'Compost' %}
        background-color: #8B4513;
      {% else %}
        background-color: #2c3e50;
      {% endif %}
      color: white;
    }
```

## Testing

### Running Tests Locally

```bash
# Run standalone validation
python tests/test_validation.py

# Run with pytest
pip install -r requirements_test.txt
pytest tests/
```

### Validation Checks

The test suite validates:
- All required files exist
- Python syntax is valid
- JSON files are valid
- Manifest structure is correct
- Domain is consistent across files
- No debug print statements remain
- Logger is defined before use
- Coordinator loop structure is correct
- HACS metadata exists
- LICENSE file exists

### Continuous Integration

This repository includes GitHub Actions workflows that automatically run on every push to `main`:

| Workflow | Purpose | Status |
|----------|---------|--------|
| `validate.yml` | Runs validation tests, pytest, and linting | ![Validate](https://github.com/gaillardTom/sherbrooke-poubelle-ha/workflows/Validate%20Integration/badge.svg) |
| `release.yml` | Builds release packages on new releases | - |
| HACS | Validates HACS integration compatibility | - |
| Hassfest | Validates Home Assistant integration standards | - |

To view the workflow status, check the Actions tab in the GitHub repository.

## Troubleshooting

### No addresses found
- Enter your address in uppercase
- Make sure you enter just the street name without "Rue", "Boulevard", etc.
- Example: Use `LAROCQUE` instead of `Rue Larocque`
- If your address uses an accent do not use it.
- Example: Use `LUNIVERSITE` instead of `L'université`

### Calendar not updating
- The calendar is updated every 24 hours by default
- Check Home Assistant logs for API errors

## Files Included

```
custom_components/sherbrooke_poubelle/
├── __init__.py              # Entry point
├── config_flow.py           # Setup UI
├── const.py                 # Constants & colors
├── coordinator.py           # ICS calendar fetching
├── manifest.json            # Integration metadata
├── notify.py                # Notification service
├── sensor.py                # Sensors
├── services.yaml            # Service definitions
└── translations/
    ├── en.json              # English
    └── fr.json              # French

.github/workflows/            # CI/CD workflows
├── validate.yml             # Validation on push
├── brands.yml               # Brand validation
└── release.yml              # Release automation

brands/                       # Brand assets for HACS
├── icon.png                 # Main integration icon (256x256)
├── icon@2x.png              # High-res icon (512x512)
├── logo.png                 # Logo with text (optional)
├── dark_icon.png            # Dark mode icon (optional)
├── dark_logo.png            # Dark mode logo (optional)
└── README.md                # Brand creation guide

scripts/                      # Helper scripts
├── create-icon.py           # Create a basic icon with Python
├── prepare-brands.sh        # Prepare brands for submission (Unix)
└── prepare-brands.ps1       # Prepare brands for submission (Windows)

tests/                        # Test suite
├── test_validation.py       # Structure validation
├── test_coordinator.py      # Coordinator tests
└── test_config_flow.py      # Config flow tests

dashboard-examples.md         # Dashboard card examples
hacs.json                     # HACS metadata
LICENSE                       # Personal Use License
```

## Data Source

This integration uses the official waste collection data from the [City of Sherbrooke](https://www.sherbrooke.ca/collecte-des-matieres-residuelles).

## Supported Languages

- 🇬🇧 English
- 🇫🇷 French

## License

This project is licensed under a **Personal Use License**. See [LICENSE](LICENSE) for details.

- **Personal use**: ✅ Allowed
- **Commercial use**: ❌ Prohibited without explicit permission
- **Redistribution**: ✅ Allowed with attribution and same license
- **Modification**: ✅ Allowed for personal use

## Brand / Icon

This integration includes brand assets for HACS display.

### For HACS (Required)

HACS requires a `brands/` directory with at least an `icon.png` file.

**Option 1: Include in your repository (Easiest)**
```
custom_components/sherbrooke_poubelle/brands/
├── icon.png          # Required: 256x256px PNG
├── icon@2x.png       # Optional: 512x512px PNG
├── dark_icon.png     # Optional: white version for dark mode
└── logo.png          # Optional: wider format with text
```

HACS will automatically find and display this icon.

**Option 2: Submit to Home Assistant Brands repository**
Fork https://github.com/home-assistant/brands and create `custom_integrations/domotique-sherbrooke/icon.png`

### Creating the Icon

Use the provided script to create a basic icon:

```bash
pip install pillow
python scripts/create-icon.py
```

Or design your own using:
- [Icon Kitchen](https://icon.kitchen/) (Recommended - free, simple)
- [Material Design Icons](https://materialdesignicons.com/)
- Any image editor (Photoshop, GIMP, Figma, etc.)

**Requirements:**
- Format: PNG (not SVG for custom integrations)
- Size: 256x256 pixels
- Background: Transparent
- Style: Simple, recognizable at small sizes

### Icon Design

Suggested design elements:
- **Trash can** or **bin** (represents waste collection)
- **Recycling symbol** (green color #27ae60)
- Colors matching the integration:
  - Garbage: Dark gray #2c3e50
  - Recycling: Green #27ae60
  - Compost: Brown #8B4513

See [brands/README.md](brands/README.md) for detailed guidelines.

## Disclaimer

This is an unofficial integration and is not affiliated with the City of Sherbrooke.
