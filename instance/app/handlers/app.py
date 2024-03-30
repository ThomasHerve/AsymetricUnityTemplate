import hug

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
    return f"Message published : {body["message"]}"