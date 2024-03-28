import hug, os, random, string
from kubernetes import client, config

@hug.post('/create-room')
def create_room():

    image = os.environ["INSTANCE_IMAGE"]
    namespace = os.environ["KUBERNETES_NAMESPACE"]

    # Random pod id
    pod_id = ''.join(random.choice(string.ascii_lowercase) for i in range(10)) 

    config.load_kube_config(config_file='./kubernetes-config')
    v1 = client.CoreV1Api()
	
    containers = []
    container1 = client.V1Container(name='instance', image=image)
    containers.append(container1)

    pod_spec = client.V1PodSpec(containers=containers)
    pod_metadata = client.V1ObjectMeta(name='instance-' + pod_id, namespace=namespace)

    pod_body = client.V1Pod(api_version='v1', kind='Pod', metadata=pod_metadata, spec=pod_spec)
        
    v1.create_namespaced_pod(namespace=namespace , body=pod_body)
    return pod_id

@hug.post('/delete-room')
def delete_room(body):
    return ""
