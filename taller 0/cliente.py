#!/usr/bin/python
# -*- coding: utf-8 -*-

# Programa Cliente
# www.pythondiario.com

import socket
import sys

# Creando un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta el socket en el puerto cuando el servidor esté escuchando
server_address = ("192.168.8.246", 5500)


sock.connect(server_address)
while True:
    print >>sys.stderr, 'conectando a %s puerto %s' % server_address


    try:
        # Enviando datos
        message = str(raw_input('escriba mensaje '))
        print >>sys.stderr, 'enviando "%s"' % message
        sock.sendall(message)

        data = sock.recv(19)
        print "recibido -> ", data


    finally:
        print 'Reiniciando'

print >>sys.stderr, 'cerrando socket'
sock.close()
