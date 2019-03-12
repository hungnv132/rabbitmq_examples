import sys
import pika


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

exchange_name = 'topic_logs'
exchange_type = 'topic'
channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

# exclusive=True: the queue should be deleted when consumer connection is closed
result = channel.queue_declare(exclusive=True)

queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

# Binding: we need to tell the exchange to send messages to our queue
for binding_key in binding_keys:
    channel.queue_bind(exchange=exchange_name,
                       queue=queue_name,
                       routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

channel.basic_consume(callback, queue=queue_name, no_ack=True)

channel.start_consuming()
