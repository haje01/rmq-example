import os 
import time 
import json

import requests
import pika

RMQ_HOST = os.environ['RMQ_HOST']
RMQ_PASS = os.environ['RMQ_PASS']
RMQ_API_URL = F'http://{RMQ_HOST}:15672/api/'

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

chan.exchange_declare(exchange='mand', exchange_type='direct')

chan.basic_publish(exchange='mand', routing_key='mand', mandatory=True, body='msg 1')

chan.confirm_delivery()

try:
    chan.basic_publish(exchange='mand', routing_key='mand', mandatory=True,
        body='msg 2')
except pika.exceptions.UnroutableError:
    print('Mandatory message not delivered')
