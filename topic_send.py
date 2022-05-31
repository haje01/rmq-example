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

chan.exchange_declare(exchange='top', exchange_type='topic')

chan.basic_publish(exchange='top', routing_key='meal.korean', body='bulgogi')
chan.basic_publish(exchange='top', routing_key='meal.chinese', body='jjajang-myeon')
chan.basic_publish(exchange='top', routing_key='desert.chinese', body='tanghuru')
chan.basic_publish(exchange='top', routing_key='desert.korean', body='sikhye')
