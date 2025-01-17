"""Config flow for Swiss Hydrological Data integration."""

from typing import Any

from swisshydrodata import SwissHydroData
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
)

from .const import (
    CONF_STATION,
    CONF_STATION_KEY_ID,
    CONF_STATION_KEY_NAME,
    CONF_STATION_KEY_WATER_BODY_NAME,
    CONF_STATION_MONITORED_CONDITIONS,
    DOMAIN,
)


class SwissHydroDataConfigFlow(ConfigFlow, domain=DOMAIN):
    """Swiss Hydrological Data config flow."""

    VERSION = 1
    MINOR_VERSION = 1

    user_input: dict[str, Any]

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Async user step to set up a station."""

        errors: dict[str, str] = {}

        if user_input is not None:
            station_id = user_input[CONF_STATION]
            conditions = await self.get_conditions(station_id)
            user_input[CONF_STATION_MONITORED_CONDITIONS] = conditions
            unique_id = f"swiss_hydro_data_{station_id}"
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=unique_id,
                data=user_input,
            )

        stations = await self.get_station_list()

        options = [
            SelectOptionDict(
                value=station["id"],
                label=f"{station[CONF_STATION_KEY_ID]}: {station[CONF_STATION_KEY_NAME]} ({station[CONF_STATION_KEY_WATER_BODY_NAME]})",
            )
            for station in stations
        ]

        return self.async_show_form(
            step_id="user",
            errors=errors,
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_STATION): SelectSelector(
                        SelectSelectorConfig(options=options, sort=True),
                    ),
                }
            ),
        )

    async def get_conditions(self, station_id: str) -> list:
        """Get monitored conditions for a certain station."""
        session = async_get_clientsession(self.hass)
        shd = SwissHydroData(session)
        station_data = await shd.async_get_station(station_id)
        return list(station_data["parameters"].keys())

    async def get_station_list(self) -> list:
        """Get a list of all available stations."""
        session = async_get_clientsession(self.hass)
        shd = SwissHydroData(session)
        return await shd.async_get_stations() or []
