#!/usr/bin/env python3
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.8.247', socket_timeout=2))#the IP is from server
channel = connection.channel()


channel.queue_declare(queue='hello')#create a queue of messages with name "hello"

import time

def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)
	time.sleep(body.count(b'.'))#wait a number of '.' seconds exist, doing more easy to view Round-robin dispatching
	print(" [x] Done")

channel.basic_consume(callback,
					  queue='hello',
					  no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()