#!/usr/bin/env python3
import pika


connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.8.247', socket_timeout=2))
channel = connection.channel()


channel.queue_declare(queue='task_queue', durable=True)

import time

def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)
	time.sleep(body.count(b'.'))
	print(" [x] Done")
	ch.basic_ack(delivery_tag = method.delivery_tag)#represents ACK

channel.basic_qos(prefetch_count=1)#set number of messages resolve or consume (this case 1 at time)
channel.basic_consume(callback,
					  queue='task_queue')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()