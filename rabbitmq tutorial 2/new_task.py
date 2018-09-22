#!/usr/bin/env python
import pika

credentials = pika.credentials.PlainCredentials("carlosrabbit", "1234", erase_on_connect=False)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.10.214', credentials=credentials, socket_timeout=2))

channel = connection.channel()


channel.queue_declare(queue='hello')

import sys
for i in range(1000000):
	message = ' '.join(sys.argv[1:]) or "Hello World! #{}".format(i)
	channel.basic_publish(exchange='',
						routing_key='hello',
						body=message)
	print(" [x] Sent %r" % message)