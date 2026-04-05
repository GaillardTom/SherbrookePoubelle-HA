"""Tests for the Sherbrooke Waste Collection config flow."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "custom_components" / "sherbrooke_poubelle"))


class TestConfigFlow:
    """Test the config flow."""

    def test_extract_sector_from_url(self):
        """Test extraction of sector from calendar URL."""
        from config_flow import SherbrookeWasteConfigFlow

        # Test valid URL
        url = "https://www.sherbrooke.ca/sectors/01/days/Lundi/ics"
        sector = SherbrookeWasteConfigFlow._extract_sector(None, url)
        assert sector == "01"

        # Test another valid URL
        url = "https://www.sherbrooke.ca/sectors/15/days/Mardi/ics"
        sector = SherbrookeWasteConfigFlow._extract_sector(None, url)
        assert sector == "15"

    def test_extract_sector_invalid_url(self):
        """Test extraction with invalid URL returns unknown."""
        from config_flow import SherbrookeWasteConfigFlow

        # Test URL without sectors
        url = "https://www.sherbrooke.ca/some/other/path"
        sector = SherbrookeWasteConfigFlow._extract_sector(None, url)
        assert sector == "unknown"

        # Test empty URL
        sector = SherbrookeWasteConfigFlow._extract_sector(None, "")
        assert sector == "unknown"

    def test_config_flow_version(self):
        """Test that config flow has a version defined."""
        from config_flow import SherbrookeWasteConfigFlow

        assert hasattr(SherbrookeWasteConfigFlow, 'VERSION')
        assert isinstance(SherbrookeWasteConfigFlow.VERSION, int)
        assert SherbrookeWasteConfigFlow.VERSION >= 1


# if __name__ == "__main__":
#     pytest.main([__file__, "-v"])
