"""Support for hydrological data from the Fed. Office for the Environment."""

import logging

from swisshydrodata import SwissHydroData

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util import Throttle

from .const import (
    ATTR_MAX_24H,
    ATTR_MEAN_24H,
    ATTR_MIN_24H,
    ATTR_STATION,
    ATTR_STATION_UPDATE,
    ATTR_WATER_BODY_TYPE,
    CONDITIONS,
    CONF_STATION_MONITORED_CONDITIONS,
    MIN_TIME_BETWEEN_UPDATES,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform."""
    station = config_entry.data.get("station")

    for condition in config_entry.data.get(CONF_STATION_MONITORED_CONDITIONS):
        async_add_entities([SwissHydrologicalDataSensor(station, condition)], True)


class SwissHydrologicalDataSensor(SensorEntity):
    """Implementation of a Swiss hydrological sensor."""

    _attr_attribution = (
        "Data provided by the Swiss Federal Office for the Environment FOEN"
    )

    def __init__(self, station, condition):
        """Initialize the Swiss hydrological sensor."""
        self._condition = condition
        self._state = None
        self._name = None
        self._unit = None
        self._water_body_name = None
        self._attrs = {}
        self._icon = CONDITIONS[condition]
        self._station = station

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._water_body_name} {self._name} {self._condition}"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if isinstance(self._state, (int, float)):
            return round(self._state, 2)
        return None

    @property
    def extra_state_attributes(self):
        """Return the device state attributes."""
        return self._attrs

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return self._icon

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Fetch new state data."""
        session = async_get_clientsession(self.hass)
        shd = SwissHydroData(session)
        data = await shd.async_get_station(self._station)
        if data is None:
            self._state = None
        else:
            self._name = data["name"]
            self._state = data["parameters"][self._condition]["value"]
            self._unit = data["parameters"][self._condition]["unit"]
            self._water_body_name = data["water-body-name"]
            self._attrs = {
                ATTR_WATER_BODY_TYPE: data["water-body-type"],
                ATTR_STATION: data["name"],
                ATTR_STATION_UPDATE: data["parameters"][self._condition]["datetime"],
                ATTR_MAX_24H: data["parameters"][self._condition]["max-24h"],
                ATTR_MEAN_24H: data["parameters"][self._condition]["mean-24h"],
                ATTR_MIN_24H: data["parameters"][self._condition]["min-24h"],
            }
