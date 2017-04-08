"""
Adding Darksky Capability for weather.

Darksky is copyright https://darksky.net - See 
"""
import datetime
import requests
import json
import os
print(os.environ)
DARKSKY_API_KEY = os.environ.get('DARKSKY_API_KEY')
DEBUG = False
LATITUDE = os.environ.get('LATITUDE')
LONGITUDE = os.environ.get('LONGITUDE')


def get_darksky_data(latitude=LATITUDE, longitude=LONGITUDE):
    if DEBUG:
        if os.path.exists('./darksky_data.json'):  # remove "False" to debug and NOT pull from live.
            print("Pulling from DISK")
            data = open('./darksky_data.json', 'r').read()
    else:
        print("Pulling from LIVE")
        url = f"https://api.darksky.net/forecast/{DARKSKY_API_KEY}/{latitude},{longitude}"
        print(url)
        data = requests.get(url).text
    if DEBUG:
        open('./darksky_data.json', 'w').write(data)
    return json.loads(data)




# The icon_map is used to map Darksky values to Slack Icons.  Feel free to change this to icons of your choice in Slack.
icon_map = {
    'partly-cloudy-day': ':partly_sunny:',
    'partly-cloudy-night': ':partly_sunny:',
    'rain': ':rain_cloud:',
    'clear-day': ':sunny:',
    'clear-night': ':moon:',
    'cloudy': ':cloud:'
}


def get_week_forecast():
    data = get_darksky_data()
    daily_data = data.get('daily').get('data')
    # first return is current day:
    forecast = ""
    for i, d in enumerate(daily_data):
        if i == 0:
            day = "Today"
        else:
            day = datetime.datetime.fromtimestamp(d.get('time')).strftime('%A - (%m/%d):')
        forecast += f"{day} {icon_map.get(d.get('icon'))} {d.get('summary')} High: {d.get('temperatureMax'):.0f}F Low: {d.get('temperatureMin'):.0f}F Wind: {d.get('windSpeed'):.0f}mph from the {get_wind_direction(d.get('windBearing'))}"
        forecast += "\n"
    forecast += "Powered by Darksky - https://darksky.net/poweredby/\n"
    return forecast

def get_summary_forecast():
    return data.get('daily').get('summary')

def get_wind_direction(wind_bearing):
    if wind_bearing <= 22.5:
        return "North"
    if wind_bearing <= 67.5:
        return "Northeast"
    if wind_bearing <= 112.5:
        return"East"
    if wind_bearing <= 157.5:
        return "Southeast"
    if wind_bearing <= 202.5:
        return "South"
    if wind_bearing <= 247.5:
        return "Southwest"
    if wind_bearing <= 292.5:
        return "West"
    if wind_bearing <= 337.5:
        return "Northwest"
    return "North"

def get_current_weather():
    data = get_darksky_data()
    current = data.get('currently')
    current_conditions = current.get('summary')
    temperature = current.get('temperature')
    apparent_temperature = current.get('apparentTemperature')
    icon = icon_map.get(current.get('icon'))
    wind_speed = current.get('windSpeed')
    wind_bearing = current.get('windBearing')
    wind_direction = get_wind_direction(wind_bearing)
    ret = f"Currently, it's {current_conditions} {icon} and {temperature:.0f} degrees.  It feels like it's {apparent_temperature:.0f} degrees.   Wind is out of the {wind_direction} at {wind_speed:.0f} mph."
    ret += "\nPowered by Darksky: https://darksky.net/poweredby/\n"
    return ret

if __name__ == "__main__":
    #print(get_daily_forecast())
    print(get_current_weather())
    #print(get_summary_forecast())
    print(get_week_forecast())