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
            grouped_collections = {}


            for event in events:
                summary = str(event.get("summary", "")).lower()
                dtstart = event.get("dtstart").dt
                event_date = dtstart.date() if isinstance(dtstart, datetime) else dtstart

                # Détecter les types pour cet événement précis
                current_types = self._detect_waste_type(summary)

                _LOGGER.debug("Event: date=%s, summary='%s', detected_types=%s", event_date, summary, current_types)

                if event_date not in grouped_collections:
                    grouped_collections[event_date] = set()

                # Ajouter les types trouvés au set de cette date
                for t in current_types:
                    grouped_collections[event_date].add(t)

            # Transformer le dictionnaire en liste triée pour Home Assistant
            final_collections = []
            for date, types in grouped_collections.items():
                final_collections.append({
                    "date": date,
                    "waste_type": list(types), # On repasse en liste pour le sensor
                })

            final_collections.sort(key=lambda x: x["date"])

            return {
                "collections": final_collections,
                "next_collection": final_collections[0] if final_collections else None,
            }

        except Exception as err:
            _LOGGER.error("Error fetching waste collection data: %s", err)
            raise

    def _detect_waste_type(self, summary: str) -> list:
        """Detect waste type from event summary."""
        summary_lower = summary.lower()
        waste_types_found = set()
        for keyword, waste_type in WASTE_TYPE_MAPPING.items():
            if keyword in summary_lower:
                waste_types_found.add(waste_type)

        # Default to garbage if can't determine
        return list(waste_types_found) if waste_types_found else [WASTE_TYPE_GARBAGE]
