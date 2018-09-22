
# RabbitMQ by Pitoval - Install
## Windows
Descargar e instalar de la siguiente pagina web el rabbimq-server
* [RabbitMQ by Pitoval - Web](https://www.rabbitmq.com/install-windows.html)
* enlace directo [RabbitMQ by Pitoval - rabbitmq-server-3.7.7.exe](https://dl.bintray.com/rabbitmq/all/rabbitmq-server/3.7.7/rabbitmq-server-3.7.7.exe)

luego de instalado el **rabbitmq-server-3.7.7.exe** se va al directorio donde se instal el **RabbitMQ Server** y se ejecuta en un simbolo de sistema con permisos de administrador *rabbitmq-service.bat remove* para poder indicar donde se va manejar la informacin del control del servidor
```batch
C:\Program Files\RabbitMQ Server\rabbitmq_server-3.7.7\sbin>rabbitmq-service.bat remove
```
La ubicación que se indica en lo anterior es la predeterminada, si se ejecuta correctamente se visualizar

```batch
C:\Program Files\erl10.0.1\erts-10.0.1\bin\erlsrv: Service RabbitMQ removed from system.
```

Esto detendrá el servicio y asi podremos ahora indicar donde se alojará la información del servidor con el comando *set RABBITMQ_BASE=C:\Data\RabbitMQ* en el simbolo de sistema con permisos de administrador

```batch
C:\Program Files\RabbitMQ Server\rabbitmq_server-3.7.7\sbin>set RABBITMQ_BASE=C:\Data\RabbitMQ
```

Establecido el path donde se almacenaran los datos del server podemos instalar el servidor con el comando *rabbitmq-service.bat install* en el simbolo de sistema con permisos de administrador
```batch
C:\Program Files\RabbitMQ Server\rabbitmq_server-3.7.7\sbin>rabbitmq-service.bat install
```

procer a instalarse el servidor en el directorio que se tenga en la variable de entorno **RABBITMQ_BASE**, una vez termine e instalarse el servicio que se detuvo al inicio debe reactivarse con *rabbitmq-service.bat start*
```batch
C:\Program Files\RabbitMQ Server\rabbitmq_server-3.7.7\sbin>rabbitmq-service.bat start
```
--- 
## Ubuntu 14, 16, 18
Primeramente instalamos las dependencias de rabbitmq con el siguiente comando en una terminal
```bash
$ sudo apt-get install rabbitmq-server
```

Nos instalará el erlang y varios requisitos que requiere el rabbit server, ahora procedemos a instalar el servidor, para ello primero se descarga el .deb
```bash
$ sudo wget https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.7.7/rabbitmq-server_3.7.7-1_all.deb
```

este comando descargará el archivo *rabbitmq-server_3.7.7-1_all.deb*, se desempaqueta e instala
```bash
$ sudo dpkg -i rabbitmq-server_3.7.7-1_all.deb
```

Es probable que se genere un error en las depedencias (a pesar de haberlas instalado con rabbitmq-server) como el siguiente
```bash
(Leyendo la base de datos ... 94207 ficheros o directorios instalados actualmente.)
Preparando para desempaquetar rabbitmq-server_3.7.7-1_all.deb ...
 * Stopping message broker rabbitmq-server
   ...done.
Desempaquetando rabbitmq-server (3.7.7-1) sobre (3.2.4-1ubuntu0.1) ...
dpkg: problemas de dependencias impiden la configuración de rabbitmq-server:
 rabbitmq-server depende de erlang-nox (>= 1:19.3) | esl-erlang (>= 1:19.3); sin embargo:
  La versión de 'erlang-nox' en el sistema es 1:16.b.3-dfsg-1ubuntu2.2.
  El paquete 'esl-erlang' no está instalado.
 rabbitmq-server depende de socat; sin embargo:
  El paquete 'socat' no está instalado.

dpkg: error al procesar el paquete rabbitmq-server (--install):
 problemas de dependencias - se deja sin configurar
Procesando disparadores para man-db (2.6.7.1-1ubuntu1) ...
Procesando disparadores para ureadahead (0.100.0-16) ...
Se encontraron errores al procesar:
 rabbitmq-server
```

como se puede ver faltan los paquetes *esl-erlang* y *socat* para solucionarlo se instala el *erlang-solutions*, primero se descarga
```bash
$ sudo wget https://packages.erlang-solutions.com/erlang-solutions_1.0_all.deb
```

luego el archivo que se descarga *erlang-solutions_1.0_all.deb* debe ser desempaquetado y ejecutado
```bash
$ sudo dpkg -i erlang-solutions_1.0_all.deb
```

Al ejecutarlo agregará el repositorio para el erlang, actualizamos la lista de paquetes
```bash
$ sudo apt-get update
```

Instalamos el erlang (con la lista que se tiene ahora)
```bash
$ sudo apt-get install erlang
```

Seguramente suelte un error de las depedencias que requerira instalar
```bash
Leyendo lista de paquetes... Hecho
Creando árbol de dependencias
Leyendo la información de estado... Hecho
Tal vez quiera ejecutar «apt-get -f install» para corregirlo:
Los siguientes paquetes tienen dependencias incumplidas:
 erlang : Depende: erlang-dev
          Depende: erlang-appmon
          Depende: erlang-common-test
          Depende: erlang-debugger
          Depende: erlang-dialyzer
          Depende: erlang-et
          Depende: erlang-ftp pero no va a instalarse
          Depende: erlang-gs
          Depende: erlang-inviso
          Depende: erlang-megaco
          Depende: erlang-observer
          Depende: erlang-pman
          Depende: erlang-reltool
          Depende: erlang-test-server
          Depende: erlang-tftp pero no va a instalarse
          Depende: erlang-toolbar
          Depende: erlang-tv
          Depende: erlang-typer
          Depende: erlang-wx
          Recomienda: erlang-jinterface pero no va a instalarse
          Recomienda: erlang-ic-java pero no va a instalarse
          Recomienda: erlang-mode pero no va a instalarse
          Recomienda: erlang-src pero no va a instalarse
          Recomienda: erlang-examples pero no va a instalarse
 rabbitmq-server : Depende: erlang-nox (>= 1:19.3) pero 1:16.b.3-dfsg-1ubuntu2.2 va a ser instalado o
                            esl-erlang (>= 1:19.3) pero no va a instalarse
                   Depende: socat pero no va a instalarse
E: Dependencias incumplidas. Intente «apt-get -f install» sin paquetes (o especifique una solución).
```

Ejecutamos el comando correspondiente para instalar todas las depedencias
```bash
$ sudo apt-get -f install
```

se instalarán las dependencias y se podrá ahora instalar el servidor 
```bash
$ sudo dpkg -i rabbitmq-server_3.7.7-1_all.deb
```

Con esto ya quedará instlaado el servidor y ahora se puede proceder a configurarlo

---

# Configuración de RabbitMQ by Pitoval
## Archivo de configuración en Ubuntu 14, 16, 18
Con el servidor ya podemos proceder a su configuración, la configuración de rabbitmq se almacena en
*/etc/rabbitmq*, pero es probable que si se trata de acceder no nos permita debido al siguiente error
```bash
-bash: cd: rabbitmq/: Permiso denegado
```
Esta restricción es por "seguridad", sin embargo si queremos tener acceso a este directorio modificamos los permisos
```bash
$ sudo chmod a+rwx /etc/rabbitmq
```

Con permisos totales en este directorio ya se puede acceder, esto solo nos permite manejar de una forma mas "comoda" los archivos de configuración asi como se indica en la [guia oficial](https://www.rabbitmq.com/configure.html), aqui se explicará algunas configuraciones basicas.

## Acceso remoto por TCP

Para configurar una conexión remota por **TCP** se debe indicar por cual dirección, parte o interfaz va a establecer la comunicación del servidor con otros clientes o servidores. Una manera sencilla es indicando esta configuración un archivo con nombre *rabbit.tcp_listeners*, se crea el archivo con lo siguiente

```bash
$ sudo nano /etc/rabbitmq/rabbit.tcp_listeners
```

La ip y puerto por donde se realizará la comunicación se puede indicar de varias formas ya sea
#### Simple
```bash
listeners.tcp.1 = 0.0.0.0:5672
listeners.tcp.2 = :::5672
```

#### Formato clasico
```bash
[
  {rabbit, [
    {tcp_listeners, [{"0.0.0.0", 5672},
                     {"::",      5672}]}
  ]}
].
```

La dirección 0.0.0.0 en IPv4 y la dirección :::: en IPv6 indica que se escuchará por TODAS las direcciones, sin embargo podemos colocar como IP la de una de las interfaces del dispositivo y funcionará.

El puerrto 5672 es el puerto "estandar" que usa Rabbitmq para sus conecciones, luego de crear este archivo con su contenido el servicio debe reiniciarse (para asegurar que la configuración quede aplicada)
```bash
$ sudo service rabbitmq-server reload
```
con esto tendremos listo el puerto de escucha, ahora bien muchas de las funciones de rabbit requiere de una autenticación para varias de sus funciones (entre esas el codigo ejemplo de [send.py](/rabbitmq/send.py) y [receive.py](/rabbitmq/receive.py))


### Manejo de usuarios de Rabbitmq
Rabbitmq maneja sus propios usuarios para el uso del servicio, lo cual para ciertas circunstancia será necesario crearlos, modificarlos, eliminarlos, no olvidar que exite la [guia oficial](https://www.rabbitmq.com/rabbitmqctl.8.html) de manejo de usuarios.

#### Crear un usuario
```bash
$ sudo rabbitmqctl add_user $username $password
```
Donde *$username* es el nombre de usuario y $password es la contraseña para ese usuario

#### Colocar un tag a un usuario
```bash
$ sudo rabbitmqctl set_user_tags $username $tag
```
Donde el *$username* es el nombre de usuario al cual se le editará su tag y el *$tag* es el tag que se le colocará ya sea administrator, user, guest entre otros

#### Establecer permisos al usuario
```bash
$ sudo rabbitmqctl set_permissions -p $hostname $username $regexConf $regexWrite $regexRead
```
Donde *$hostname* es a los host (virtual host) que tendrá acceso (o bien se relaciona el permiso), *username* es a que usuario se le aplica los cambios, *$regexConf* es una expresión regular que indica el nombre de los recursos que el usuario tendrá permiso de **configuración**, *$regexWrite* es una expresión regular que indica el nombre de los recursos que el usuario tendrá permiso de **escritura**, *$regexRead* es una expresión regular que indica el nombre de los recursos que el usuario tendrá permiso de **lecutra**

Si se configurará al usuario *seeking* como **administrador** (alguien que tendrá todos los permisos), seria de la siguiente manera
```bash
rabbitmqctl set_permissions -p / seeking ".*" ".*" ".*"
```
con el usuario listo y configurado se podrá ejecutar los archivos ejemplo (de este repo)


# Instalando Pip en ubuntu server
Ubuntu server por lo general no tiene para instalar los paquetes *python-pip, python3-pip* los cuales instalan el modulo pip de python, el modulo pip nos facilita la instalación de muchos de los paquetes, si queremos instalar este en un ubuntu que no cuente esto disponible, debemos brindarle todas las depedencias que requiere para la instalación para ello es técnicamente un binario de configuración, para una "Instalación" sencilla debemos descargar lo siguiente
```bash
$ sudo wget https://bootstrap.pypa.io/get-pip.py
```
Este archivo contiene lo mencionado anteriormente, simplemente lo compilamos con el python que queremos que tenga el modulo pip de la siguiente forma
#### Python 2
```bash
sudo python get-pip.py
```
#### Python 3
```bash
sudo python3 get-pip.py
```
Instalará el modulo de pip con el python que sea compilado y ademas agrega de forma automatica a las **variables de entorno** del sistema operativo *pip* y/o *pip3*