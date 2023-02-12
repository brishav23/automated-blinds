#! /usr/bin/python

import RPi.GPIO
import urllib.request
import json
import os
import datetime
import time

res = urllib.request.urlopen(f'http://api.weatherapi.com/v1/forecast.json?key={os.environ.get("API_KEY")}&q={os.environ.get("ZIP")}')
data = json.loads(res.read().decode("utf-8"))

#print(json.dumps(data, indent=2))
#print(json.dumps(data["forecast"]["forecastday"][0]["astro"], indent=2))

sunrise = data["forecast"]["forecastday"][0]["astro"]["sunrise"]
sunset = data["forecast"]["forecastday"][0]["astro"]["sunset"]

print(f"Sunrise: {sunrise}")
print(f"Sunset: {sunset}")
