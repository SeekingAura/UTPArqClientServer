#!/usr/bin/env python
import pika

credentials = pika.credentials.PlainCredentials("carlosrabbit", "1234", erase_on_connect=False)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.253.42.218', credentials=credentials, socket_timeout=2))

channel = connection.channel()


channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()