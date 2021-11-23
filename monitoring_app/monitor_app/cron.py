from email import message
from kafka import KafkaProducer
import json
import logging
import sys
import requests
from .models import WebData, MonitorData
from datetime import datetime

logger = logging.getLogger(__name__)

def monitor_web():
    for i in WebData.objects.all():
        if (int(datetime.now().minute) % int(i.interval)) == 0 or int(i.interval) == 59:
            webStatus = requests.get(i.websiteInfo.URL, timeout=5).status_code
            row = MonitorData(WebInfo = i, time = datetime.now(), status = str(webStatus))
            temp = {
                'username': str(i.userInfo.name),
                'email': str(i.userInfo.email),
                'website': str(i.websiteInfo.name),
                'subscription': str(i.subscription),
                'status': str(webStatus),
                'date': str(datetime.now())
            }
            sys.stdout.write('data: %s\n' %temp)
            row.save()
            if i.subscription and str(webStatus) == '200':
                kafka_producer(temp)

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

def kafka_producer(data):
    producer = KafkaProducer(bootstrap_servers='localhost:9092', api_version=(0,11,5), value_serializer=json_serializer)
    producer.send("registered_user", data)
