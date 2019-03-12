import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create an exchange named 'logs'
exchange_name = 'topic_logs'
exchange_type = 'topic'
channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'info: Hello world!'
channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message)

print(" [x] Sent %r:%r" % (routing_key, message))

connection.close()

# sudo rabbitmqctl list_bindings
