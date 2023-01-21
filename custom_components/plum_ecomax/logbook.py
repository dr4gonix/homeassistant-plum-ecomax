"""Describe Plum ecoMAX logbook events."""
from __future__ import annotations

from collections.abc import Callable

from homeassistant.components.logbook.const import (
    LOGBOOK_ENTRY_MESSAGE,
    LOGBOOK_ENTRY_NAME,
)
from homeassistant.core import Event, HomeAssistant, callback
from pyplumio.const import AlertType

from custom_components.plum_ecomax.const import (
    ATTR_CODE,
    ATTR_FROM,
    ATTR_TO,
    DOMAIN,
    EVENT_PLUM_ECOMAX_ALERT,
)

ALERT_TYPES: dict[AlertType, str] = {
    AlertType.POWER_LOSS: "Encountered power loss",
    AlertType.BOILER_TEMP_SENSOR_FAILURE: "Encountered boiler temperature sensor failure",
    AlertType.MAX_BOILER_TEMP_EXCEEDED: "Maximum boiler temperature exceeded",
    AlertType.FEEDER_TEMP_SENSOR_FAILURE: "Encountered feeder temperature sensor failure",
    AlertType.MAX_FEEDER_TEMP_EXCEEDED: "Maximum feeder temperature exceeded",
    AlertType.EXHAUST_TEMP_SENSOR_FAILURE: "Exhaust temperature sensor failed",
    AlertType.KINDLING_FAILURE: "Encountered kindling failure",
    AlertType.FAN_FAILURE: "Encountered fan failure",
}


@callback
def async_describe_events(
    hass: HomeAssistant,
    async_describe_event: Callable[[str, str, Callable[[Event], dict[str, str]]], None],
) -> None:
    """Describe logbook events."""

    @callback
    def async_describe_alert_event(event: Event) -> dict[str, str]:
        """Describe ecomax logbook event."""
        alert_code = event.data[ATTR_CODE]
        start_time = event.data[ATTR_FROM]
        time_string = f"from {start_time}"

        try:
            end_time = event.data[ATTR_TO]
            time_string += f" to {end_time}"
        except KeyError:
            pass

        alert_string = ALERT_TYPES.get(
            alert_code, f'Encountered alert with code "{alert_code}"'
        )

        return {
            LOGBOOK_ENTRY_NAME: "ecoMAX",
            LOGBOOK_ENTRY_MESSAGE: f"{alert_string} {time_string}",
        }

    async_describe_event(DOMAIN, EVENT_PLUM_ECOMAX_ALERT, async_describe_alert_event)
