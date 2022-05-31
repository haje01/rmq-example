import os 
import time 
import json

import requests
import pika

RMQ_HOST = os.environ['RMQ_HOST']
RMQ_PASS = os.environ['RMQ_PASS']
RMQ_ADMIN_PASS = os.environ['RMQ_ADMIN_PASS']
RMQ_API_URL = F'http://{RMQ_HOST}:15672/api/'


def http_api(cmd, method='get', data=None):
    """HTTP API 헬퍼 함수.

    Args:
        cmd (str): API 요청 명령어
        method (str): HTTP 메소드 (get, post, delete, udpate 중 하나). 기본값 'get'
        data (dict): 요청 데이터. 기본값 None
        timeout (int) : 타임아웃 초. 기본값 None

    """
    url = RMQ_API_URL + cmd
    _method = getattr(requests, method)
    res = _method(url, auth=('admin', RMQ_ADMIN_PASS), data=json.dumps(data))
    return res

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

data = {
    'pattern': 'polq',
    'definition': {
        "max-length": 3,
        "overflow": "drop-head"
    },
    'apply-to': 'queues'
}
http_api('policies/%2F/mypol', 'put', data=data)

chan.confirm_delivery()
chan.queue_declare(queue="polq")

for i in range(5):
    msg = f"msg {i+1}"
    print("Send", msg)
    chan.basic_publish(exchange='', routing_key='polq', body=msg)

# 반영 대기
time.sleep(3)

rdata = http_api('queues/%2F/polq', 'get').json()
print("messages published :", rdata['message_stats']['publish'])
print("messages ready :", rdata['messages_ready'])