from gpiozero import RGBLED
from colorzero import Color
import math
import time

r_pin = 13
g_pin = 19
b_pin = 26

rgb_led = RGBLED(r_pin, g_pin, b_pin)

i = 0

while i < 361:
    rad = math.radians(i)
    a = (math.sin(rad) + 1) / 2      # for some reason 128 will bump output to 256 when sin = 1, check that
    rgb_led.color = (a, 0, 0)
    i += 1
    time.sleep(0.05)
