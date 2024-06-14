import os
import schedule
import time
from dotenv import load_dotenv
import docker
import grpc
import containerd_services_pb2_grpc as services
import containerd_services_pb2 as messages
import logging

# Load environment variables from .env file
load_dotenv()

# Retrieve the container engine from the environment variable
container_engine = os.getenv("CONTAINER_ENGINE")
launch_hour =  str(os.getenv("LAUNCH_HOUR"))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def prune_docker_images():
    client = docker.from_env()
    try:
        client.images.prune(filters={'dangling': False})
        logging.info("Docker images pruned successfully.")
    except Exception as e:
        logging.error(f"Error pruning Docker images: {e}")

def prune_containerd_images():
    channel = grpc.insecure_channel("unix:///run/containerd/containerd.sock")
    client = services.ImagesStub(channel)
    request = messages.PruneRequest()
    try:
        response = client.Prune(request)
        for msg in response:
            print(msg)
        logging.info("containerd images pruned successfully.")
    except Exception as e:
        logging.error(f"Error pruning containerd images: {e}")

def prune_images():
    if container_engine == "docker":
        prune_docker_images()
    elif container_engine == "containerd":
        prune_containerd_images()
    else:
        logging.error(f"Unsupported container engine: {container_engine}")
        raise ValueError("Unsupported container engine specified in environment variable")


schedule.every().day.at(launch_hour).do(prune_images)

# Keep the script running to maintain the schedule
while True:
    schedule.run_pending()
    time.sleep(1)
