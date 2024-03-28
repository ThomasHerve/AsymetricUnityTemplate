import hug
from kubernetes import client, config

@hug.post('/create-room')
def create_room():
    config.load_kube_config(config_file='./kubernetes-config')
    v1 = client.CoreV1Api()
    l = []
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        l.append(i.status.pod_ip + " " + i.metadata.namespace + " " + i.metadata.name)
    return l

@hug.post('/delete-room')
def delete_room(body):
    return ""
