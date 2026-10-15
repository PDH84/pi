"""
Weather Station V2.py
written by Peter Harrison
9/15/26

Running Weather_Station_V2.py will print all information to the command line,
while running Weather_Station_V2.py --write will write to the file and send a
meshcore message.

Has not been throughly error tested.
"""
import asyncio
from meshcore import MeshCore, EventType
import adafruit_dht
import adafruit_bme680
import board
import time
import os
import requests
import pandas as pd
from datetime import datetime
import sys


def write_file_headers(filename):
    file_exists = os.path.isfile(filename)

    if not file_exists:
        file = open(filename, 'w')
        file.write(
            'Date, Time, Indoor temperature (ºF), Indoor humidity (%), Outdoor temperature (ºF), Outdoor humidity (%), Pressure (hPa), Air quality (ohms), Web temperature (ºF), Web humidity (%)\n')
        file.close()

    return None

def convert_units(reading, units):
    if units == 'imperial':
        converted_units = round((reading * (9 / 5) + 32),1)
    elif units == 'metric':
        converted_units = round(reading, 1)
    elif units == 'hPa':
        converted_units = round(reading, 1)
    elif units == 'inHG':
        converted_units = round((reading * 0.029529980572285), 2)
    else:
        converted_units = reading

    return converted_units

def read_DHT22(indoor_sensor, temp_units):
    # reads indoor DHT22 sensor
    try:
        in_temp = convert_units(indoor_sensor.temperature, temp_units)
        in_humidity = indoor_sensor.humidity
        indoor_sensor.exit()

    except ValueError:
        in_temp = 0.0
        in_humidity = 0.0
        indoor_sensor.exit()

    return in_temp, in_humidity

def readBME680(temp_units, pressure_units):
    # read BME680 sensor
    i2c = board.I2C()  # must use board.SCL (pin5) and board.SDA (pin3)
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
    bme680.sea_level_pressure = 1017.74804

    try:
        out_temp = convert_units(bme680.temperature, temp_units)
        out_pressure = convert_units(bme680.pressure, pressure_units)
        out_humidity = round(bme680.relative_humidity, 1)
        out_aq = bme680.gas

    except ValueError:
        out_temp = 0.0
        out_pressure = 0.0
        out_aq = 0.0

    return out_temp, out_humidity, out_pressure, out_aq

def scrape_web(city_name, api_key, temp_units):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": temp_units
# if this doesn't work hard write "imperial" for temp_units
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        outdoor_temp = data['main']['temp']
        outdoor_humidity = data['main']['humidity']
        description = data['weather'][0]['description']

    else:
        print("Error: API request failed.")
        outdoor_temp = 0.0
        outdoor_humidity = 0.0

    return outdoor_temp, outdoor_humidity

def write_file(file, in_temp, in_humidity, out_temp, out_humidity, out_pressure, out_aq, web_temp, web_humidity):
    file = open(filename, 'a+')
    # save time, date, temperature, and humidity in .txt file
    file.write(time.strftime('%m/%d/%Y') + ', ' + time.strftime('%H:%M:%S') + ', {:.1f}, {:.1f}, {:.1f}, {:.1f}, {:.1f}, {:.0f}, {:.1f}, {:.1f}\n'.format(
        in_temp, in_humidity, out_temp, out_humidity, out_pressure, out_aq, web_temp, web_humidity))
    file.close()

    pass

def read_file(filename):
    weather_df = pd.read_csv(filename)

    return weather_df

def get_trends(weather_df):
    current_pressure = weather_df.iloc[-1,6]
    past_pressure_1_hr = weather_df.iloc[-5, 6]
    past_pressure_3_hr = weather_df.iloc[-13, 6]
    past_pressure_24_hr = weather_df.iloc[-96, 6]
    hourly_trend = round((current_pressure - past_pressure_1_hr), 1)
    three_hour_trend = round((current_pressure - past_pressure_3_hr), 1)
    daily_trend = round((current_pressure - past_pressure_24_hr), 1)

    return hourly_trend, three_hour_trend, daily_trend

def determine_alert_status(three_hour_trend, alert_threshold):
    if three_hour_trend <= alert_threshold:
        alert_status = "alert"
    else:
        alert_status = "normal"

    return alert_status

def determine_schedule_status(schedule):
    if schedule == "max":
        schedule_status = "send"
    elif schedule == "1hour":
        now = datetime.now()
        current_min = int(now.strftime("%M"))
        if current_min <= 15:
            schedule_status = "send"
        else:
            schedule_status = "hold"
    elif schedule == "3hour":
        now = datetime.now()
        current_min = int(now.strftime("%M"))
        current_hour = int(now.strftime("%H"))
        if current_min <= 15 and current_hour % 3 == 0:
            schedule_status = "send"
        else:
            schedule_status = "hold"
    elif schedule == "6hour":
        now = datetime.now()
        current_min = int(now.strftime("%M"))
        current_hour = int(now.strftime("%H"))
        if current_min <= 15 and current_hour % 6 == 0:
            schedule_status = "send"
        else:
            schedule_status = "hold"
    elif schedule == "12hour":
        now = datetime.now()
        current_min = int(now.strftime("%M"))
        current_hour = int(now.strftime("%H"))
        if current_min <= 15 and current_hour % 24 == 0:
            schedule_status = "send"
        else:
            schedule_status = "hold"
    elif schedule == "daily":
        now = datetime.now()
        current_min = int(now.strftime("%M"))
        current_hour = int(now.strftime("%H"))
        if current_min <= 15 and current_hour == 12:
            schedule_status = "send"
        else:
            schedule_status = "hold"
    else:
        schedule_status = "hold"

    return schedule_status

def create_automated_message(alert_status, out_temp, out_humidity, out_pressure, three_hour_trend):
    if alert_status == "alert":
        automated_message = "A significant ({0:0.f} hPa) pressure drop has been detected.  Possible thunderstorm.\n\nTemperature= {1:0.1f}ºF\nHumidity= {2:0.1f}%\nPressure= {3:0.1f}hPa\nPressure trend (last 3 hours)= {4:0.1f}hPa".format(three_hour_trend, out_temp, out_humidity, out_pressure, three_hour_trend)
    else:
        automated_message = "Temperature= {0:0.1f}ºF\nHumidity= {1:0.1f}%\nPressure= {2:0.1f}hPa\nPressure trend (last 3 hours)= {3:0.1f}hPa".format(out_temp, out_humidity, out_pressure, three_hour_trend)

    return automated_message

# program config
filename = 'test_weather_data.txt'
temp_units = 'imperial'   # imperial and metric available currently
pressure_units = 'hPa'    # hPa and inHg available currently
alert_threshold = -4.0    # must be in hPa
schedule = 'max'          # options are max, 1hour, 3hour, 6hour, 12hour, daily

# config for API and sensors
api_key = "870fac250dfc0e6d0519f57b39b1ca81"
city = "Woodstown"
indoor_sensor = adafruit_dht.DHT22(board.D4)   # pin 4


if len(sys.argv) > 1 and sys.argv[1] == '--write':
    write_to_file = True
else:
    write_to_file = False

write_file_headers(filename)

in_temp, in_humidity = read_DHT22(indoor_sensor, temp_units)
out_temp, out_humidity, out_pressure, out_aq = readBME680(temp_units, pressure_units)
web_temp, web_humidity = scrape_web(city, api_key, temp_units)
if write_to_file:
    write_file(filename, in_temp, in_humidity, out_temp, out_humidity, out_pressure, out_aq, web_temp, web_humidity)
weather_df = read_file(filename)
hourly_trend, three_hour_trend, daily_trend = get_trends(weather_df)
alert_status = determine_alert_status(three_hour_trend, alert_threshold)
schedule_status = determine_schedule_status(schedule)
automated_message = create_automated_message(alert_status, out_temp, out_humidity, out_pressure, three_hour_trend)

if not write_to_file:
    schedule_status = "hold"

if schedule_status == "send" or alert_status == "alert":
    async def send_channel_message():
        # Connect to the MeshCore device via serial
        meshcore = await MeshCore.create_serial("/dev/ttyACM0")

        try:
            # Send message to channel index 0 (Public Channel)
            result = await meshcore.commands.send_chan_msg(
                chan=2,
                msg=automated_message,
                timestamp=None
            )

            if result.type == EventType.ERROR:
                print(f"Error: {result.payload}")
            else:
                print("Message sent successfully.")

        finally:
            await meshcore.disconnect()

    asyncio.run(send_channel_message())

# print readings on the shell
print("Inside temp:                       ", in_temp, "ºF")
print("Inside humidity:                   ", in_humidity, "%")
print("Outside temp:                      ", out_temp, "ºF")
print("Outdoor humidity:                  ", out_humidity, "%")
print("Pressure:                          ", out_pressure, "hPa")
print("Pressure tend in past hour:        ", hourly_trend, "hPa")
print("Pressure tend in past three hours: ", three_hour_trend, "hPa")
print("Pressure tend in past day:         ", daily_trend, "hPa")
print("Air quality:                       ", out_aq, " ohms")
print("Reported temp:                     ", web_temp, "ºF")
print("Reported humidity:                 ", web_humidity, "%")

print("Calculating dww point...")
dew_point = (out_temp - (out_humidity - 100)/5)
print(dew_point)