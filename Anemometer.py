#!/usr/bin/python3

from thread import start_new_thread
import RPi.GPIO as GPIO
import math
import time

class AnemometerServer():
    # RPi.GPIO Layout verwenden (wie Pin-Nummern)
    GPIO.setmode(GPIO.BOARD)

    PIN = 7

    imp_per_sec = 0

    ## Velocidad actual de la velocidad del viento en metros por segundos.
    wind_speed = 0

    def __init__(self, pin=7,):
        self.PIN = pin

    def connect(self):
        """
        Inicializa la conexión con el sensor.
        """
        GPIO.setup(self.PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.PIN, GPIO.RISING, callback=interrupt,
                              bouncetime=5)

    def disconnect(self):
        """
        Para la conexión con el sensor.
        """
        pass

    def addImp(self):
        """
        Aumenta imp por segundo.
        """
        self.imp_per_sec += 1

    def imp_to_meters_second(self):
        """
        Convierte imp to m/s
        :return: m/s
        """

        val = self.imp_per_sec
        # y = 8E-09x5 - 2E-06x4 + 0,0002x3 - 0,0073x2 + 0,4503x + 0,11

        calc = float("8e-9") * math.pow(val, 5) - float("2e-6") * \
            math.pow(val, 4) + float("2e-4") * math.pow(val, 3) - float("7.3e-3") * \
            math.pow(val, 2) + 0.4503 * val + 0.11

        if calc < 0.2:
            calc = 0

        return calc

    def threadeval(self):

        while 1:
            self.wind_speed = self.imp_to_meters_second()
            print("Velocidad actual: %f m/s" % self.wind_speed)

            self.imp_per_sec = 0

            for x in self.events:
                x.set()
            time.sleep(1)

    start_new_thread(threadeval, ())
