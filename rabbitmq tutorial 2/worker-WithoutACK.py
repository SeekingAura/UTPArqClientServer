#!/usr/bin/env python
import pika
credentials = pika.credentials.PlainCredentials("carlosrabbit", "1234", erase_on_connect=False)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.10.214', credentials=credentials, socket_timeout=2))
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