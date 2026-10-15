"""
air_compressor.py

Program works, short button push (less than 2 seconds) turns on relay
and starts a timer, long press (2 seconds or more) turns off timer.
10/07/23
Added log and keyboard interupt, untested. 11/27/23
"""
import time
import sys
from gpiozero import Button, LED


def long_press():
    print("Button was long pressed.")
    log = open('/home/pi/automation/basement_log.txt', 'a+')
    log.write('{0},{1},Long press detected.\r\n'.
              format(time.strftime('%m/%d/%y'), time.strftime('%H:%M')))
    log.close()
    global timer
    timer = 0


def short_press():
    print("Button was short pressed.")
    log = open('/home/pi/automation/basement_log.txt', 'a+')
    log.write('{0},{1},Short press detected.\r\n'.
              format(time.strftime('%m/%d/%y'), time.strftime('%H:%M')))
    log.close()
    global timer
    m = 30      # minutes for the timer
    timer = m * 60


def button_pressed():
    global tstamp1
    tstamp1 = time.time()


def button_released():
    global tstamp1
    global tstamp2
    tstamp2 = time.time()

    td = tstamp2 - tstamp1

    if td >= long_press_time:
        long_press()
    else:
        short_press()


def status(relay_status, timer):
    if relay_status:
        print("The air compressor is currently on and the timer "
              "is at: ", str(timer), " minutes.")
    else:
        print("The air compressor is currently off.")


tstamp1 = time.time()
tstamp2 = time.time()
button_pin = 4
button = Button(button_pin, bounce_time=0.05)
long_press_time = 2
relay_pin = 17      # pin for the relay
relay = LED(relay_pin)
relay.off()
timer = 0
relay_status = False


def main():
    global relay_status

    while True:
        button.when_pressed = button_pressed
        button.when_released = button_released
        if timer > 0:
            relay.on()
            relay_status = True
            log = open('/home/pi/automation/basement_log.txt', 'a+')
            log.write('{0},{1},Relay turned on.\r\n'.format
                      (time.strftime('%m/%d/%y'), time.strftime('%H:%M')))
            log.close()
        else:
            relay.off()
            relay_status = False
            log = open('/home/pi/automation/basement_log.txt', 'a+')
            log.write('{0},{1},Relay turned off.\r\n'.format
                      (time.strftime('%m/%d/%y'), time.strftime('%H:%M')))
            log.close()

        try:
            stdin = sys.stdin.read()
            if "status" in stdin:
                status(relay_status, timer)
        except:
            pass


if __name__ == '__main__':
    main()
