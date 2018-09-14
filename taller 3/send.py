#!/usr/bin/env python
import pika

credentials = pika.credentials.PlainCredentials("seeking", "9924", erase_on_connect=False)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.11.47', credentials=credentials, socket_timeout=2))
channel = connection.channel()


channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()