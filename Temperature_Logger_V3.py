'''
Reads indoor and outdoor conditions and writes it to a file.

Added API weather grabber for outdoor temp and humidity.

'''


import adafruit_dht
import board
import time
import os
import requests

def get_weather_data(city_name, api_key):
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
    else:
        print("Error: API request failed.")
    
    return outdoor_temp, outdoor_humidity

def write_file(filename, temperature_f, humidity, out_temp, out_humidity):
    file = open(filename, 'a')
    # save time, date, temperature, and humidity in .txt file
    file.write(time.strftime('%H:%M:%S %d/%m/%Y') + ', {:.2f}, {:.2f}, {:.2f}, {:.2f}\n'.format(temperature_f, humidity, out_temp, out_humidity))
    file.close()
    
    pass

# Sensor data pin is connected to GPIO 4
sensor = adafruit_dht.DHT22(board.D4)
filename = 'hourly_sensor_reading.txt'

# for API weather grabber
api_key = "870fac250dfc0e6d0519f57b39b1ca81"
city = "Woodstown"

# Check if the file exists before opening it in 'a' mode (append mode)
file_exists = os.path.isfile(filename)

# Write the header to the file if the file does not exist
if not file_exists:
    file = open(filename, 'w')
    file.write('Time and Date, Indoor temperature (ºF), Indoor humidity (%), Outdoor temperature (ºF), Outdoor humidity (%)\n')
    file.close()
    
try:
    # read the humidity and temperature
    temperature_c = sensor.temperature
    temperature_f = temperature_c * (9 / 5) + 32
    humidity = sensor.humidity
       
    sensor.exit()

    out_temp, out_humidity = get_weather_data(city, api_key)

    #print readings on the shell
    print("Inside temp={1:0.1f}ºF, Inside humidity={2:0.1f}%, Outside temp={3:0.1f}ºF, Outside humidity={4:0.1f}%".format(temperature_c, temperature_f, humidity, out_temp, out_humidity))

    write_file(filename, temperature_f, humidity, out_temp, out_humidity)
        
except RuntimeError as error:
    # Errors happen fairly often, DHT's are hard to read, just keep going
    print(error.args[0])
    time.sleep(2.0)

except KeyboardInterrupt:
    print('Program stopped')
    file.close()

except Exception as e:
    print('An unexpected error occurred:', str(e))
    file.close()
    sensor.exit()

