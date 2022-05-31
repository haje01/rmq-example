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

chan.exchange_declare(exchange='pubsub', exchange_type='fanout')

for i in range(10):
    msg = f"msg {i+1}"
    print("Send", msg)
    chan.basic_publish(exchange='pubsub', routing_key='', body=msg)
    time.sleep(3)