import hug
import requests
import os

messages = []

@hug.get('/pull')
def pull():
    global messages
    send = messages.copy()
    messages = []
    return send

@hug.post('/publish')
def publish(body):
    global messages
    messages.append(body["message"])
    return f"Message published : {body['message']}"

@hug.post('/stop')
def stop():
    instance_name = os.environ["INSTANCE_NAME"]
    backend_url = os.environ["BACKEND_URL"]
    requests.post(f"https://{backend_url}/delete-room", data={"instance": instance_name})
    return "deleted"