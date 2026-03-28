from xmlrpc_redes import Server
import time
import sys
import threading

def test_server1():

    host = "150.150.0.2"
    #host = "localhost"
    port = 8080

    def echo(mensaje):
        return mensaje
    
    def suma(*args):
        return sum(args)
    
    def concat(*args):
        mensaje=""
        for arg in args:
            mensaje += arg
        return mensaje
    
    server = Server(host,port)
    server.add_method(echo)
    server.add_method(suma)
    server.add_method(concat)
    server.serve()
test_server1()