"""
Automated_message_V2.py
written by Peter Harrison
9/15/26

Reads outdoor weather temp and sends a network test message.
"""

import asyncio
from meshcore import MeshCore, EventType
import pandas as pd
import board
import adafruit_bme680

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

def readBME680(temp_units, pressure_units):
    # read BME680 sensor
    i2c = board.I2C()  # must use board.SCL (pin5) and board.SDA (pin3)
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
    bme680.sea_level_pressure = 1017.74804

    try:
        out_temp = convert_units(bme680.temperature, temp_units)
        out_pressure = convert_units(bme680.pressure, pressure_units)
        out_humidity = round(bme680.relative_humidity, 1)

    except ValueError:
        out_temp = 0.0
        out_pressure = 0.0

    return out_temp, out_humidity, out_pressure

def read_file(filename):
    weather_df = pd.read_csv(filename)

    return weather_df

def get_trends(weather_df):
    current_pressure = weather_df.iloc[-1,6]
    past_pressure_24_hr = weather_df.iloc[-96, 6]
    daily_trend = round((current_pressure - past_pressure_24_hr), 1)

    return daily_trend

filename = "weather_data.txt"
temp_units = 'imperial'   # imperial and metric available currently
pressure_units = 'hPa'    # hPa and inHg available currently
out_temp, out_humidity, out_pressure = readBME680(temp_units, pressure_units)
daily_trend = get_trends(read_file(filename))
automated_message = "This is an automated network test.\n\nTemperature= {0:0.1f}ºF\nHumidity= {1:0.1f}%\nPressure= {2:0.1f}hPa\nPressure trend= {3:0.1f}".format(
            out_temp, out_humidity, out_pressure, daily_trend)

async def send_channel_message():
    # Connect to the MeshCore device via serial
    meshcore = await MeshCore.create_serial("/dev/ttyACM0")

    try:
        # Send message to channel index 0 (Public Channel)
        result = await meshcore.commands.send_chan_msg(
            chan=1,
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
