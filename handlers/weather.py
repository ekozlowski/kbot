help_text = "`weather` Get weather information.  Powered by Darksky - https://darksky.net/poweredby/"

from . import darksky

import os
from functools import lru_cache


@lru_cache(maxsize=1, typed=False)
def preflight_check():
    ret = ""
    if not os.environ.get("DARKSKY_API_KEY"):
        ret += "You need to add your Darksky API key to the DARKSKY_API_KEY.\n"
    if not os.environ.get("LATITUDE") or not os.environ.get("LONGITUDE"):
        ret += "You need to add your latitude and longitude to the 'LATITUDE' and 'LONGITUDE' environment variables.\n"
    return ret


def handle(command, callback):
    msg = preflight_check()
    if msg:
        return msg
    pieces = command.split()
    try:
        command = pieces[1]
    except IndexError:
        callback(darksky.get_current_weather())
    if command.lower() == "help":
        callback(
            """
I can display a weather summary, or a weekly forecast.
For a weekly forecast, tell me `@kbot weather weekly`.
For current conditions, just tell me `@kbot weather`.
        """
        )
        return
    if command.lower() == "weekly":
        callback(darksky.get_week_forecast())
