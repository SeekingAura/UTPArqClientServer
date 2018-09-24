#!/usr/bin/env python3
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.0.16'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',#Create exchange in this case for log
                         exchange_type='fanout')#type exchanger fanout is very simple, this takes all info is passing on the queue

result = channel.queue_declare(exclusive=True)#create a queue with randon name and exclusive True  erase the quere when the consumer conection is close 
queue_name = result.method.queue

channel.queue_bind(exchange='logs',##Bind queu to use for exchange, log
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()