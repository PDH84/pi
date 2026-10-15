"""
Temperature_Logger_V0.1.py
Logs temperature and humidity every five minutes to a txt file.
Added ability to check current status (untested).
Added ability to create copy of current log file while program running (untested).
12/04/23
"""
import os
import time
import Adafruit_DHT
import sys
import fcntl
import shutil

DHT_SENSOR_1 = Adafruit_DHT.DHT22  # indoor temp sensor
DHT_1_PIN = 22  # pin 15
DHT_SENSOR_2 = Adafruit_DHT.DHT22  # outdoor temp sensor
DHT_2_PIN = 24  # pin 18
sleep_counter = 300
fl = fcntl.fcntl(sys.stdin.fileno(), fcntl.F_GETFL)
fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, fl | os.O_NONBLOCK)

print('Temperature_Logger_V0.1 is running, started on {0}_{1}'.
        format(time.strftime('%m%d%y'), time.strftime('%H:%M')))
print('Enter "stop" to end program.')
print('Enter "status" to see current status.')

file_name = 'Temperature_log_{0}'.format(time.strftime('%m%d%y'))

while True:

#    creates a new file for each day
#    file_name = '{0}'.format(time.strftime('%m%d%y'))    

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
        if type(humidity_1) == float:
            pass
        else:
            humidity_1 = -89.9
        if type(temperature_1) == float:
            temperature_1 = (temperature_1 * 1.8) + 32
        else:
            temperature_1 = -89.9
        if type(humidity_2) == float:
            pass
        else:
            humidity_2 = -89.9
        if type(temperature_2) == float:
            temperature_2 = (temperature_2 * 1.8) + 32
        else:
            temperature_2 = -89.9
    
        file.write('{0},{1:0.1f},{2:0.1f},{3:0.1f},{4:0.1f}\r\n'.
                   format(time.strftime('%m/%d/%y %H:%M'),
                       temperature_1, humidity_1, temperature_2, humidity_2))

        file.close()

    sleep_counter += 1
    try:
        stdin = sys.stdin.read()
        if "stop" in stdin:
            break
    except:
        pass

    try:
        stdin = sys.stdin.read()
        if "status" in stdin:
            print('Temperature_Logger_V0.1 is running, started on {0}_{1}'.
                   format(time.strftime('%m%d%y'), time.strftime('%H:%M')))
            print('Indoor temperature and humidity: {0}, {1}'.
                   format(temperature_1, humidity_1))
            print('Outdoor temperature and humidity: {0}, {1}'.
                   format(temperature_2, humidity_2))
    except:
        pass

    try:
        stdin = sys.stdin.read()
        if "log" in stdin:
            shutil.copyfile('./{0}'.format(file_name), './{0}_copy'.format(file_name)')
    except:
        pass

    time.sleep(1)
