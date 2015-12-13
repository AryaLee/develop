import pika
import sys
import time

class testReceive(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
        self.channel = self.connection.channel()

    def __del__(self):
        self.connection.close()

    def basic_test(self):
        self.channel.queue_declare(queue = 'hello')

        def callback(ch, method, properties, body):
            print "receive %r" %body

        self.channel.basic_consume(callback, queue = 'hello', no_ack = True)
        print "Waiting for messages. To exit press Ctrl+C"
        self.channel.start_consuming()

    def work_queue_test(self):
        self.channel.queue_declare(queue = 'task_queue', durable = True)
        print "Waiting for message. To exit press Ctrl+C"
        def callback(ch, method, properties, body):
            print "receive %r" %body
            time.sleep(body.count(b'.'))
            print "Done"
            ch.basic_ack(delivery_tag = method.delivery_tag)

        self.channel.basic_qos(prefetch_count = 1)
        self.channel.basic_consume(callback, queue = 'task_queue')

        self.channel.start_consuming()

    def publish_subscribe_test(self):
        self.channel.exchange_declare(exchange = 'logs', type = 'fanout')
        result = self.channel.queue_declare(exclusive = True)
        queue_name = result.method.queue

        self.channel.queue_bind(exchange = 'logs', queue = queue_name)
        print "Waiting for message. To exit press Ctrl+C"
        def callback(ch, method, properties, body):
            print '%r' %body

        self.channel.basic_consume(callback, queue = queue_name, no_ack = True)
        self.channel.start_consuming()

    def routing_test(self):
        self.channel.exchange_declare(exchange = 'direct_logs', type = 'direct')
        result = self.channel.queue_declare(exclusive = True)
        queue_name = result.method.queue
        
        servities = sys.argv[1:]
        if not servities:
            sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
            sys.exit(1)

        for servity in servities:
            self.channel.queue_bind(exchange = 'direct_logs', queue = queue_name, routing_key = servity)

        print "Waiting for message. To exit press Ctrl+C"
        def callback(ch, method, properties, body):
            print '%r:%r' %(method.routing_key, body)

        self.channel.basic_consume(callback, queue = queue_name, no_ack = True)

        self.channel.start_consuming()

    def topics_test(self):
        self.channel.exchange_declare(exchange = 'topic_logs', type = 'topic')
        result = self.channel.queue_declare(exclusive = True)
        queue_name = result.method.queue

        binding_keys = sys.argv[1:]

        if not binding_keys:
            sys.stderr.write('Usage: %s [binding_key]...\n' %sys.argv[0])
            sys.exit(1)

        for binding_key in binding_keys:
            self.channel.queue_bind(exchange = 'topic_logs', queue = queue_name, routing_key = binding_key)
        
        print "Waiting for message. To exit press Ctrl+C"

        def callback(ch, method, properities, body):
            print (' %r:%r' %(method.routing_key, body))

        self.channel.basic_consume(callback, queue = queue_name, no_ack = True)
        self.channel.start_consuming()

    def rpc_test(self):
        self.channel.queue_declare(queue = 'rpc_queue')
        self.channel.basic_qos(prefetch_count = 1)
        self.channel.basic_consume(self.on_request, queue = 'rpc_queue')

        print "Waiting RPC requests"
        self.channel.start_consuming()

    def fib(self, n):
        if n <= 1:
            return n
        else:
            return self.fib(n-1) + self.fib(n-2)

    def on_request(self, ch, method, properties, body):
        n = int(body)
        print 'fib(%s)' %n
        response = self.fib(n)
        ch.basic_publish(exchange = '', routing_key = properties.reply_to, properties = pika.BasicProperties(correlation_id = properties.correlation_id), body = str(response))
        ch.basic_ack(delivery_tag = method.delivery_tag)

if __name__== '__main__':
    test = testReceive()
    # test.basic_test()
    # test.work_queue_test()
    # test.publish_subscribe_test()
    # test.routing_test()
    # test.topics_test()
    test.rpc_test()


