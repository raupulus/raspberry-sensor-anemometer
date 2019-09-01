#!/usr/bin/python3

from _thread import start_new_thread
import time

from Anemometer import Anemometer

anemometer = Anemometer()


def threadeval ():
    while 1:
        anemometer.wind_speed = anemometer.imp_to_meters_second()
        print("Velocidad actual: %f m/s" % anemometer.wind_speed)

        anemometer.imp_per_sec = 0

        for x in anemometer.events:
            x.set()
        time.sleep(1)


start_new_thread(threadeval, ())