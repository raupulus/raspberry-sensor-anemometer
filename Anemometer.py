#!/usr/bin/python3
import time

import RPi.GPIO as GPIO
import math
import time


class Anemometer():
    """
    Esta clase representa un sensor que envía pulsos digitales a un pin GPIO
    conociendo de esta forma las vueltas completas que realiza.

    Mediante el método generateWind() se actualizarán los valores de la clase
    calculando y limpiándolos.
    De esta forma queda el modelo para el anemómetro separado de las peticiones
    en tiempo pudiendo pedirse cada una en intervalos distintos se calculará
    siempre la direncia de tiempo dinámicamente.

    La clase quedará siempre tomando datos y se podrán calcular en cualquier
    momento usando para ello los datos recopilados desde la última vez.
    """

    ## Cantidad de pulsos (cierres de circuito) que tiene por vuelta completa.
    pulsos_por_vuelta = 2

    ## Pin sobre el que se toman las lecturas/pulsos digitales.
    PIN = 7

    ## Radio del anemómetro en centímetros.
    RADIO = 9

    ## Pulsos obtenidos en el periodo de tiempo.
    pulsos = 0

    ## Los pulsos totales en el tiempo completo de ejecución.
    pulsos_totales = 0

    ## Velocidad actual de la velocidad del viento en metros por segundos.
    wind_speed = 0

    ## Suma de todas las velocidades (para sacar media con pulsos_totales)
    wind_speed_total = 0

    ## Recuento de todas las veces que se ha calculado los datos.
    wind_recount = 0

    ## Velocidad máxima.
    wind_max = 0

    ## Velocidad mínima.
    wind_min = 0

    ## Velocidad media.
    wind_average = 0

    ## Valores anteriores registrados.
    old_pulsos = 0
    old_wind_max = 0
    old_wind_min = 0
    old_wind_average = 0
    old_s_time = time.time()
    old_time_diff = 0

    ## Contador de tiempo entre cálculos.
    s_time = time.time()
    time_diff = 0  ## Diferencia de tiempo entre comprobaciones

    def __init__(self, pin=7, RADIO = 9, pulsos_vuelta=2):
        self.PIN = pin
        self.RADIO = RADIO
        self.pulsos_por_vuelta = pulsos_vuelta
        self.connect()

    def connect(self):
        """
        Inicializa la conexión con el sensor escuchando pulsos y asignando
        eventos para detectarlos.
        """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.PIN, GPIO.RISING, callback=self.sumar_pulso,
                              bouncetime=5)

    def disconnect(self):
        """
        Para la conexión con el sensor.
        """
        pass

    def sumar_pulso(self, pin):
        """
        Aumenta el contador de pulsos recibidos por el anemómetro.
        """
        self.pulsos += 1

    def pulsos_to_meters_second(self):
        """
        Convierte pulsos en metros por segundo
        velocidad = distancia / tiempo
        velocidad = (vueltas * circunferencia) / tiempo
        velocidad = ((pulsos / pulsos por vuelta) * (2 * pi * radio)) / tiempo

        :return: m/s
        """

        ## Parámetros base
        pulsos = int(self.pulsos)
        pulsos_por_vuelta = int(self.pulsos_por_vuelta)
        radio = float(self.RADIO)

        ## Cálculo de tiempo desde que inició el contador de pulsos
        time_now = time.time()
        time_diff = time_now - self.s_time

        ## Parámetros calculados
        vueltas = (pulsos / pulsos_por_vuelta)
        circunferencia = 2 * math.pi * (radio / 10)
        velocidad = (circunferencia * vueltas) / time_diff

        ## Reseteo pulsos
        self.old_pulsos = pulsos
        self.pulsos_totales += self.pulsos
        self.pulsos = 0
        self.old_time_diff = self.time_diff
        self.time_diff = time_diff
        self.old_s_time = self.s_time
        self.s_time = time.time()

        return velocidad

    def generate_wind(self):
        """
        Genera los valores para el viento actual, máximo, mínimo y media.
        """

        ## Aumento el contador, será reseteado al llamar a get_all_datas().
        self.wind_recount += 1

        ## Valores anteriores registrados.
        self.old_wind_max = self.wind_max
        self.old_wind_min = self.wind_min
        self.old_wind_average = self.wind_average

        ## Velocidad actual de la velocidad del viento en metros por segundos.
        self.wind_speed = self.pulsos_to_meters_second()

        ## Velocidad máxima.
        if self.wind_speed > self.wind_max:
            self.wind_max = self.wind_speed

        ## Velocidad mínima.
        if (self.wind_min == 0) or (self.wind_speed < self.wind_min):
            self.wind_min = self.wind_speed

        ## Velocidad media.
        self.wind_speed_total += self.wind_speed
        if self.pulsos_totales > 0:
            self.wind_average = self.wind_speed_total / self.wind_recount
        else:
            self.wind_average = 0

    def get_all_datas(self):
        """
        Devuelve todos los datos del modelo para el último periodo de medición.
        """

        ## Almaceno todos los datos a devolver.
        data =  {
            'wind_speed': self.wind_speed,
            'wind_average': self.wind_average,
            'wind_min': self.wind_min,
            'wind_max': self.wind_max,
        }

        ## Limpio los datos del modelo.
        pulsos = 0
        pulsos_totales = 0
        wind_speed = 0
        wind_speed_total = 0
        wind_max = 0
        wind_min = 0
        wind_average = 0
        s_time = time.time()
        time_diff = 0

        ## Devuelvo los datos.
        return data

    def start_read(self):
        """
        Comienza la lectura de datos cada un periodo de tiempo para hacer los
        cálculos de los eventos en GPIO recibidos durante ese tiempo.
        Este hilo queda abierto para que al consultar al modelo haya permanecido
        constantemente almacenando datos y sea inmediata su devolución sin
        necesitar realizar los cálculos en ese momento.
        """
        pass

    def stop_read(self):
        """
        Para la lectura de datos y cierra el hilo de trabajo con el anemómetro.
        """
        pass

    def tablemodel(self):
        """
        Plantea campos como modelo de datos para una base de datos y poder ser
        tomados desde el exterior.
        """
        pass

anemometer = Anemometer()

while True:
    ## Genero estadíasticas
    anemometer.generate_wind()

    print('Pulsos Totales:', anemometer.pulsos_totales)
    print('Pulsos en esta medición:', anemometer.old_pulsos)
    print('Tiempo recopilando pulsos:', anemometer.old_time_diff)
    print('Metros por segundos:', anemometer.wind_speed)
    print('Media de todas las capturas:', anemometer.wind_average)
    print('Viento mínimo:', anemometer.wind_min)
    print('Viento máximo:', anemometer.wind_max)
    time.sleep(5)