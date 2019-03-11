import sys
import pika

"""
we'll create a Work Queue that will be used to distribute 
time-consuming tasks among multiple workers.
"""

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# When RabbitMQ quits or crashes it will forget the queues and messages
# unless you tell it not to.
# we need to mark both the queue and messages as durable.
queue_name = 'task_queue'
channel.queue_declare(queue=queue_name, durable=True)

message = ' '.join(sys.argv[1:]) or 'Hello world!'
channel.basic_publish(exchange='',
                      routing_key=queue_name,
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=2,  # make message persistent
                      ))

print(" [x] Sent  %r" % message)
connection.close()
