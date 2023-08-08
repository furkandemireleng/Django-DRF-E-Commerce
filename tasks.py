import os

import pika
from celery import shared_task, current_task
from celery.exceptions import MaxRetriesExceededError
from django.core.mail import EmailMessage, get_connection
from dotenv import load_dotenv

load_dotenv()


@shared_task
def send_push_notification(message):
    username = os.environ.get('RABBITMQ_USER')
    password = os.environ.get('RABBITMQ_PASSWORD')
    host = os.environ.get('RABBITMQ_HOST')
    port = os.environ.get('RABBITMQ_PORT')

    credentials = pika.PlainCredentials(f'{username}', f'{password}')
    parameters = pika.ConnectionParameters(f'{host}',
                                           int(port),
                                           '/',
                                           credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Declare a queue named 'my_queue'
    channel.queue_declare(queue='queue')

    # Publish the message to the 'my_queue' queue
    channel.basic_publish(exchange='', routing_key='queue', body=message)


