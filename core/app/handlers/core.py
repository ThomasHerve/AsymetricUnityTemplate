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
	
    # Create a pod
    containers = []
    container1 = client.V1Container(name='instance', image=image)
    containers.append(container1)

    pod_spec = client.V1PodSpec(containers=containers) # TODO SELECTOR
    pod_metadata = client.V1ObjectMeta(name='instance-' + pod_id, namespace=namespace)

    pod_body = client.V1Pod(api_version='v1', kind='Pod', metadata=pod_metadata, spec=pod_spec)
        
    v1.create_namespaced_pod(namespace=namespace , body=pod_body)

    # Create a service
    service_port_list = [client.V1ServicePort(port=8000, target_port=80, name='instance-' + pod_id)]
    service_spec = client.V1ServiceSpec(ports=service_port_list, selector={
        "pod_id": pod_id
    })
    service_metadata = client.V1ObjectMeta(name='instance-' + pod_id, namespace=namespace)
    service = kubernetes.client.V1Service()


    return pod_id

@hug.post('/delete-room')
def delete_room(body):

    namespace = os.environ["KUBERNETES_NAMESPACE"]
    
    config.load_kube_config(config_file='./kubernetes-config')
    v1 = client.CoreV1Api()

    pods_list = v1.list_namespaced_pod(namespace=namespace)
    pods = [item.metadata.name for item in pods_list.items]
    if not f"instance-{body["instance"]}" in pods:
        return "Instance " + body["instance"] + " does not exist"

    v1.delete_namespaced_pod(namespace=namespace, name='instance-'+body["instance"])

    return "Ok"
