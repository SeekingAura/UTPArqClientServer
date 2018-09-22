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

channel.basic_consume(callback,
                      queue='hello')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()