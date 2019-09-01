#!/usr/bin/python3

import sys
from _thread import start_new_thread
import time

from Anemometer import Anemometer
from TCPConnectionHandler import TCPConnectionHandler
from Server import Server

anemometer = Anemometer()
tcp_connection_handler = TCPConnectionHandler

HOST = ''
PORT = 2400


def threadeval ():
    while 1:
        anemometer.wind_speed = anemometer.imp_to_meters_second()
        print("Velocidad actual: %f m/s" % anemometer.wind_speed)

        anemometer.imp_per_sec = 0

        for x in anemometer.events:
            x.set()
        time.sleep(1)


if __name__ == "__main__":
    ## Crea el hilo
    start_new_thread(threadeval, ())

    ## Instancia el servidor
    server = Server((HOST, PORT), tcp_connection_handler)

    ## Terminar con Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
