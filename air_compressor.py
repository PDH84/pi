"""
Kind of a mess, not really sure what I want to do with this yet but some
semi-tested code which may be useful.
"""


from gpiozero import Button, LED
import time
import datetime

relay = LED(23)
air_compressor_pin =    # pin for button
h = 0                   # hours for timer
m = 30                  # minutes for timer
s = 0                   # seconds for timer

def countdown(h, m, s):
    # Calculate the total number of seconds
    total_seconds = h * 3600 + m * 60 + s

    # While loop that checks if total_seconds reaches zero
    # If not zero, decrement total time by one second
    while total_seconds > 0:
        # Timer represents time left on countdown
        timer = datetime.timedelta(seconds=total_seconds)

        # Prints the time left on the timer
        print(timer, end="\r")

        # Delays the program one second
        time.sleep(1)

        # Reduces total time by one second
        total_seconds -= 1



def toggle_relay():
    print("toggling")
    relay.toggle()


button = Button(air_compressor_pin, bounce_time=0.1)
button.when_pressed = toggle_relay

while True:
    print("Busy doing other stuff")
    sleep(2)
