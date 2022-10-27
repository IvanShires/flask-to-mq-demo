import flask
from flask import request, Flask, render_template
import pika

def publish_queue_msg(queue,msg):
    credentials = pika.PlainCredentials('myuser', 'mypassword')
    with pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials)) as connection:
        channel = connection.channel()
        channel.queue_declare(queue=queue)
        channel.basic_publish(exchange='',
                      routing_key=queue,
                      body=msg)


app = Flask(__name__)

@app.route('/')
def index():
    client_ip = request.remote_addr
    publish_queue_msg('client_ip_addr',client_ip)
    return "Item added to the queue"

