import re
import argparse
from kubernetes import client, config

def get_namespaces_matching_pattern(pattern):
    v1 = client.CoreV1Api()
    all_namespaces = v1.list_namespace().items
    matched_namespaces = [ns.metadata.name for ns in all_namespaces if re.match(pattern, ns.metadata.name)]
    return matched_namespaces

def get_pods_in_namespace(namespace):
    v1 = client.CoreV1Api()
    pods = v1.list_namespaced_pod(namespace).items
    return pods

def main(regex_pattern):
    # Load kubeconfig
    config.load_kube_config()
    
    # Get namespaces matching the provided regex pattern
    namespaces = get_namespaces_matching_pattern(regex_pattern)
    if not namespaces:
        print(f"No namespaces found matching the pattern: {regex_pattern}")
        return

    for namespace in namespaces:
        print(f"\nNamespace: {namespace}")
        pods = get_pods_in_namespace(namespace)
        for pod in pods:
            print(f"  Pod: {pod.metadata.name}")
            for container in pod.spec.containers:
                print(f"    Container Name: {container.name}")
                print(f"    Image: {container.image}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get container names and images from namespaces matching a regex pattern.')
    parser.add_argument('pattern', type=str, help='The regex pattern to match namespaces.')
    args = parser.parse_args()
    
    main(args.pattern)
