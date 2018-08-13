

#!/usr/bin/python
# -*- coding: utf-8 -*-

# Programa Servidor
# www.pythondiario.com

import socket
import sys
import operator

def get_operator_fn(op):
    return {
        '+' : operator.add,
        '-' : operator.sub,
        '*' : operator.mul,
        '/' : operator.truediv,
        'MOD' : operator.mod,
        '^' : operator.xor,
        }[op]

def eval_binary_expr(op1, operator, op2):
    op1,op2 = int(op1), int(op2)
    return get_operator_fn(operator)(op1, op2)


# Creando el socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlace de socket y puerto
server_address = ("192.168.11.179", 10006)
print >>sys.stderr, 'empezando a levantar %s puerto %s' % server_address
sock.bind(server_address)

# Escuchando conexiones entrantes
sock.listen(10)

while True:
    # Esperando conexion
    print >>sys.stderr, 'Esperando para conectarse'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'concexion desde', client_address

        # Recibe los datos en trozos y reetransmite
        while True:
            data = connection.recv(19)
            op=None
            op1=None
            op2=None
            print "data -> ", data
            try:
                op, op1, op2=str(data).split(",")
                print "operacion", op," op1", op1, "op2", op2
                print "resultado -> ", eval_binary_expr(int(op1), op, int(op2))

                connection.sendall(str(eval_binary_expr(int(op1), op, int(op2))))
            except:
                print("Error")
                connection.sendall("Error")


    finally:
        # Cerrando conexion
        connection.close()
