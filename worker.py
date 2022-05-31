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

chan.queue_declare(queue='taskq', durable=True)
count = 0

def callback(ch, method, prop, body):
    print(body.decode('utf-8'))
    # 시간이 걸리는 처리
    time.sleep(3)  
    ch.basic_ack(delivery_tag=method.delivery_tag)

chan.basic_qos(prefetch_count=1)
chan.basic_consume('taskq', callback)
chan.start_consuming()