#!/usr/bin/env python3
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.8.191', socket_timeout=2))#the IP is from server
channel = connection.channel()
result=channel.queue_declare(exclusive=True)#temporal queue
queueNameMe = result.method.queue
channel.basic_qos(prefetch_count=1)#set number of messages resolve or consume (this case 1 at time)

channel.queue_declare(queue='conectoSitio')#create a queue of messages with name "hello"


def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)
channel.basic_qos(prefetch_count=3)
channel.basic_consume(callback,
					  queue='hello',
					  no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()