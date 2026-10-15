# real_feel.py
# Created by Peter Harrison
# When this program is run it prompts the user to rate their comfort on a scale
# of 1 to 5.  1 being cold, 2 comfortably chilly, 3 perfect, 4 comfortably warm,
# 5 too hot.  The program then reads the current temperature and humidity from an
# attached sensor.  It then logs the date, time, temperature, humidity, calculated
# dew point, and subjective comfort level.
#
# Eventually this data will be used to map a comfort range to be displayed by a
# color on a LED.
#
# A further addition to make is to also prompt the user of the comfort level outside,
# possible with the 0 option for haven't been outside, and to then use a webcrawler
# (or attached external sensor) to record that data as well.
#
#
# To-do:
# 1) Copy current program to this file, adjust for 1-5 comfort range.
# 2) Work on a separate LED program.
# 3) Work on a data cruncher program for the LED color ranges.
# 4) Figure out a webcrawler weather/temp grabbing program.
# 5) Figure out github sync.



'''
# code taken from duckduckgoAI
import requests
from bs4 import BeautifulSoup

city = "Woodstown"
url = f"https://www.google.com/search?q=weather+{city}"
html = requests.get(url).content
soup = BeautifulSoup(html, 'html.parser')

# Extract temperature
temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
# Extract time and sky description
str_ = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
data = str_.split('\n')
time = data[0]
sky = data[1]

print(f"Temperature: {temp}")
print(f"Time: {time}")
print(f"Sky: {sky}")
'''