"""Tests for the Sherbrooke Waste Collection coordinator."""

import pytest
from datetime import datetime, date
from unittest.mock import Mock, patch, AsyncMock
import icalendar

# Import the module under test
import sys
from pathlib import Path
# sys.path.insert(0, str(Path(__file__).parent.parent / "custom_components" / "sherbrooke_poubelle"))

from custom_components.sherbrooke_poubelle.const import WASTE_TYPE_GARBAGE, WASTE_TYPE_RECYCLING, WASTE_TYPE_COMPOST
from custom_components.sherbrooke_poubelle.coordinator import SherbrookeWasteCoordinator

class TestWasteTypeDetection:
    """Test waste type detection from calendar summaries."""

    def test_detect_garbage(self):
        """Test detection of garbage waste type."""
        from custom_components.sherbrooke_poubelle.coordinator import SherbrookeWasteCoordinator

        coordinator = Mock(spec=SherbrookeWasteCoordinator)
        # Create a mock instance with the method
        coordinator._detect_waste_type = SherbrookeWasteCoordinator._detect_waste_type

        # Test French terms
        assert WASTE_TYPE_GARBAGE in coordinator._detect_waste_type(coordinator, "Collecte des ordures")
        assert WASTE_TYPE_GARBAGE in coordinator._detect_waste_type(coordinator, "waste collection")

    def test_detect_recycling(self):
        """Test detection of recycling waste type."""
        from custom_components.sherbrooke_poubelle.coordinator import SherbrookeWasteCoordinator

        coordinator = Mock(spec=SherbrookeWasteCoordinator)
        coordinator._detect_waste_type = SherbrookeWasteCoordinator._detect_waste_type

        # Test French and English terms
        assert WASTE_TYPE_RECYCLING in coordinator._detect_waste_type(coordinator, "Collecte du recyclage")
        assert WASTE_TYPE_RECYCLING in coordinator._detect_waste_type(coordinator, "recycling day")
        assert WASTE_TYPE_RECYCLING in coordinator._detect_waste_type(coordinator, "matières recyclables")

    def test_detect_compost(self):
        """Test detection of compost waste type."""
        from custom_components.sherbrooke_poubelle.coordinator import SherbrookeWasteCoordinator

        coordinator = Mock(spec=SherbrookeWasteCoordinator)
        coordinator._detect_waste_type = SherbrookeWasteCoordinator._detect_waste_type

        # Test French and English terms
        assert WASTE_TYPE_COMPOST in coordinator._detect_waste_type(coordinator, "résidus alimentaires")
        assert WASTE_TYPE_COMPOST in coordinator._detect_waste_type(coordinator, "compost collection")
        assert WASTE_TYPE_COMPOST in coordinator._detect_waste_type(coordinator, "organique")

    def test_detect_multiple_types(self):
        """Test detection when multiple waste types are mentioned."""
        from custom_components.sherbrooke_poubelle.coordinator import SherbrookeWasteCoordinator

        coordinator = Mock(spec=SherbrookeWasteCoordinator)
        coordinator._detect_waste_type = SherbrookeWasteCoordinator._detect_waste_type

        # Test combined collection
        result = coordinator._detect_waste_type(coordinator, "Collecte des ordures et recyclage")
        assert WASTE_TYPE_GARBAGE in result
        assert WASTE_TYPE_RECYCLING in result

    def test_default_to_garbage(self):
        """Test that unknown waste types default to garbage."""
        from custom_components.sherbrooke_poubelle.coordinator import SherbrookeWasteCoordinator

        coordinator = Mock(spec=SherbrookeWasteCoordinator)
        coordinator._detect_waste_type = SherbrookeWasteCoordinator._detect_waste_type

        result = coordinator._detect_waste_type(coordinator, "Some random text")
        # Should return a list with garbage as default
        assert WASTE_TYPE_GARBAGE in result

class TestDateParsing:
    """Test date parsing and handling in the coordinator."""

    @pytest.fixture
    def sample_ics_data(self):
        """Return the existing sample ICS data from the test file."""
        return """BEGIN:VCALENDAR
PRODID:-//github.com/ical-org/ical.net//NONSGML ical.net 5.2.0//EN
VERSION:2.0
BEGIN:VEVENT
DTEND:20260413T071500
DTSTAMP:20260407T043926Z
DTSTART:20260413T070000
SEQUENCE:0
SUMMARY:Compost
UID:d5183f79-ef7e-4f86-9e86-550fa2d9967a
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:Compost
TRIGGER:-PT15M
END:VALARM
END:VEVENT
BEGIN:VEVENT
DTEND:20260413T071500
DTSTAMP:20260407T043926Z
DTSTART:20260413T070000
SEQUENCE:0
SUMMARY:Waste
UID:801069f9-c351-4992-96b4-cdaa6da2cf6c
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:Waste
TRIGGER:-PT15M
END:VALARM
END:VEVENT
END:VCALENDAR"""

    @pytest.fixture
    def mock_coordinator(self, mock_hass):
        """Create a coordinator for testing."""
        from custom_components.sherbrooke_poubelle.coordinator import SherbrookeWasteCoordinator
        return SherbrookeWasteCoordinator(mock_hass, "http://test.url/calendar.ics")

    @pytest.mark.asyncio
    async def test_parses_datetime_values_from_ics(self, mock_hass, sample_ics_data, mock_coordinator):
        """Test parsing ICS events with DATETIME values (DTSTART:20260413T070000)."""
        mock_response = AsyncMock()
        mock_response.text.return_value = sample_ics_data
        mock_response.raise_for_status = Mock()

        mock_session = Mock()
        mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.get.return_value.__aexit__ = AsyncMock(return_value=False)

        with patch("aiohttp.ClientSession") as mock_session_class, \
             patch("homeassistant.util.dt.now") as mock_now:

            mock_session_class.return_value.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session_class.return_value.__aexit__ = AsyncMock(return_value=False)

            # Simulate current date is April 7, 2026
            mock_now.return_value = datetime(2026, 4, 7, 12, 0, 0)

            data = await mock_coordinator._async_update_data()

        assert data is not None
        assert "collections" in data
        collections = data["collections"]
        assert len(collections) == 1  # Both events on same date, grouped

        # Check the date is correctly extracted (April 13, 2026)
        assert collections[0]["date"] == date(2026, 4, 13)

    @pytest.mark.asyncio
    async def test_groups_multiple_types_on_same_date(self, mock_hass, sample_ics_data, mock_coordinator):
        """Test that multiple waste types on the same date are grouped together."""
        mock_response = AsyncMock()
        mock_response.text.return_value = sample_ics_data
        mock_response.raise_for_status = Mock()

        mock_session = Mock()
        mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.get.return_value.__aexit__ = AsyncMock(return_value=False)

        with patch("aiohttp.ClientSession") as mock_session_class, \
             patch("homeassistant.util.dt.now") as mock_now:

            mock_session_class.return_value.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session_class.return_value.__aexit__ = AsyncMock(return_value=False)

            mock_now.return_value = datetime(2026, 4, 7, 12, 0, 0)

            data = await mock_coordinator._async_update_data()

        collections = data["collections"]
        assert len(collections) == 1

        waste_types = collections[0]["waste_type"]
        assert len(waste_types) == 2
        assert WASTE_TYPE_COMPOST in waste_types
        assert WASTE_TYPE_GARBAGE in waste_types

    @pytest.mark.asyncio
    async def test_next_collection_identifies_earliest_date(self, mock_hass, sample_ics_data, mock_coordinator):
        """Test that next_collection returns the earliest upcoming collection."""
        mock_response = AsyncMock()
        mock_response.text.return_value = sample_ics_data
        mock_response.raise_for_status = Mock()

        mock_session = Mock()
        mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.get.return_value.__aexit__ = AsyncMock(return_value=False)

        with patch("aiohttp.ClientSession") as mock_session_class, \
             patch("homeassistant.util.dt.now") as mock_now:

            mock_session_class.return_value.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session_class.return_value.__aexit__ = AsyncMock(return_value=False)

            mock_now.return_value = datetime(2026, 4, 7, 12, 0, 0)

            data = await mock_coordinator._async_update_data()

        next_collection = data["next_collection"]
        assert next_collection is not None
        assert next_collection["date"] == date(2026, 4, 13)
        assert WASTE_TYPE_COMPOST in next_collection["waste_type"]
        assert WASTE_TYPE_GARBAGE in next_collection["waste_type"]

    @pytest.mark.asyncio
    async def test_events_before_today_filtered(self, mock_hass, mock_coordinator):
        """Test that events before today are filtered out."""
        ics_data = """BEGIN:VCALENDAR
PRODID:-//github.com/ical-org/ical.net//NONSGML ical.net 5.2.0//EN
VERSION:2.0
BEGIN:VEVENT
DTEND:20260405T071500
DTSTAMP:20260407T043926Z
DTSTART:20260405T070000
SEQUENCE:0
SUMMARY:Collecte des ordures
UID:test-past@example.com
END:VEVENT
BEGIN:VEVENT
DTEND:20260413T071500
DTSTAMP:20260407T043926Z
DTSTART:20260413T070000
SEQUENCE:0
SUMMARY:Compost
UID:test-future@example.com
END:VEVENT
END:VCALENDAR"""

        mock_response = AsyncMock()
        mock_response.text.return_value = ics_data
        mock_response.raise_for_status = Mock()

        mock_session = Mock()
        mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.get.return_value.__aexit__ = AsyncMock(return_value=False)

        with patch("aiohttp.ClientSession") as mock_session_class, \
             patch("homeassistant.util.dt.now") as mock_now:

            mock_session_class.return_value.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session_class.return_value.__aexit__ = AsyncMock(return_value=False)

            mock_now.return_value = datetime(2026, 4, 7, 12, 0, 0)

            data = await mock_coordinator._async_update_data()

        collections = data["collections"]
        assert len(collections) == 1
        assert collections[0]["date"] == date(2026, 4, 13)

    @pytest.mark.asyncio
    async def test_empty_calendar_returns_empty_collections(self, mock_hass, mock_coordinator):
        """Test that an empty calendar returns empty collections and None next_collection."""
        ics_data = """BEGIN:VCALENDAR
PRODID:-//github.com/ical-org/ical.net//NONSGML ical.net 5.2.0//EN
VERSION:2.0
END:VCALENDAR"""

        mock_response = AsyncMock()
        mock_response.text.return_value = ics_data
        mock_response.raise_for_status = Mock()

        mock_session = Mock()
        mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.get.return_value.__aexit__ = AsyncMock(return_value=False)

        with patch("aiohttp.ClientSession") as mock_session_class, \
             patch("homeassistant.util.dt.now") as mock_now:

            mock_session_class.return_value.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session_class.return_value.__aexit__ = AsyncMock(return_value=False)

            mock_now.return_value = datetime(2026, 4, 7, 12, 0, 0)

            data = await mock_coordinator._async_update_data()

        assert data["collections"] == []
        assert data["next_collection"] is None


class TestConstants:
    """Test that constants are properly defined."""

    def test_waste_type_mapping(self):
        """Test that waste type mapping includes expected terms."""
        from custom_components.sherbrooke_poubelle.const import WASTE_TYPE_MAPPING

        # French terms
        assert "ordures" in WASTE_TYPE_MAPPING
        assert "résidus alimentaires" in WASTE_TYPE_MAPPING
        assert "récupération" in WASTE_TYPE_MAPPING

        # English terms
        assert "waste" in WASTE_TYPE_MAPPING
        assert "recycling" in WASTE_TYPE_MAPPING
        assert "compost" in WASTE_TYPE_MAPPING

    def test_icons_defined(self):
        """Test that icons are defined for all waste types."""
        from custom_components.sherbrooke_poubelle.const import ICONS, WASTE_TYPE_GARBAGE, WASTE_TYPE_RECYCLING, WASTE_TYPE_COMPOST

        assert WASTE_TYPE_GARBAGE in ICONS
        assert WASTE_TYPE_RECYCLING in ICONS
        assert WASTE_TYPE_COMPOST in ICONS

        # Check they start with mdi:
        for icon in ICONS.values():
            assert icon.startswith("mdi:")

    def test_colors_defined(self):
        """Test that colors are defined for all waste types."""
        from custom_components.sherbrooke_poubelle.const import COLORS, WASTE_TYPE_GARBAGE, WASTE_TYPE_RECYCLING, WASTE_TYPE_COMPOST

        assert WASTE_TYPE_GARBAGE in COLORS
        assert WASTE_TYPE_RECYCLING in COLORS
        assert WASTE_TYPE_COMPOST in COLORS

        # Check they are valid hex colors
        for color in COLORS.values():
            assert color.startswith("#")
            assert len(color) == 7  # #RRGGBB

    def test_names_defined(self):
        """Test that display names are defined for all waste types."""
        from custom_components.sherbrooke_poubelle.const import WASTE_TYPE_NAMES, WASTE_TYPE_GARBAGE, WASTE_TYPE_RECYCLING, WASTE_TYPE_COMPOST

        assert WASTE_TYPE_GARBAGE in WASTE_TYPE_NAMES
        assert WASTE_TYPE_RECYCLING in WASTE_TYPE_NAMES
        assert WASTE_TYPE_COMPOST in WASTE_TYPE_NAMES


class TestConfigFlowConstants:
    """Test that config flow constants are defined."""

    def test_config_keys_exist(self):
        """Test that all config keys are defined."""
        from custom_components.sherbrooke_poubelle.const import (
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
        from custom_components.sherbrooke_poubelle.const import API_SEARCH_URL

        assert API_SEARCH_URL.startswith("https://")
        assert "sherbrooke.ca" in API_SEARCH_URL

