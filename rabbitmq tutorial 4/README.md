# RabbitMQ by Pitoval - Tutorial 4 - Routing
* [Routing](https://www.rabbitmq.com/tutorials/tutorial-four-python.html)

A **producer** is a user application that sends messages.
A **queue** is a buffer that stores messages.
A **consumer** is a user application that receives messages.


En los ejemplos anteriores no se estaba dando uso de exchange, el exchange es el espacio ideal o adecuado para almacenar los logs, este es un canal que se ecnarga de escribir en el momento como tal. En el canal de intercambio a diferencia de las queue hace que todos los que estan en conectados a este recibna el mismo mensaje