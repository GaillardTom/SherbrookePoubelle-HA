"""Tests for the Sherbrooke Waste Collection coordinator."""

import pytest
from datetime import datetime, date
from unittest.mock import Mock, patch, AsyncMock
import icalendar

# Import the module under test
import sys
from pathlib import Path
# sys.path.insert(0, str(Path(__file__).parent.parent / "custom_components" / "sherbrooke_poubelle"))

from const import WASTE_TYPE_GARBAGE, WASTE_TYPE_RECYCLING, WASTE_TYPE_COMPOST
from custom_components.sherbrooke_poubelle.coordinator import SherbrookeWasteCoordinator

class TestWasteTypeDetection:
    """Test waste type detection from calendar summaries."""

    def test_detect_garbage(self):
        """Test detection of garbage waste type."""
        from coordinator import SherbrookeWasteCoordinator

        coordinator = Mock(spec=SherbrookeWasteCoordinator)
        # Create a mock instance with the method
        coordinator._detect_waste_type = SherbrookeWasteCoordinator._detect_waste_type

        # Test French terms
        assert WASTE_TYPE_GARBAGE in coordinator._detect_waste_type(coordinator, "Collecte des ordures")
        assert WASTE_TYPE_GARBAGE in coordinator._detect_waste_type(coordinator, "waste collection")

    def test_detect_recycling(self):
        """Test detection of recycling waste type."""
        from coordinator import SherbrookeWasteCoordinator

        coordinator = Mock(spec=SherbrookeWasteCoordinator)
        coordinator._detect_waste_type = SherbrookeWasteCoordinator._detect_waste_type

        # Test French and English terms
        assert WASTE_TYPE_RECYCLING in coordinator._detect_waste_type(coordinator, "Collecte du recyclage")
        assert WASTE_TYPE_RECYCLING in coordinator._detect_waste_type(coordinator, "recycling day")
        assert WASTE_TYPE_RECYCLING in coordinator._detect_waste_type(coordinator, "matières recyclables")

    def test_detect_compost(self):
        """Test detection of compost waste type."""
        from coordinator import SherbrookeWasteCoordinator

        coordinator = Mock(spec=SherbrookeWasteCoordinator)
        coordinator._detect_waste_type = SherbrookeWasteCoordinator._detect_waste_type

        # Test French and English terms
        assert WASTE_TYPE_COMPOST in coordinator._detect_waste_type(coordinator, "résidus alimentaires")
        assert WASTE_TYPE_COMPOST in coordinator._detect_waste_type(coordinator, "compost collection")
        assert WASTE_TYPE_COMPOST in coordinator._detect_waste_type(coordinator, "organique")

    def test_detect_multiple_types(self):
        """Test detection when multiple waste types are mentioned."""
        from coordinator import SherbrookeWasteCoordinator

        coordinator = Mock(spec=SherbrookeWasteCoordinator)
        coordinator._detect_waste_type = SherbrookeWasteCoordinator._detect_waste_type

        # Test combined collection
        result = coordinator._detect_waste_type(coordinator, "Collecte des ordures et recyclage")
        assert WASTE_TYPE_GARBAGE in result
        assert WASTE_TYPE_RECYCLING in result

    def test_default_to_garbage(self):
        """Test that unknown waste types default to garbage."""
        from coordinator import SherbrookeWasteCoordinator

        coordinator = Mock(spec=SherbrookeWasteCoordinator)
        coordinator._detect_waste_type = SherbrookeWasteCoordinator._detect_waste_type

        result = coordinator._detect_waste_type(coordinator, "Some random text")
        # Should return a list with garbage as default
        assert WASTE_TYPE_GARBAGE in result


class TestConstants:
    """Test that constants are properly defined."""

    def test_waste_type_mapping(self):
        """Test that waste type mapping includes expected terms."""
        from const import WASTE_TYPE_MAPPING

        # French terms
        assert "ordures" in WASTE_TYPE_MAPPING
        assert "résidus alimentaires" in WASTE_TYPE_MAPPING
        assert "recyclage" in WASTE_TYPE_MAPPING

        # English terms
        assert "waste" in WASTE_TYPE_MAPPING
        assert "recycling" in WASTE_TYPE_MAPPING
        assert "compost" in WASTE_TYPE_MAPPING

    def test_icons_defined(self):
        """Test that icons are defined for all waste types."""
        from const import ICONS, WASTE_TYPE_GARBAGE, WASTE_TYPE_RECYCLING, WASTE_TYPE_COMPOST

        assert WASTE_TYPE_GARBAGE in ICONS
        assert WASTE_TYPE_RECYCLING in ICONS
        assert WASTE_TYPE_COMPOST in ICONS

        # Check they start with mdi:
        for icon in ICONS.values():
            assert icon.startswith("mdi:")

    def test_colors_defined(self):
        """Test that colors are defined for all waste types."""
        from const import COLORS, WASTE_TYPE_GARBAGE, WASTE_TYPE_RECYCLING, WASTE_TYPE_COMPOST

        assert WASTE_TYPE_GARBAGE in COLORS
        assert WASTE_TYPE_RECYCLING in COLORS
        assert WASTE_TYPE_COMPOST in COLORS

        # Check they are valid hex colors
        for color in COLORS.values():
            assert color.startswith("#")
            assert len(color) == 7  # #RRGGBB

    def test_names_defined(self):
        """Test that display names are defined for all waste types."""
        from const import WASTE_TYPE_NAMES, WASTE_TYPE_GARBAGE, WASTE_TYPE_RECYCLING, WASTE_TYPE_COMPOST

        assert WASTE_TYPE_GARBAGE in WASTE_TYPE_NAMES
        assert WASTE_TYPE_RECYCLING in WASTE_TYPE_NAMES
        assert WASTE_TYPE_COMPOST in WASTE_TYPE_NAMES


class TestConfigFlowConstants:
    """Test that config flow constants are defined."""

    def test_config_keys_exist(self):
        """Test that all config keys are defined."""
        from const import (
            CONF_ADDRESS_NUMBER,
            CONF_STREET_NAME,
            CONF_SELECTED_ADDRESS,
            CONF_CALENDAR_URL,
            CONF_SECTOR,
            CONF_COLLECTION_DAY,
        )

        assert isinstance(CONF_ADDRESS_NUMBER, str)
        assert isinstance(CONF_STREET_NAME, str)
        assert isinstance(CONF_SELECTED_ADDRESS, str)

    def test_api_url_defined(self):
        """Test that API URL is defined."""
        from const import API_SEARCH_URL

        assert API_SEARCH_URL.startswith("https://")
        assert "sherbrooke.ca" in API_SEARCH_URL


# if __name__ == "__main__":
#     pytest.main([__file__, "-v"])
