# Taller 5 - Implementación de un servicio de calcudora usando SOPA con la libreria zeep
* [Routing](https://www.rabbitmq.com/tutorials/tutorial-six-python.html)

A **producer** is a user application that sends messages.
A **queue** is a buffer that stores messages.
A **consumer** is a user application that receives messages.


Los topis solo pueden tener un maximo de 255 bytes

Recibir de TODO
python receive_logs_topic.py "#"

Recibir todo lo que empiuece con valor. y luego cualquier cosa
python receive_logs_topic.py "valor.*"

Enviar solo a los que sean prueba
python emit_log_topic.py "prueba" "A critical kernel error"