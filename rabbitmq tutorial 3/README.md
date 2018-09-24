# RabbitMQ by Pitoval - Tutorial 3 - Publish/Subscribe
* [Publish/Subscribe](https://www.rabbitmq.com/tutorials/tutorial-three-python.html)




En los ejemplos anteriores no se estaba dando uso de exchange, el exchange es el espacio ideal o adecuado para almacenar los logs, este es un canal que se encarga retransmitir a todos los pertenecientes del canal el mismo mensaje.

En la comunicación es importante diferenciar los diferentes tipos de aplicación
* **Producer:** Parte de la aplicación que envia mensajes
* **Queue:** Es un "buffer" que almacena los mensjaes
* **Consumer:** parte de la aplicación que recibe los mensajes

para este ejemplo el que se ejcuta con *receive_logs.py* son los worker o servicios que dan uso del servidor lo ejecutamos en 2 o mas instnacias
```bash
$ sudo python3 receive_logs.py
```

Hay que asegurar que la dirección indicada sea la del servidor y que el usuario guest se pueda acceder por medio remoto, luego emitiremos log con
```bash
$ sudo python3 emit_log.py
```
Veremos que todas las maquinas o procesos que se tienen activo de receive_logs obtienen el mensaje