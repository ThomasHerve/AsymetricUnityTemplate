import hug
from kubernetes import client, config

@hug.post('/create-room')
def create_room():
    config.load_kube_config(config_file='./kubernetes-config')
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    return ret.items[0].metadata.name

@hug.post('/delete-room')
def delete_room(body):
    return ""
