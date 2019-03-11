import pika

# To establish a connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# To create a 'hello' queue to which the message will be delivered
channel.queue_declare(queue='hello')

# RabbitMQ never send a message directly to the queue, always need to go through
# exchanges.
# Default exchange is an empty string, allow us to specify exactly to
# which queue the message should go.
message = 'Hello you!'
channel.basic_publish(exchange='', routing_key='hello', body=message)

print(" [x] Sent 'Hello World!'")
connection.close()

# sudo rabbitmqctl list_queues
