"""Notification service for Sherbrooke Waste Collection."""

import logging
from datetime import datetime, timedelta

from homeassistant.components.notify import NotifyEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_change
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    CONF_SELECTED_ADDRESS,
    DEFAULT_NOTIFICATION_TIME,
    NOTIFICATION_DAYS_BEFORE,
    WASTE_TYPE_NAMES,
    WASTE_TYPE_GARBAGE,
    WASTE_TYPE_RECYCLING,
    WASTE_TYPE_COMPOST,
)
from .coordinator import SherbrookeWasteCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the notification entity."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    notify_entity = WasteCollectionNotifyEntity(coordinator, entry)
    async_add_entities([notify_entity])

    # Schedule daily check at notification time
    notify_entity.async_schedule_check(hass)


class WasteCollectionNotifyEntity(NotifyEntity):
    """Notify entity for waste collection reminders."""

    _attr_has_entity_name = True
    _attr_translation_key = "waste_notification"

    def __init__(self, coordinator: SherbrookeWasteCoordinator, entry: ConfigEntry):
        """Initialize the notify entity."""
        super().__init__()
        self.coordinator = coordinator
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_notification"
        self._attr_name = "Waste Collection Notification"
        self._notification_sent_today = False
        self._last_check_date = None

    def async_schedule_check(self, hass: HomeAssistant) -> None:
        """Schedule the daily notification check."""
        # Parse default notification time (19:00)
        hour, minute = map(int, DEFAULT_NOTIFICATION_TIME.split(":"))

        async_track_time_change(
            hass,
            self._async_check_and_notify,
            hour=hour,
            minute=minute,
            second=0,
        )
        _LOGGER.debug(
            "Scheduled waste collection check for %02d:%02d",
            hour, minute
        )

    async def _async_check_and_notify(self, now: datetime) -> None:
        """Check if notification should be sent."""
        today = now.date()

        # Reset flag if it's a new day
        if self._last_check_date != today:
            self._notification_sent_today = False
            self._last_check_date = today

        if self._notification_sent_today:
            return

        if not self.coordinator.data:
            return

        next_collection = self.coordinator.data.get("next_collection")
        if not next_collection:
            return

        collection_date = next_collection["date"]
        days_until = (collection_date - today).days

        # Notify the day before (or configured days before)
        if days_until == NOTIFICATION_DAYS_BEFORE:
            waste_type = next_collection["waste_type"]
            waste_name = WASTE_TYPE_NAMES.get(waste_type, waste_type)

            message = self._build_notification_message(
                waste_name, collection_date, days_until
            )

            await self.async_send_message(message)
            self._notification_sent_today = True
            _LOGGER.info("Sent waste collection notification: %s", message)

    def _build_notification_message(
        self, waste_name: str, collection_date: datetime.date, days_until: int
    ) -> str:
        """Build the notification message."""
        date_str = collection_date.strftime("%A %B %d")  # e.g., "Thursday January 15"

        if days_until == 1:
            when = "tomorrow"
        elif days_until == 0:
            when = "today"
        else:
            when = f"in {days_until} days ({date_str})"

        return f"🗑️ Waste Collection Reminder: Put out the {waste_name} bin {when}!"

    async def async_send_message(self, message: str, title: str = None) -> None:
        """Send a notification message (required by NotifyEntity)."""
        # This will be handled by Home Assistant's notification system
        # The entity state will contain the message
        self._attr_available = True
        self._attr_message = message
        self.async_write_ha_state()
