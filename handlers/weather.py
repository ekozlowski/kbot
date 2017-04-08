help_text = "`weather` coming soon :slightly_smiling_face:"

from . import darksky


def handle(command):
    pieces = command.split()
    try:
        command = pieces[1]
    except IndexError:
        return darksky.get_current_weather()
    if command.lower() == 'help':
        message = """
I can display a weather summary, or a weekly forecast.
For a weekly forecast, tell me `@kbot weather weekly`.
For current conditions, just tell me `@kbot weather`.

        """
        return message
    if command.lower() == 'weekly':
        return darksky.get_week_forecast()

