import time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello', durable=True)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(10)
    print(" [x] Done")
    channel.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(callback, queue='hello', no_ack=False)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
