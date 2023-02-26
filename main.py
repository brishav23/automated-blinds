#! /usr/bin/python

import RPi.GPIO
import urllib.request
import json
import os
import datetime
import time
import socket
import sys
import signal

child_pid = os.fork()

if (child_pid == 0):
    # child process

    # Set up signal handler
    def sig_handler(num, frame):
        print("Got the signal")
    signal.signal(signal.SIGUSR1, sig_handler)

    cur_time = datetime.date.today()
    res = urllib.request.urlopen(f'http://api.weatherapi.com/v1/forecast.json?key={os.environ.get("API_KEY")}&q={os.environ.get("ZIP")}')
    data = json.loads(res.read().decode("utf-8"))

    sunrise = data["forecast"]["forecastday"][0]["astro"]["sunrise"]
    sunset = data["forecast"]["forecastday"][0]["astro"]["sunset"]

    print(cur_time)
    print(f"Sunrise: {sunrise}")
    print(f"Sunset: {sunset}")
    while True:
        if datetime.date.today() != cur_time:
            cur_time = datetime.date.today()
            res = urllib.request.urlopen(f'http://api.weatherapi.com/v1/forecast.json?key={os.environ.get("API_KEY")}&q={os.environ.get("ZIP")}')
            data = json.loads(res.read().decode("utf-8"))

            sunrise = data["forecast"]["forecastday"][0]["astro"]["sunrise"]
            sunset = data["forecast"]["forecastday"][0]["astro"]["sunset"]

            print(cur_time)
            print(f"Sunrise: {sunrise}")
            print(f"Sunset: {sunset}")
        time.sleep(30)
else:
    # parent process, runs the server to handle user requests and
    # sends signals to child to handle user requests

    # Set up signal handler to clean up child process
    def int_handler(num, frame):
        os.kill(child_pid, signal.SIGKILL)
        os.waitpid(child_pid, 0)
        sys.exit(0)
    signal.signal(signal.SIGINT, int_handler)

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("127.0.0.1", 17590))
    while True:
        msg, addr = server.recvfrom(1024)
        if (msg.decode("utf-8") == "994124175901223"):
            os.kill(child_pid, signal.SIGUSR1)
