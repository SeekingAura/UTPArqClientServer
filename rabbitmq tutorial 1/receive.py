#!/usr/bin/env python3
import pika
credentials = pika.credentials.PlainCredentials("carlosrabbit", "1234", erase_on_connect=False)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.253.42.218', credentials=credentials, socket_timeout=2))
channel = connection.channel()


channel.queue_declare(queue='hello')#Create queue of meesages into server of name hello

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='hello',# Take messages from queue hello
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()