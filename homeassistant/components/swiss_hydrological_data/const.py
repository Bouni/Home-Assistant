"""Constants for Swiss Hydrological Data integration."""

from datetime import timedelta
from typing import Final

DOMAIN = "swiss_hydrological_data"
STATION_ID = "station_id"
CONF_STATION: Final = "station"
CONF_STATION_MONITORED_CONDITIONS: Final = "monitored_conditions"
CONF_CONDITION_TEMPERATURE: Final = "temperature"
CONF_CONDITION_LEVEL: Final = "level"
CONF_CONDITION_DISCHARGE: Final = "discharge"
CONF_STATION_KEY_ID: Final = "id"
CONF_STATION_KEY_NAME: Final = "name"
CONF_STATION_KEY_WATER_BODY_NAME: Final = "water-body-name"
CONF_STATION_KEY_WATER_BODY_TYPE: Final = "water-body-type"
DEFAULT_TIME_MODE = "now"
PLACEHOLDERS = {
    "stationboard_url": "http://transport.opendata.ch/examples/stationboard.html",
    "opendata_url": "http://transport.opendata.ch",
}
ATTR_MAX_24H = "max-24h"
ATTR_MEAN_24H = "mean-24h"
ATTR_MIN_24H = "min-24h"
ATTR_STATION = "station"
ATTR_STATION_UPDATE = "station_update"
ATTR_WATER_BODY = "water_body"
ATTR_WATER_BODY_TYPE = "water_body_type"

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=60)

SENSOR_DISCHARGE = "discharge"
SENSOR_LEVEL = "level"
SENSOR_TEMPERATURE = "temperature"

CONDITIONS = {
    SENSOR_DISCHARGE: "mdi:waves-arrow-right",
    SENSOR_LEVEL: "mdi:waves-arrow-up",
    SENSOR_TEMPERATURE: "mdi:thermometer-water",
}

CONDITION_DETAILS = [
    ATTR_MAX_24H,
    ATTR_MEAN_24H,
    ATTR_MIN_24H,
]
