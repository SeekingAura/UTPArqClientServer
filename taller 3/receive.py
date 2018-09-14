#!/usr/bin/env python
import pika
credentials = pika.credentials.PlainCredentials("seeking", "9924", erase_on_connect=False)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.253.1.9', credentials=credentials, socket_timeout=2))
channel = connection.channel()


channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()