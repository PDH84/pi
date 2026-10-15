"""
Temperature_Logger_V0.py

Check the keyboard interrupt, any major changes to that need to also
be made in the air_compressor.py

Logs temperature and humidity every five minutes to a txt file.
11/27/23
"""
import os
import time
import Adafruit_DHT
import sys
import fcntl

DHT_SENSOR_1 = Adafruit_DHT.DHT22  # indoor temp sensor
DHT_1_PIN = 22  # pin 15
DHT_SENSOR_2 = Adafruit_DHT.DHT22  # outdoor temp sensor
DHT_2_PIN =   # add pin 
sleep_counter = 300
fl = fcntl.fcntl(sys.stdin.fileno(), fcntl.F_GETFL)
fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, fl | os.O_NONBLOCK)

while True:
    print("Enter 'stop' to end program.")        # maybe put this outside of while loop

    file_name = '{0}_{1}'.format(time.strftime('%m%d%y'), time.strftime('%H:%M'))

    if sleep_counter == 300:
        sleep_counter = 0
        try:
            humidity_1, temperature_1 = Adafruit_DHT.read_retry(DHT_SENSOR_1, DHT_1_PIN)

        # if error is encountered here values set to -90.0
        # if error in encountered later values set to -89.9
        except:
            humidity_1 = -90.0	
            temperature_1 = -90.0   

        try:
            humidity_2, temperature_2 = Adafruit_DHT.read_retry(DHT_SENSOR_2, DHT_2_PIN)
        except:
            humidity_2 = -90.0
            temperature_2 = -90.0

        file = open('/home/pi/templogger/{0}'.format(file_name), 'a+')

        # another line of error checking, if it's corrected here it'll be -89.9 
        if type(humidity_1)==float:
            pass
        else:
            humidity_1 = -89.9
        if type(temperature_1)==float:
            pass
        else:
            temperature_1 = -89.9
        if type(humidity_2)==float:
            pass
        else:
            humidity_2 = -89.9
        if type(temperature_2)==float:
            pass
        else:
            temperature_2 = -89.9
    
        file.write('{0},{1},{2:0.1f}*C,{3:0.1f}%,{4:0.1f}*C,{5:0.1f}%\r\n'.
                   format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'),
                       temperature_1, humidity_1, temperature_2, humidity_2))

        file.close()

    sleep_counter += 1
    try:
        stdin = sys.stdin.read()
        if "\n" in stdin or "\r" in stdin:
            break
    except:
        pass

    time.sleep(1)
