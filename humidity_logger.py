import os
import time
import Adafruit_DHT

DHT_SENSOR_1 = Adafruit_DHT.DHT22    # thermostat sensor
DHT_SENSOR_2 = Adafruit_DHT.DHT22    # desk sensor
DHT_SENSOR_3 = Adafruit_DHT.DHT22    # middle room sensor
DHT_SENSOR_4 = Adafruit_DHT.DHT22    # outdoor sensor
# DHT_SENSOR_5 = Adafruit_DHT.DHT22
DHT_1_PIN = 4     # pin 7
DHT_2_PIN = 17    # pin 11
DHT_3_PIN = 27    # pin 13
DHT_4_PIN = 22    # pin 15
# DHT_5_PIN =

try:
    file = open('/home/pi/humidity.csv', 'a+')
    if os.stat('/home/pi/humidity.csv').st_size == 0:
        file.write('Date,Time,Thermostat Temperature, Thermostat Humidity, Desk Temperature, Desk Humidity,'
                   'Middle Temperature, Middle Humidity, Outdoor Temperature, Outdoor Humidity\r\n')
except:
    pass

while True:
    humidity_1, temperature_1 = Adafruit_DHT.read_retry(DHT_SENSOR_1, DHT_1_PIN)
    humidity_2, temperature_2 = Adafruit_DHT.read_retry(DHT_SENSOR_2, DHT_2_PIN)
    humidity_3, temperature_3 = Adafruit_DHT.read_retry(DHT_SENSOR_2, DHT_2_PIN)
    humidity_4, temperature_4 = Adafruit_DHT.read_retry(DHT_SENSOR_2, DHT_2_PIN)

    if humidity_1 is not None and temperature_1 is not None:
        file.write('{0},{1},{2:0.1f}*C,{3:0.1f}%,{4:0.1f}*C,{5:0.1f}%'
                   ',{6:0.1f}*C,{7:0.1f}%,{8:0.1f}*C,{9:0.1f}%\r\n'.
                   format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'),
                          temperature_1, humidity_1, temperature_2, humidity_2,
                          temperature_3, humidity_3, temperature_4, humidity_4))
    else:
        print("Failed to retrieve data from humidity sensor")

    time.sleep(300)
