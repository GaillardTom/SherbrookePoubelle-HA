"""Sensor platform for Sherbrooke Waste Collection."""

from datetime import datetime, timedelta
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    CONF_ADDRESS_NUMBER,
    CONF_STREET_NAME,
    CONF_SELECTED_ADDRESS,
    CONF_SECTOR,
    CONF_COLLECTION_DAY,
    WASTE_TYPE_GARBAGE,
    WASTE_TYPE_RECYCLING,
    WASTE_TYPE_COMPOST,
    ICONS,
    COLORS,
    WASTE_TYPE_NAMES,
)
from .coordinator import SherbrookeWasteCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        NextCollectionSensor(coordinator, entry),
        CollectionCountdownSensor(coordinator, entry),
    ]

    async_add_entities(sensors)


class NextCollectionSensor(CoordinatorEntity, SensorEntity):
    """Sensor showing the next waste collection."""

    _attr_has_entity_name = True
    _attr_translation_key = "next_collection"

    def __init__(self, coordinator: SherbrookeWasteCoordinator, entry: ConfigEntry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_next_collection"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"Poubelle - {entry.data[CONF_SELECTED_ADDRESS]}",
            manufacturer="Ville de Sherbrooke",
            model=f"Sector {entry.data[CONF_SECTOR]}",
        )

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None

        next_collection = self.coordinator.data.get("next_collection")
        if not next_collection:
            return "Unknown"

        # Return display name for waste type
        waste_type = next_collection["waste_type"]
        return WASTE_TYPE_NAMES.get(waste_type, waste_type)

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        if not self.coordinator.data:
            return {}

        next_collection = self.coordinator.data.get("next_collection")
        if not next_collection:
            return {}

        collection_date = next_collection["date"]
        days_until = (collection_date - datetime.now().date()).days

        return {
            "collection_date": collection_date.isoformat(),
            "waste_type": next_collection["waste_type"],
            "days_until": days_until,
            "raw_summary": next_collection.get("raw_summary", ""),
        }

    @property
    def icon(self):
        """Return the icon based on waste type."""
        if not self.coordinator.data:
            return "mdi:trash-can"

        next_collection = self.coordinator.data.get("next_collection")
        if not next_collection:
            return "mdi:trash-can"

        waste_type = next_collection["waste_type"]
        return ICONS.get(waste_type, "mdi:trash-can")

    @property
    def device_class(self):
        """Return the device class."""
        return None


class CollectionCountdownSensor(CoordinatorEntity, SensorEntity):
    """Sensor showing days until next collection."""

    _attr_has_entity_name = True
    _attr_translation_key = "collection_countdown"

    def __init__(self, coordinator: SherbrookeWasteCoordinator, entry: ConfigEntry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_countdown"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"Waste Collection - {entry.data[CONF_SELECTED_ADDRESS]}",
            manufacturer="Ville de Sherbrooke",
            model=f"Sector {entry.data[CONF_SECTOR]}",
        )

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None

        next_collection = self.coordinator.data.get("next_collection")
        if not next_collection:
            return None

        collection_date = next_collection["date"]
        days_until = (collection_date - datetime.now().date()).days

        return days_until

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        if not self.coordinator.data:
            return {}

        next_collection = self.coordinator.data.get("next_collection")
        if not next_collection:
            return {}

        collection_date = next_collection["date"]

        return {
            "collection_date": collection_date.isoformat(),
            "waste_type": next_collection["waste_type"],
        }

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "days"

    @property
    def icon(self):
        """Return the icon."""
        if not self.coordinator.data:
            return "mdi:calendar-clock"

        next_collection = self.coordinator.data.get("next_collection")
        if not next_collection:
            return "mdi:calendar-clock"

        days_until = (next_collection["date"] - datetime.now().date()).days

        if days_until == 0:
            return "mdi:calendar-today"
        elif days_until == 1:
            return "mdi:calendar-tomorrow"
        else:
            return "mdi:calendar-clock"
