"""Pytest configuration for Sherbrooke Waste Collection tests."""

import pytest
import sys
from pathlib import Path

# Add the integration directory to the path
# integration_path = Path(__file__).parent.parent / "custom_components" / "sherbrooke_poubelle"
# sys.path.insert(0, str(integration_path))
root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))

@pytest.fixture
def mock_hass():
    """Create a mock Home Assistant instance."""
    from unittest.mock import Mock, AsyncMock

    hass = Mock()
    hass.data = {}
    hass.config_entries = Mock()
    hass.config_entries.async_forward_entry_setups = AsyncMock(return_value=True)
    hass.config_entries.async_unload_platforms = AsyncMock(return_value=True)

    return hass


@pytest.fixture
def mock_config_entry():
    """Create a mock config entry."""
    from unittest.mock import Mock

    entry = Mock()
    entry.entry_id = "test_entry_id"
    entry.data = {
        "address_number": "1268",
        "street_name": "CALAIS",
        "selected_address": "1268 RUE CALAIS",
        "calendar_url": "https://www.sherbrooke.ca/sectors/01/days/Lundi/ics",
        "sector": "01",
        "collection_day": "Lundi",
    }
    entry.title = "1268 RUE CALAIS"

    return entry
