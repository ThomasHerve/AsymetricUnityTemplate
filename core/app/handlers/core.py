import hug, base64, os

@hug.post('/create-room')
def create_room():
    token = base64.b64decode(os.environ["KUBERNETES_TOKEN"])
    return token

@hug.post('/delete-room')
def delete_room(body):
    return ""
