"""
NEED TO CHANGE SO DATE IS ONLY THING IN FIRST COLUMN AND TIME IS IN SECOND COLUMN


To do: round air quality to an int
hPa to two decimal places
round everything else to one decimal place

error trap sensor reading
pressure tracking
meshcore output
"""

# import asyncio
# from meshcore import MeshCore, EventType
import adafruit_dht
import adafruit_bme680
import board
import time
import os
import requests
import pandas as pd


def weather_web_scraper(city_name, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "imperial"  # Use "imperial" or "metric"
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        outdoor_temp = data['main']['temp']
        outdoor_humidity = data['main']['humidity']
        description = data['weather'][0]['description']

        return outdoor_temp, outdoor_humidity

    else:
        print("Error: API request failed.")
        outdoor_temp = 0.0
        outdoor_humidity = 0.0

        return outdoor_temp, outdoor_humidity


def write_file(filename, in_temp_f, in_humidity, out_temp_f, out_humidity, out_pressure_inhg, out_aq, web_temp, web_humidity):
    file = open(filename, 'a')
    # save time, date, temperature, and humidity in .txt file
    file.write(time.strftime('%m/%d/%Y') + ', ' + time.strftime('%H:%M:%S') + ', {:.1f}, {:.1f}, {:.1f}, {:.1f}, {:.1f}, {:.0f}, {:.1f}, {:.1f}\n'.format(
        in_temp_f, in_humidity, out_temp_f, out_humidity, out_pressure_inhg, out_aq, web_temp, web_humidity))
    file.close()

    pass

'''
def get_trends(filename, row_index, col_index):
    df = pd.read_csv(filename)
    row_index = 0 - row_index
    value = df.iloc[row_index][col_index]
    return value
'''

# If using DHT22 sensor data pin is connected to GPIO 4
sensor = adafruit_dht.DHT22(board.D4)

# If using BME680 sensor
# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()   # uses board.SCL (pin5) and board.SDA (pin3)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
# change this to match the location's pressure (hPa) at sea level
# average is 1013.25, used online calculator for current value
bme680.sea_level_pressure = 1017.74804

filename = 'weather_data.txt'

# for API weather scraper
api_key = "870fac250dfc0e6d0519f57b39b1ca81"
city = "Woodstown"

# Check if the file exists before opening it in 'a' mode (append mode)
# Write the header to the file if the file does not exist
file_exists = os.path.isfile(filename)

if not file_exists:
    file = open(filename, 'w')
    file.write(
        'Date, Time, Indoor temperature (ºF), Indoor humidity (%), Outdoor temperature (ºF), Outdoor humidity (%), Pressure (hPa), Air quality (ohms), Web temperature (ºF), Web humidity (%)\n')
    file.close()

# Doesn't work yet0
# last_hour_pressure = get_trends(filename, 4, 6)

try:
    # reads the humidity and temperature from DHT22 sensor
    in_temp_c = sensor.temperature
    in_temp_f = in_temp_c * (9 / 5) + 32
    in_humidity = sensor.humidity

    sensor.exit()

except ValueError:
    in_temp_f = 0.0
    in_humidity = 0.0
    print("Indoor sensor error.")
    sensor.exit()

try:
    # Pulls readings from BME680, does conversions
    out_temp_c = bme680.temperature
    out_pressure_hpa = bme680.pressure
    out_humidity = bme680.relative_humidity
    out_aq = bme680.gas
    out_temp_f = out_temp_c * (9 / 5) + 32
    # convert hPa to inHg
    # out_pressure_inhg = out_pressure_hpa * 0.02952998

except ValueError:
    out_temp_f = 0.0
    out_pressure_hpa = 0.0
    out_ap = 0.0
    print("Outdoor sensor error.")

# Pulls temp and humidity from web
web_temp, web_humidity = weather_web_scraper(city, api_key)


# Not working yet
# pressure_trend = out_pressure_hpa - last_hour_pressure

# print readings on the shell
print("Inside temp: {:.1f}ºF".format(in_temp_f))
print("Inside humidity: {:.1f}%".format(in_humidity))
print("Reported temp: {:.1f}ºF".format(web_temp))
print("Reported humidity: {:.1f}%".format(web_humidity))
print("Outside temp: {:.1f}ºF".format(out_temp_f))
print("Air quality: {:.0f}%".format(out_aq))
print("Outdoor humidity: {:.1f}%".format(out_humidity))
print("Pressure: %0.0f hPa" % bme680.pressure)
print("Altitude = %0.2f meters" % bme680.altitude)
# print("Pressure tend in past hour: {:.1f}hPa".format(pressure_trend))

write_file(filename, in_temp_f, in_humidity, out_temp_f, out_humidity, out_pressure_hpa, out_aq, web_temp, web_humidity)



"""
Code for sending meshcore message out. Unused currently, possible future use.

automated_message = "Inside temp={1:0.1f}ºF, Inside humidity={2:0.1f}%, Outside temp={3:0.1f}ºF, Outside humidity={4:0.1f}%".format(
            temperature_c, temperature_f, humidity, out_temp, out_humidity)

async def send_channel_message():
    # Connect to the MeshCore device via serial
    meshcore = await MeshCore.create_serial("/dev/ttyUSB0")

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
"""
