import hug

@hug.post('/create-room')
def create_room():
    token = ""
    with open("kubernetes-token/token", "r") as f:
        token = f.read()
    return token

@hug.post('/delete-room')
def delete_room(body):
    return ""
