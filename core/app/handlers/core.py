import hug, os, random, string
from kubernetes import client, config

@hug.post('/create-room')
def create_room():

    image = os.environ["INSTANCE_IMAGE"]
    namespace = os.environ["KUBERNETES_NAMESPACE"]
    ingress = os.environ["KUBERNETES_INGRESS_NAME"]
    port = int(os.environ["KUBERNETES_PORT"])

    # Random pod id
    pod_id = ''.join(random.choice(string.ascii_lowercase) for i in range(10)) 

    config.load_kube_config(config_file='./kubernetes-config')
    v1 = client.CoreV1Api()
	
    # Create a pod
    containers = []
    container1 = client.V1Container(name='instance', image=image)
    containers.append(container1)

    pod_spec = client.V1PodSpec(containers=containers)
    pod_metadata = client.V1ObjectMeta(name='instance-' + pod_id, namespace=namespace, labels={
        "pod_id": pod_id
    })

    pod_body = client.V1Pod(api_version='v1', kind='Pod', metadata=pod_metadata, spec=pod_spec)
        
    v1.create_namespaced_pod(namespace=namespace , body=pod_body)

    # Create a service
    service_port_list = [client.V1ServicePort(port=port, target_port=port, name='http')]
    service_spec = client.V1ServiceSpec(ports=service_port_list, selector={
        "pod_id": pod_id
    })
    service_metadata = client.V1ObjectMeta(name='instance-' + pod_id, namespace=namespace)
    service = client.V1Service(metadata=service_metadata, spec=service_spec)
    
    v1.create_namespaced_service(namespace=namespace , body=service)

    # Update the ingress class
    networking = client.NetworkingV1Api()

    current_ingress = networking.read_namespaced_ingress(name=ingress, namespace=namespace)
    current_ingress_paths = current_ingress.spec.rules[0].http.paths
    current_ingress_paths.append(client.V1HTTPIngressPath(path=f"/{pod_id}(/|$)(.*)", path_type="Prefix", backend=client.V1IngressBackend(service=client.V1IngressServiceBackend(name=f"instance-{pod_id}", port=client.V1ServiceBackendPort(number=port)))))
    current_ingress.spec.rules[0].http.paths = current_ingress_paths

    networking.patch_namespaced_ingress(ingress, namespace, current_ingress)

    return pod_id

@hug.post('/delete-room')
def delete_room(body):
    ingress = os.environ["KUBERNETES_INGRESS_NAME"]
    namespace = os.environ["KUBERNETES_NAMESPACE"]
    
    config.load_kube_config(config_file='./kubernetes-config')
    v1 = client.CoreV1Api()

    pods_list = v1.list_namespaced_pod(namespace=namespace)
    pods = [item.metadata.name for item in pods_list.items]
    if not f"instance-{body['instance']}" in pods:
        return "Instance " + body["instance"] + " does not exist"

    v1.delete_namespaced_pod(namespace=namespace, name='instance-'+body["instance"])
    v1.delete_namespaced_service(namespace=namespace, name='instance-'+body["instance"])

    # Remove ingress entry
    networking = client.NetworkingV1Api()
    current_ingress = networking.read_namespaced_ingress(name=ingress, namespace=namespace)
    current_ingress_paths = current_ingress.spec.rules[0].http.paths
    current_ingress_paths = list(filter(lambda x: x.backend.service.name != f"instance-{body["instance"]}", current_ingress_paths))
    current_ingress.spec.rules[0].http.paths = current_ingress_paths

    networking.patch_namespaced_ingress(ingress, namespace, current_ingress)

    return "Ok"
