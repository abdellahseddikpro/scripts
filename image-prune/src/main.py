import os
import schedule
import time
from dotenv import load_dotenv
import logging
import subprocess
# Load environment variables from .env file
load_dotenv()

# Retrieve the container engine from the environment variable
container_engine = os.getenv("CONTAINER_ENGINE")
launch_hour =  str(os.getenv("LAUNCH_HOUR"))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def prune_docker_images():
    try:
        result = subprocess.run(['docker', 'image', 'prune', '-af'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(f"Docker images pruned successfully. Output: {result.stdout.decode('utf-8')}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error pruning Docker images: {e.stderr.decode('utf-8')}")

def prune_containerd_images():
    try:
        result = subprocess.run(['ctr', '-n', 'k8s.io', 'images', 'prune'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(f"containerd images pruned successfully. Output: {result.stdout.decode('utf-8')}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error pruning containerd images: {e.stderr.decode('utf-8')}")

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
