import hug, os, random, string
from kubernetes import client, config
import qrcode
from PIL import Image

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
    container1 = client.V1Container(name='instance', image=image, env=[client.V1EnvVar(name="INSTANCE_NAME", value=pod_id), client.V1EnvVar(name="BACKEND_URL", value=os.environ["BACKEND_URL"]), client.V1EnvVar(name="PASSWORD", value=os.environ["PASSWORD"])])
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

    # QR code
    url = value=os.environ["BACKEND_URL"] + "/" + pod_id
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Créer une image PIL à partir du QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Convertir l'image PIL en tableau de 0 et de 1
    qr_array = []
    width, height = img.size
    pixels = img.load()
    for y in range(height):
        row = []
        for x in range(width):
            # Si le pixel est noir (représentant le code QR), ajouter 1, sinon 0
            row.append(1 if pixels[x, y] == 0 else 0)
        qr_array.append(row)

    return {"instance": pod_id, "qr_code": qr_array}

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

    if "password" not in body or body["password"] != os.environ["PASSWORD"]:
        return "Wrong password"

    v1.delete_namespaced_pod(namespace=namespace, name='instance-'+body["instance"])
    v1.delete_namespaced_service(namespace=namespace, name='instance-'+body["instance"])

    # Remove ingress entry
    networking = client.NetworkingV1Api()
    current_ingress = networking.read_namespaced_ingress(name=ingress, namespace=namespace)
    current_ingress_paths = current_ingress.spec.rules[0].http.paths
    current_ingress_paths = list(filter(lambda x: x.backend.service.name != f"instance-{body['instance']}", current_ingress_paths))
    current_ingress.spec.rules[0].http.paths = current_ingress_paths

    networking.patch_namespaced_ingress(ingress, namespace, current_ingress)

    return "Ok"
