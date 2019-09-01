#!/usr/bin/python3

import socketserver

class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # Ctrl-C Limpia todos los hilos creados
    daemon_threads = True

    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address,
                                        RequestHandlerClass)
