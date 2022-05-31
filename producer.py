import os 

import pika

RMQ_HOST = os.environ['RMQ_HOST']
RMQ_PASS = os.environ['RMQ_PASS']

# RabbitMQ 패스워드로 크레덴셜
cred = pika.PlainCredentials('rabbit', RMQ_PASS)

# RabbitMQ 주소로 커넥션 초기화 
conn = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=RMQ_HOST,
        credentials=cred,
    )
)

# 채널 생성
chan = conn.channel()

chan.queue_declare(queue='minq')

chan.basic_publish(exchange='', routing_key='minq', body='Hello World!')
chan.basic_publish(exchange='', routing_key='minq', body='Hello World!')
