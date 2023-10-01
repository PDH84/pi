"""
Generally what I want but need to figure out and clean up the when_pressed
and long_press stuff.
"""
from gpiozero import Button, LED
import time
import datetime


def short_press():
    m = 30    # mins for timer
    total_seconds = m * 60
    return total_seconds

def long_press():
    total_seconds = 0
    return total_seconds

def main():
    relay = LED(23)
    air_compressor_pin =  # pin for button
    total_seconds = 0
    relay.off()
    button = Button(air_compressor_pin, bounce_time=0.1)

    button.when_pressed = short_press()
    button.long_press = long_press()

    while total_seconds > 0:
        if relay is False:
            relay = True
        # Timer represents time left on countdown
        timer = datetime.timedelta(seconds=total_seconds)
        print(timer, end="\r")
        time.sleep(1)
        total_seconds -= 1

    relay = False
    time.sleep(1)

if __name__ == '__main__':
    main()