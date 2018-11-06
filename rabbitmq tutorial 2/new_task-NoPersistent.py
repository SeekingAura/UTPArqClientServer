#!/usr/bin/env python3
import pika


connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.253.24.206', socket_timeout=2))

channel = connection.channel()


channel.queue_declare(queue='hello')#Create queue of messages name hello

import sys
for i in range(int(sys.argv[1])):
	message = '#{} '.format(i).join(sys.argv[2:]) or "Hello World! #{}".format(i)+"."*i
	channel.basic_publish(exchange='',
						routing_key='hello',#send messages to hello queue
						body=message)
	print(" [x] Sent %r" % message)