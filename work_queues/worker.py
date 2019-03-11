import time
import pika

"""
we'll create a Work Queue that will be used to distribute 
time-consuming tasks among multiple workers.
"""


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(10)
    print(" [x] Done")
    channel.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# When RabbitMQ quits or crashes it will forget the queues and messages
# unless you tell it not to.
# we need to mark both the queue and messages as durable.
queue_name = 'task_queue'
channel.queue_declare(queue=queue_name, durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

# tells RabbitMQ not to give more than one message to a worker at a time
# or don't dispatch a new message to a worker until it has processed and
# acknowledged the previous one.
# It will dispatch it to the next worker that is not still busy.
channel.basic_qos(prefetch_count=1)

# In order to make sure a message is never lost, RabbitMQ supports message
# acknowledgments. An ack(nowledgement) is sent back by the consumer to
# tell RabbitMQ
channel.basic_consume(callback, queue=queue_name, no_ack=False)

channel.start_consuming()
