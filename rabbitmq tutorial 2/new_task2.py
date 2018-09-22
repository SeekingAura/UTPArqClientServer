#!/usr/bin/env python
import pika

credentials = pika.credentials.PlainCredentials("carlosrabbit", "1234", erase_on_connect=False)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.10.214', credentials=credentials, socket_timeout=2))

channel = connection.channel()


channel.queue_declare(queue='task_queue', durable=True)

import sys
message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
					routing_key='task_queue',#key is where key to use
					body=message,
					properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
print(" [x] Sent %r" % message)