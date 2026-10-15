from gpiozero import RGBLED
import time

r_pin = 13
g_pin = 19
b_pin = 26

led = RGBLED(r_pin, g_pin, b_pin)

r_start = 1.0
g_start = 0.0
b_start = 0.0

r_end = 0.0
g_end = 1.0
b_end = 0.0

rate = 1
rate_division = rate / 100
i = 0

led.color = (r_start, g_start, b_start)

while i < 100:
    i += 1
    if r_start >= r_end:
        r = r_start - (abs(r_start - r_end) * (i / 100))
    else:
        r = r_start + (abs(r_start - r_end) * (i / 100))
    if g_start >= g_end:
        g = g_start - (abs(g_start - g_end) * (i / 100))
    else:
        g = g_start + (abs(g_start - g_end) * (i / 100))
    if b_start >= b_end:
        b = b_start - (abs(b_start - b_end) * (i / 100))
    else:
        b = b_start + (abs(b_start - b_end) * (i / 100))
    led.color = (r, g, b)
    time.sleep(rate_division)

led.color = (r_end, g_end, b_end)
