#!/usr/bin/python3

import socketserver
import time


class TCPConnectionHandler(socketserver.BaseRequestHandler):
    """
    Una instancia por cada conexión, las acciones se personalizan en el
    manejador de la clase, la función **handle(self)**
    """

    global anemometer

    def handle(self):
        self.event = threading.Event()

        anemometer = self.anemometer
        anemometer.events.append(self.event)

        while 1:
            self.event.wait()
            self.event.clear()
            try:
                self.request.sendall('{"windspeed": %f, "time": "%s"}' % (
                    anemometer.wind_speed,
                    time.strftime('%X %x %Z')
                ))
            except:
                break
        anemometer.events.remove(self.event)