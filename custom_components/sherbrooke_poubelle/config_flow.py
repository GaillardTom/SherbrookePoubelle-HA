"""Config flow for Sherbrooke Waste Collection integration."""

import logging

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    CONF_ADDRESS_NUMBER,
    CONF_STREET_NAME,
    CONF_SELECTED_ADDRESS,
    CONF_CALENDAR_URL,
    CONF_SECTOR,
    CONF_COLLECTION_DAY,
    API_SEARCH_URL,
)

_LOGGER = logging.getLogger(__name__)

class SherbrookeWasteConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Sherbrooke Waste Collection."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self._address_number = None
        self._street_name = None
        self._addresses = []

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            self._address_number = user_input[CONF_ADDRESS_NUMBER]
            self._street_name = user_input[CONF_STREET_NAME]

            # Fetch matching addresses from API
            addresses = await self._fetch_addresses(
                self._address_number, self._street_name
            )

            if addresses:
                self._addresses = addresses
                return await self.async_step_select_address()
            else:
                errors["base"] = "no_addresses_found"

        data_schema = vol.Schema({
            vol.Required(CONF_ADDRESS_NUMBER): str,
            vol.Required(CONF_STREET_NAME): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_select_address(self, user_input=None):
        """Handle address selection step."""
        errors = {}

        if user_input is not None:
            selected_index = user_input[CONF_SELECTED_ADDRESS]
            selected = self._addresses[selected_index]

            # Create config entry
            return self.async_create_entry(
                title=selected["address"],
                data={
                    CONF_ADDRESS_NUMBER: self._address_number,
                    CONF_STREET_NAME: self._street_name,
                    CONF_SELECTED_ADDRESS: selected["address"],
                    CONF_CALENDAR_URL: selected["calendar_link"],
                    CONF_SECTOR: selected["sector"],
                    CONF_COLLECTION_DAY: selected["day"],
                },
            )

        # Build selection list
        address_choices = {
            i: f"{addr['address']} (Jour: {addr['day']})"
            for i, addr in enumerate(self._addresses)
        }

        data_schema = vol.Schema({
            vol.Required(CONF_SELECTED_ADDRESS): vol.In(address_choices),
        })

        return self.async_show_form(
            step_id="select_address",
            data_schema=data_schema,
            errors=errors,
        )

    async def _fetch_addresses(self, address_number: str, street_name: str):
        """Fetch matching addresses from Sherbrooke API."""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Accept": "application/json, text/plain, */*",
                    "Content-Type": "application/json",
                    "Origin": "https://www.sherbrooke.ca",
                    "Referer": "https://www.sherbrooke.ca/fr/services-a-la-population/collecte-des-matieres-residuelles/calendrier-des-collectes",
                }
                payload = {
                    "address": address_number,
                    "street": street_name,
                }

                async with session.post(
                    API_SEARCH_URL,
                    headers=headers,
                    json=payload,
                    timeout=30,
                ) as response:
                    response.raise_for_status()
                    data = await response.json()

                    # Parse and format results
                    addresses = []
                    for item in data:
                        # Extract sector from calendar link
                        # URL format: .../sectors/01/days/Lundi/ics
                        calendar_link = item.get("calendarLink", "")
                        sector = self._extract_sector(calendar_link)

                        addresses.append({
                            "address": item.get("address"),
                            "day": item.get("day"),
                            "calendar_link": calendar_link,
                            "sector": sector,
                            "pdf": item.get("pdf"),
                        })

                    return addresses

        except Exception as err:
            _LOGGER.error("Error fetching addresses: %s", err)
            return []

    @staticmethod
    def _extract_sector(calendar_link: str) -> str:
        """Extract sector from calendar URL."""
        # URL format: .../sectors/01/days/Lundi/ics
        try:
            parts = calendar_link.split("/")
            if "sectors" in parts:
                sector_idx = parts.index("sectors") + 1
                return parts[sector_idx]
        except (ValueError, IndexError):
            pass
        return "unknown"


