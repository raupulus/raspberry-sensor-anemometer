#!/usr/bin/python3

import RPi.GPIO as GPIO
import math

class Anemometer():
    PIN = 7

    events = []

    imp_per_sec = 0

    ## Velocidad actual de la velocidad del viento en metros por segundos.
    wind_speed = 0

    ## Velocidad máxima.
    wind_max = 0

    ## Velocidad mínima.
    wind_min = 0

    ## Velocidad media.
    wind_average = 0

    ## Valores anteriores registrados
    old_wind_max = 0
    old_wind_min = 0
    old_wind_average = 0


    def __init__(self, pin=7,):
        self.PIN = pin

        self.connect()

    def connect(self):
        """
        Inicializa la conexión con el sensor.
        """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.PIN, GPIO.RISING, callback=self.addImp,
                              bouncetime=5)

    def disconnect(self):
        """
        Para la conexión con el sensor.
        """
        pass

    def addImp(self, val):
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


