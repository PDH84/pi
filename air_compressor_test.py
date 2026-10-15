'''
New program to turn on and off the basement air compressor remotely.

Based on old arduino code but stolen mostly from the internet.

Work on way to output to another program to update status.
'''

from gpiozero import Button
import gpiozero
from time import time, sleep


relay_pin = 12
relay = gpiozero.OutputDevice(relay_pin, active_high=False, initial_value=False )
# input channel button
button = Button(26, bounce_time=0.1)
running = False
# time in seconds that relay will remain on
timer = 600
end_time = 0

def start_timer():
    global running, end_time
    running = True
    end_time = time() + timer
    #relay.on()
    print("Relay on.")

def check_timer():
    global running
    if running:
        if time() >= end_time:
#            relay.off()
            running = False
            print("Timer finished")

button.when_pressed = start_timer

while True:
    check_timer()
    sleep(0.1)