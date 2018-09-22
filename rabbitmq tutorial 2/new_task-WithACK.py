#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.8.247', socket_timeout=2))

channel = connection.channel()


channel.queue_declare(queue='task_queue', durable=True)

import sys
for i in range(int(sys.argv[1])):
	message = '#{} '.format(i).join(sys.argv[2:]) or "Hello World! #{}".format(i)+"."*i
	channel.basic_publish(exchange='',
						routing_key='task_queue',#key is where key to use
						body=message,
						properties=pika.BasicProperties(
							delivery_mode = 2, # make message persistent, not end until message consumes
						))
	print(" [x] Sent %r" % message)