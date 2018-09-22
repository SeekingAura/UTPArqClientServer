
# RabbitMQ by Pitoval - Tutorial 2 - Work queues
* [Work Queues](https://www.rabbitmq.com/tutorials/tutorial-two-python.html)

Con Rabbitmq cuando envia mensajes debe especificar a que cola del servidor se dbeen de enviar, lo mismo el que se encarga de "Consumir" o recibir esos mensajes debe especificar a que cola debe de tomar, pero no tiene por que ser un solo dispositivo o proceso que este "recibiendo" o atendiendo los mensajes, es decir puede haber mas de uno resolviendo la misma tarea y el rabbitmq se encarga de hacer un balance de cargas dando uso del algoritmo de despacho **Round-robin**.

el codigo de ejemplo *worker-NoACK.py* se encarga de recibir los mensajes pero sin acuse de recibido (ACK), para ver el **Round-robin** en acción se deben de ejecutar 2 o mas instancias
```bash
$ sudo python3 worker-NoACK.py
```

Puede ejecutarse en 1 o mas equipos diferentes al servidor, en como se encuentra configurado funcionará con el usuario **guest** (debe tenerse garantizado acceso o uso del mismo si estamos por medio remoto), en su configuración de "escucha" si el worker recibe un mensaje con el caracter '.' (punto) esa misma cantidad de puntos que contenga el mensaje esperará en segundos para luego poder consumir o recibir un nuevo mensaje (asi se tengan encolados), 

Teniendo presente como se funcionan los mnesajes ejecutaremos el *new_task-NoACK,py* para su ejecución recibe un parametro de cantidad de mensajes que enviará y un segundo parametro que es opcional que es mandar un mensaje especifico, en este caso se ejecutará de la siguiente manera
```bash
sudo python3 new_task-NoACK.py 10
```

Como el parametro opcional está vacio enviará **Hello World! #$numero $npuntos** Donde $numero es el número de mensaje (es el mismo de iteración) y $npuntos son caracteres '.' donde la cantidad de cada vez es el mismo de iteración; ahora bien, una vez ejecutado lo anterior de los worker que se tienen activos se probará "interrumpirlo" o bien cerrar alguno de estos que estaban activos desde el instante de lanzar *new_task-NoACK.py 10* antes de que termien de recibir todos los mensjaes que se enviaron.

Si se hace correctamente se podrá notar que los worker restantes reciben sus mensajes común corriente y los mensajes que le correspondian al que fue interrumpido se "pierden" debido a que no tienen ACK y la queue no es durables

Ahora probemos con una queue que permitir emensjaes durables y el worker de uso del ACK, pra ello primero ejecutamos 2 o mas worker con *worker-WithACK.py* de la siguiente manera
```bash
$ sudo python3 worker-WitchACK.py
```

mientras estan activos los procesos worker ahora ejecutaremos tareas que sean persistentes, es decir que mantengan ahí hasta que termien su protocolo (en este caso el ACK) del archivo *new_task-Persistent.py* asi
```bash
$ sudo new_task-Persistent.py 13
```

De esta forma enviará hasta 13 mensjaes donde cada mensaje tendrá el caracter '.' con el mismo número de iteraciones, recordemos que el worker no temrina de atender el mensaje hasta que pasen tantos puntos tenga como segundos. Mientras los worken están "despachando" los mensajes pruebe cancelando esos procesos worker y observe como los worker restantes terminana de atender los mensajes

Si el ACK no se realiza en el metodo cuando el worker es interrumpido o cancelado su proceso el mensaje será "retomado" por los demas worker es decir el los mensajes o el servicio se vuelve a lanzar

Desde el servidor se puede revisar el estado de las colas, en si con el siguiente comando
```bash
$ sudo sudo rabbitmqctl list_queues name messages_ready messages_unacknowledged
```

Podrá ver todas las queue y los mensajes que **NO** se estan procesando y los mensajes que no se han enviado acuse de recibido asi
```bash
Timeout: 60.0 seconds ...
Listing queues for vhost / ...
hello	0	0
task_queue	0	8
```
El primer número es lo mensajes que estan pendientes a procesar y el segundo número es la cantidad de mensajes que no se le han dado ACK