#!/usr/bin/python3

import socketserver
import sys
import threading
from _thread import start_new_thread
import time

from Anemometer import Anemometer

anemometer = Anemometer()


def threadeval ():
    print('Entra')
    while 1:
        anemometer.wind_speed = anemometer.imp_to_meters_second()
        print("Velocidad actual: %f m/s" % anemometer.wind_speed)

        anemometer.imp_per_sec = 0

        for x in anemometer.events:
            x.set()
        time.sleep(1)


start_new_thread(threadeval, ())



HOST = ''
PORT = 2400

############################################################################
'''  One instance per connection.
     Override handle(self) to customize action. '''

class TCPConnectionHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.event = threading.Event()
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

############################################################################

class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(\
        self,\
        server_address,\
        RequestHandlerClass)

############################################################################

if __name__ == "__main__":
    server = Server((HOST, PORT), TCPConnectionHandler)
    # terminate with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
