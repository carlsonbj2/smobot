"""File with class for Local Smobot."""
import aiohttp
import json
import asyncio
import time

from .smobot_status import SmobotStatus

# This is all based on Firmware version (4), which is the latest
# available as of 251228

class Smobot:
    """Class for talking with Smobot Locally."""

    # Assumes we're in F, but the API doesn't tell us
    # what the configuration is.
    MAX_SETPOINT = 600
    MIN_SETPOINT = 180

    def __init__(self, ip: str):
        """Create the smobot client.

        Arguments:
            ip {string} -- ip address of the Smobot.
        """
        self._ip = ip
        self._base_url = f"http://{self._ip}/ajax/"
        self._headers = {
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-us",
        }
        self.session = aiohttp.ClientSession(
            headers=self._headers, raise_for_status=True
        )
        self._status = None

    async def close(self):
        """Close the session."""
        return await self.session.close()

    @property
    async def status(self):
        """Get status."""
        if not self._status:
            await self.update_status()
        return self._status

    async def update_status(self):
        """Update the status of your smobot."""
        async with self.session.get(self._base_url + "smobot") as response:
            full_state = await response.json()
            self._status = SmobotStatus(**full_state)

    async def post_setpoint(self, setpoint):
        """Set the setpoint for the smobot."""

        if setpoint > Smobot.MAX_SETPOINT or setpoint < Smobot.MIN_SETPOINT:
            raise ValueError("Setpoint must be within range {} to {}".format(
                Smobot.MIN_SETPOINT, Smobot.MAX_SETPOINT
            ))

        body = {"setpoint": str(setpoint)}

        # Always returns "OK", even if the setpoint was invalid
        # and coereced down - not JSON.
        async with self.session.post(
            self._base_url + "setgrillset", data=body
        ) as response:
            return await response.text()
