"""DataUpdateCoordinator for Sherbrooke Waste Collection."""

import asyncio
from datetime import datetime, timedelta
import logging

import aiohttp
import icalendar
import recurring_ical_events

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    DOMAIN,
    UPDATE_INTERVAL,
    WASTE_TYPE_GARBAGE,
    WASTE_TYPE_RECYCLING,
    WASTE_TYPE_COMPOST,
    WASTE_TYPE_MAPPING,
)

_LOGGER = logging.getLogger(__name__)


class SherbrookeWasteCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch waste collection data from ICS calendar."""

    def __init__(self, hass: HomeAssistant, calendar_url: str):
        """Initialize the coordinator."""
        self.calendar_url = calendar_url
        self._calendar = None

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    async def _async_update_data(self):
        """Fetch and parse the ICS calendar."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.calendar_url, timeout=30) as response:
                    response.raise_for_status()
                    ics_data = await response.text()

            # Parse ICS data
            calendar = icalendar.Calendar.from_ical(ics_data)

            # Get events for next 7 days
            today = datetime.now().date()
            end_date = today + timedelta(days=7)

            events = recurring_ical_events.of(calendar).between(today, end_date)

            # Process events into structured data
            collections = []
            for event in events:
                summary = str(event.get("summary", "")).lower()
                dtstart = event.get("dtstart").dt

                # Determine waste type from summary
                waste_type = self._detect_waste_type(summary)

                if isinstance(dtstart, datetime):
                    event_date = dtstart.date()
                else:
                    event_date = dtstart

                collections.append({
                    "date": event_date,
                    "waste_type": waste_type,
                    "summary": summary,
                    "raw_summary": str(event.get("summary", "")),
                })

            # Sort by date
            collections.sort(key=lambda x: x["date"])

            return {
                "collections": collections,
                "next_collection": collections[0] if collections else None,
            }

        except Exception as err:
            _LOGGER.error("Error fetching waste collection data: %s", err)
            raise

    def _detect_waste_type(self, summary: str) -> str:
        """Detect waste type from event summary."""
        summary_lower = summary.lower()

        for keyword, waste_type in WASTE_TYPE_MAPPING.items():
            if keyword in summary_lower:
                return waste_type

        # Default to garbage if can't determine
        _LOGGER.debug("Could not determine waste type for: %s", summary)
        return WASTE_TYPE_GARBAGE
