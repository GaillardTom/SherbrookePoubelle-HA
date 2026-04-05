"""Pytest configuration for Sherbrooke Waste Collection tests."""

import pytest
import sys
from pathlib import Path

# Add the integration directory to the path
integration_path = Path(__file__).parent.parent / "custom_components" / "sherbrooke_poubelle"
sys.path.insert(0, str(integration_path))


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
        "address_number": "1234",
        "street_name": "TEST",
        "selected_address": "1234 Test Street",
        "calendar_url": "https://www.sherbrooke.ca/sectors/01/days/Lundi/ics",
        "sector": "01",
        "collection_day": "Lundi",
    }
    entry.title = "1234 Test Street"

    return entry
