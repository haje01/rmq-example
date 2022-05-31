import os 
import time 

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

chan.confirm_delivery()
chan.exchange_declare(exchange='conf')

try:
    chan.basic_publish(exchange='non', routing_key='', body='Hello World!')
except pika.exceptions.ChannelClosedByBroker as e:
    assert 'NOT_FOUND' in e.args[1]
    print("Message not sent")
