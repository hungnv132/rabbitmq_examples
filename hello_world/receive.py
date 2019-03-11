import pika


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Both send.py and receive.py file declare the queue name to make sure that
# the queue exists
# We don't know which one run first. In such cases it's a good practice to
# repeat declaring the queue in both programs.
channel.queue_declare(queue='hello')

# subscribe a callback function to a queue
queue_name = 'hello'
channel.basic_consume(callback, queue=queue_name, no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
