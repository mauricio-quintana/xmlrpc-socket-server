from xmlrpc_redes import Server
import time
import sys
import threading

def test_server1():

    host = "100.100.0.2"
    #host = "localhost"
    port = 80

    def mayusculas(s):
        return s.upper()
    
    def contar_vocales(s):
        time.sleep(10)
        cant = 0
        for t in s.lower():
            if t in "aeiou":
                cant = cant + 1
        return cant
    
    def division(a, b):
        return a / b
    
    def saludar():
        return "HOLA"
    
    def mayor_a_5(a,b):
        if(b>5):
            return a.upper()
        else:
            return a.lower()
    
    server = Server(host,port)
    server.add_method(mayusculas)
    server.add_method(contar_vocales)
    server.add_method(division)
    server.add_method(saludar)
    server.add_method(mayor_a_5)
    
    server.serve()

test_server1()