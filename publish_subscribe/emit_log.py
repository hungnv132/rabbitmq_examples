import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create an exchange named 'logs'
channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or 'info: Hello world!'
queue_name = ''
channel.basic_publish(exchange='logs', routing_key=queue_name, body=message)

print(" [x] Sent %r" % message)

connection.close()

# sudo rabbitmqctl list_bindings
