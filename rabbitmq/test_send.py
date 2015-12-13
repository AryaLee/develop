import pika
import sys
import uuid

class testSend(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
        self.channel = self.connection.channel()

    def __del__(self):
        self.connection.close()

    def basic_test(self):
        self.channel.queue_declare(queue = 'hello')
        self.channel.basic_publish(exchange = '', routing_key = 'hello', body = 'Hello World!')
        print " Send 'Hello World!"

    def work_queue_test(self, data = []):
        self.channel.queue_declare(queue = 'task_queue', durable = True)
        message = " ".join(data) or "hello world!"
        self.channel.basic_publish(exchange = '', routing_key = 'task_queue', body = message, properties = pika.BasicProperties(delivery_mode = 2))
        print " Send %r" %message

    def publish_subscribe_test(self):
        self.channel.exchange_declare(exchange = 'logs', type = 'fanout')
        message = ' '.join(sys.argv[1:]) or "info: Hello World!"
        self.channel.basic_publish(exchange = 'logs', routing_key = '', body = message)
        print "send %r" %message


    def routing_test(self):
        self.channel.exchange_declare(exchange = 'direct_logs', type = 'direct')
        severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
        message = ' '.join(sys.argv[2:]) or 'hello world!'
        self.channel.basic_publish(exchange = 'direct_logs', routing_key = severity, body = message)
        print 'Send %r:%r' %(severity, message)

    def topics_test(self):
        self.channel.exchange_declare(exchange = 'topic_logs', type = 'topic')
        routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
        message = ' '.join(sys.argv[2:]) or 'Hello World'
        self.channel.basic_publish(exchange = 'topic_logs', routing_key = routing_key, body = message)
        print 'Send %r:%r' %(routing_key, message)

    def on_response(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = body

    def rpc_test(self, n):
        result = self.channel.queue_declare(exclusive = True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack = True, queue = self.callback_queue)

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange = '', routing_key = 'rpc_queue', properties = pika.BasicProperties(reply_to = self.callback_queue, correlation_id = self.corr_id), body = str(n))

        while self.response is None:
            self.connection.process_data_events()

        print 'get response %r' %self.response


if __name__ == '__main__':
    test = testSend()
    # test.basic_test()
    # test.work_queue_test()
    # test.publish_subscribe_test()
    # test.routing_test()
    # test.topics_test()
    test.rpc_test(10)

